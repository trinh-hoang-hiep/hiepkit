from onnx_models import SynthesizerTrn
import utils
from text import text_to_sequence
from text.symbols import symbols
import torch
import commons_onnx as commons_onnx
from scipy.io.wavfile import write
import glob
import os


export_path = "onnx_convert"

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons_onnx.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file("C:\\Users\\sodalab\\Downloads//vietnamese_man_pham_nguyen_son_tung_doc_truyen.json")

print(f"len(symbols): {len(symbols)}")
net_g = SynthesizerTrn(
    len(symbols)
,
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model)
_ = net_g.eval()

def latest_checkpoint_path(dir_path, regex="G_*.pth"):
    f_list = glob.glob(os.path.join(dir_path, regex))
    f_list.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    x = f_list[-1]
    return x
latest_checkpoint = latest_checkpoint_path("C:\\Users\\sodalab\\Downloads/checkpoint")
print('Last checkpoint:', latest_checkpoint)
_ = utils.load_checkpoint(latest_checkpoint, net_g)

text = 'hoj˨˦-kaj˧˩˨ va˧˨ kɔ˨˦ ɲiəw˧˨ dɔŋ͡m˨˦-ɣɔp˦˥ tik˦˥-kɯk˨ˀ˩ cɔ˧˧ ɲa˧˨-tu˧˨ = ɣɤ̆n˧˨ dɤ̆j˧˧ kɔ˨˦ den˨˦ mot˨ˀ˩ buəj˧˩˨ ciən˧˩˨-lam˧ˀ˥ c@ŋ˧˧ ban˨˦ haŋ˧˨ tɯ˧˨-tʰiən˨ˀ˩ʔ'
stn_tst = get_text(text, hps)
with torch.no_grad():
    x_tst = stn_tst.unsqueeze(0)
    x_tst_lengths = torch.LongTensor([stn_tst.size(0)])#####.unsqueeze(0) #####thhiep
    if hps.data.n_speakers > 0:
        sid = torch.tensor([0])
    else:
        sid = None
    o = net_g(x_tst, x_tst_lengths, sid, export_path)[0,0].data.cpu().float().numpy()
    
    file_name = f'test_onnx.wav'
    write(file_name, hps.data.sampling_rate, o)