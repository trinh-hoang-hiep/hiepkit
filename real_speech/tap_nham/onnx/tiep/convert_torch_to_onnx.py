
import matplotlib.pyplot as plt

import os
from datetime import datetime
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
import glob

import commons_onnx
import utils
# from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from onnx_models import SynthesizerTrn######################onnx_models
from text.symbols import symbols
from text import text_to_sequence

from scipy.io.wavfile import write
import argparse
import onnxruntime as ort
import random
import onnx
import numpy as np


class TTSWrapper(nn.Module):
    
    def __init__(self, hps, latest_checkpoint):
        super().__init__()
        
        self.net_g = SynthesizerTrn(
            len(symbols),
            hps.data.filter_length // 2 + 1,
            hps.train.segment_size // hps.data.hop_length,
            n_speakers=hps.data.n_speakers,
            **hps.model).to("cpu")
        self.net_g.eval()
        
        _ = utils.load_checkpoint(latest_checkpoint, self.net_g, None)
        # self.use_sdp = self.net_g.use_sdp
        
    def forward(self, x, x_lengths, sid=None, noise_scale=1, length_scale=1, noise_scale_w=1., max_len=None):
        x, m_p, logs_p, x_mask = self.net_g.enc_p(x, x_lengths)
        if self.net_g.n_speakers > 0:
            g = self.net_g.emb_g(sid).unsqueeze(-1) # [b, h, 1]
        else:
            g = None

        if self.net_g.use_sdp:
            logw = self.net_g.dp(x, x_mask, g=g, reverse=True, noise_scale=noise_scale_w)
        else:
            logw = self.net_g.dp(x, x_mask, g=g)
        w = torch.exp(logw) * x_mask * length_scale
        w_ceil = torch.ceil(w)
        y_lengths = torch.clamp_min(torch.sum(w_ceil, [1, 2]), 1).long()
        y_mask = torch.unsqueeze(commons_onnx.sequence_mask(y_lengths, None), 1).to(x_mask.dtype)
        attn_mask = torch.unsqueeze(x_mask, 2) * torch.unsqueeze(y_mask, -1)
        attn = commons_onnx.generate_path(w_ceil, attn_mask)

        m_p = torch.matmul(attn.squeeze(1), m_p.transpose(1, 2)).transpose(1, 2) # [b, t', t], [b, t, d] -> [b, d, t']
        logs_p = torch.matmul(attn.squeeze(1), logs_p.transpose(1, 2)).transpose(1, 2) # [b, t', t], [b, t, d] -> [b, d, t']

        z_p = m_p + torch.randn_like(m_p) * torch.exp(logs_p) * noise_scale
        z = self.net_g.flow(z_p, y_mask, g=g, reverse=True)
        o = self.net_g.dec((z * y_mask)[:,:,:max_len], g=g)
        return o#, attn, y_mask, (z, z_p, m_p, logs_p)
    
    
def latest_checkpoint_path(dir_path, regex="G_*.pth"):
    f_list = glob.glob(os.path.join(dir_path, regex))
    f_list.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    x = f_list[-1]
    return x

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons_onnx.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

def to_numpy(x):
    return np.array((x)).astype(np.float64)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="nu_mienbac")
    args = parser.parse_args()

    args.config = 'C:\\Users\\sodalab\\Downloads//vietnamese_man_pham_nguyen_son_tung_doc_truyen.json'
    latest_checkpoint = latest_checkpoint_path("C:\\Users\\sodalab\\Downloads/checkpoint")
    print('Last checkpoint:', latest_checkpoint)

    # load
    hps = utils.get_hparams_from_file(args.config)
    model = TTSWrapper(hps, latest_checkpoint)

    # default config
    noise_scale = .667
    length_scale = 1.
    noise_scale_w = 0.8
    text = 'hoj˨˦-kaj˧˩˨ va˧˨ kɔ˨˦ ɲiəw˧˨ dɔŋ͡m˨˦-ɣɔp˦˥ tik˦˥-kɯk˨ˀ˩ cɔ˧˧ ɲa˧˨-tu˧˨ = ɣɤ̆n˧˨ dɤ̆j˧˧ kɔ˨˦ den˨˦ mot˨ˀ˩ buəj˧˩˨ ciən˧˩˨-lam˧ˀ˥ c@ŋ˧˧ ban˨˦ haŋ˧˨ tɯ˧˨-tʰiən˨ˀ˩ʔ'
    speaker_id = 1
    
    print('Raw text:', text, len(text))
    stn_tst = get_text(text, hps)
    # print('Processed text:', stn_tst)
    with torch.no_grad():
        x_tst = stn_tst.to("cpu").unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to("cpu")
        sid = torch.LongTensor([speaker_id]).to("cpu")
        audio = model(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale, length_scale=length_scale, noise_scale_w=noise_scale_w)[0,0].data.cpu().float().numpy()

    print(audio.shape)
    
    postfix = os.path.basename(latest_checkpoint)[:-4]
    
    file_name = f'test_pytorch_{postfix}.wav'
    write(file_name, hps.data.sampling_rate, audio)

    # export
    torch.onnx.export(
        model,
        (x_tst, x_tst_lengths, sid, noise_scale, length_scale, noise_scale_w),
        'onnx_model_name.onnx',
        verbose=False,                   
        export_params=True,             # store the trained parameter weights inside the model file
        opset_version=14,               # the ONNX version to export the model to
        do_constant_folding=True,       # whether to execute constant folding for optimization
        input_names = ['x_tst', 'x_tst_lengths', 'sid', 'noise_scale', 'length_scale', 'noise_scale_w'],        # the model's input names
        output_names = ['output'],      # the model's output names
        dynamic_axes={'input' : {0 : 'batch_size'}, 'output' : {0 : 'batch_size'}})  # variable length axes




    # check conversion
    model = onnx.load('onnx_model_name.onnx')
    output =[node.name for node in model.graph.output]

    input_all = [node.name for node in model.graph.input]
    input_initializer =  [node.name for node in model.graph.initializer]
    net_feed_input = list(set(input_all)  - set(input_initializer))

    print('Inputs: ', net_feed_input)
    print('Outputs: ', output)
    
    # test inference
    ort_session = ort.InferenceSession('onnx_model_name.onnx')
    input_dict = {
        'x_tst': x_tst.numpy().astype(np.int64), 
        'x_tst_lengths': x_tst_lengths.numpy().astype(np.int64), 
        # 'sid': torch.LongTensor([speaker_id+1]).to("cpu").numpy().astype(np.int64), 
        'noise_scale_w': to_numpy(noise_scale_w), 
        'length_scale':to_numpy(length_scale), 
        'noise_scale': to_numpy(noise_scale),
        }
    output_onnx = ort_session.run(None, input_dict)[0][0,0]
    print(output_onnx.shape)
    
    file_name = f'test_onnx_{postfix}.wav'
    write(file_name, hps.data.sampling_rate, output_onnx)
    
    