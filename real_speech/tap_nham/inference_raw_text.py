import matplotlib.pyplot as plt
import IPython.display as ipd
MAX_INT = 32768
import numpy as np

import os
from datetime import datetime
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader

import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text.symbols_character_shortsilence import symbols as symbolscharacter
from text import text_to_sequence

from scipy.io.wavfile import write

import argparse
import time
import re


import asyncio
from text2phonemesequence import Text2PhonemeSequence
from tests.nguyenlm_text_normalization import norm_text_extend
from normalize_input.normalize import normalize_input_text_to_speech
from utils_text import split_long_document

def get_text(text,is_character, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners,is_character=is_character)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)

    text_norm = torch.LongTensor(text_norm)
    return text_norm

# Load Text2PhonemeSequence
model = Text2PhonemeSequence(pretrained_g2p_model='charsiu/g2p_multilingual_byT5_small_100', language='vie-n-fix', is_cuda=True)


def convert_text_to_phoneme(list_token):
  phones=[]
  for token in list_token:
    subphones=[]
    for subtoken in token.split("-"):
      subphones.append(model.infer_sentence(subtoken).replace(" ", "").replace("▁", " "))
    phones.append("-".join(subphones))
  return phones


def tokenize_text_for_short_silence(text):
    text=text.replace("@", "a_còng")
    tokenized_text=norm_text_extend(text)
    return tokenized_text



def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)




def convert_rawtext_to_phoneme(text):
    
    text=deEmojify(text)
    text=tokenize_text_for_short_silence(text)
    textarr=text.split(" ")
    mask_equal=[0 if i !="=" else 1 for i in textarr]
    phonemes=convert_text_to_phoneme(textarr)
    phonemes=[ "=" if (mask ==1) else phonemes[i] for i, mask in enumerate(mask_equal)]#####["=" if mask_equal[i] ==1 else phonemes[i] for i in range(mask_equal)]
    stringphoneme=" ".join(phonemes)
    return stringphoneme

arrtext=[
#          "anh ta đương trải qua một giặng đường luẩn quẩn không vinh hiển",
#          "và phục tùng số phận đã khiến cho anh có một tâm hồn thanh bạch",
# #          "• Cắt lớp 3 chất liệu cầu kỳ kết hợp cotton co giãn thoải mái , dệt thoáng nhẹ mát @ 🌬",
#          "nên khi phải đánh-thức nhau chúng đá vào mạng mỡ của nhau mà la lên",
#          "để hun đúc anh ta trở nên một kẻ lẩn thẩn",
#          "chỉ vì nói tới cái quảng trường ấy",
#          "nhưng mà vốn có óc một nhà triết lý",
#          "phúc chỉ đáp thế nào cho phải phép",
        "Tuần này, FPT Software AI Center gấp đôi niềm vui khi 2 bài báo nghiên cứu mới của các học viên chương trình AI Residency đã được chấp nhận tại Hội nghị The Association for Computational Linguistics thường niên lần thứ 62 (ACL 2024).",
        "Hội nghị The Association for Computational Linguistics (ACL) là hội nghị quốc tế hàng đầu (rank A*) về lĩnh vực ngôn ngữ học tính toán, bao gồm nhiều lĩnh vực nghiên cứu đa dạng liên quan đến các phương pháp tính toán đối với ngôn ngữ tự nhiên",
        "Đây là hội nghị thường niên được tổ chức bởi Hiệp hội Ngôn ngữ học tính toán, thu hút rất nhiều các nhà nghiên cứu, các tài năng trong lĩnh vực công nghệ đến từ khắp nơi trên thế giới",
        "Hội nghị ACL lần thứ 62 sẽ diễn ra tại Trung tâm Hội nghị Centara Grand and Bangkok, Bangkok, Thái Lan từ ngày 11 đến ngày 16 tháng 8 năm nay",
        "Các mô hình Transformer được chứng minh không bền vững với các văn bản đối nghịch. Các phương pháp đánh giá độ bền vững thường chỉ được thực hiện sau khi tinh chỉnh các mô hình mà không quan tâm đến dữ liệu huấn luyện. Trong bài báo này, nhóm nghiên cứu đã chứng minh rằng có mối tương quan chặt chẽ giữa dữ liệu huấn luyện và độ bền vững của mô hình. Tập trung chủ yếu vào các mô hình Transformer Encoder-only như BERT và RoBERTa cùng với các kết quả bổ sung cho Decoder-only và Encoder-Decoder như BART, ELECTRA và GPT2, nhóm đề xuất một phương pháp để chứng minh luận điểm này. Ngoài ra, phương pháp này còn có thể được sử dụng như một công cụ nhanh chóng và hiệu quả để đánh giá độ bền vững của các mô hình Transformer.",
        "Bài báo giới thiệu SRank, một phương pháp xếp hạng mới dành cho việc lựa chọn các giải pháp code tốt nhất từ các Mô hình Ngôn ngữ Lớn về Code (CodeLLMs). SRank sử dụng phân tích mối quan hệ và sự tương đồng chức năng giữa các cụm giải pháp code để cải thiện quá trình xếp hạng. Kết quả nghiên cứu cho thấy SRank đạt được kết quả xuất sắc với điểm pass@1 trên nhiều tiêu chuẩn, vượt trội hơn so với các phương pháp hiện tại với mức trung bình là 6,1%.",
        "là tổ chức tồn tại đến nay, cải cách hành chính và chống tham nhũng",
        "ông được tổ chức cử về nước, cùng với một số đồng chí của ông, để tuyên truyền tư tưởng cách mạng cho thanh niên ở thanh hóa",
        "lão kể có hôm lão đến một thị trấn chơi, có lão họ lý chơi thua nhiều quá, nên gã đem đồ ký gửi ra mà cược lấy mấy chiếc rương to, khi mở ra toàn vàng ròng",
        "Ba chị em bây hãy dấu mình yêu quái,  trà trộn vào cung điện,  làm cho Trụ vương điêu đứng, đợi cho võ vương đánh trụ thành công, ta cho chúng bay thành thần",
        "Nếu ta không báo ứng cho hắn sao gọi là linh, nói rồi liền đằng vân bay vào triều, cố vật chết vua Trụ để rửa hờn"
         
         ]

if __name__ == '__main__':
    for text in arrtext:
        # args
        parser = argparse.ArgumentParser()
        parser.add_argument("--config", default="/home/thhiep/mayt4/text-to-speech/logs/nam_mienbac_doctruyen/config.json")
        parser.add_argument("--model", default="/home/thhiep/mayt4/text-to-speech/logs/nam_mienbac_doctruyen/G_50000.pth")
        parser.add_argument("--text", default=text)
        parser.add_argument("--is_character", action="store_true")
        args = parser.parse_args()
        
        # load model
        hps = utils.get_hparams_from_file(args.config)
        print(args.is_character)

        # net_g = SynthesizerTrn(
        #     len(symbols),
        #     hps.data.filter_length // 2 + 1,
        #     hps.train.segment_size // hps.data.hop_length,
        #     **hps.model).to("cpu")
        # _ = net_g.eval()

        # _ = utils.load_checkpoint(args.model, net_g, None)


        if(args.is_character):##### do nothing
            lensymbols=len(symbolscharacter)
            args.text=norm_text_extend(args.text)
            print("text đưa vào model", args.text) ##### bỏ async
        if(not args.is_character):#####store_true
            lensymbols=len(symbols)
            ###feature is disable
            args.text=convert_rawtext_to_phoneme(args.text)
            print("text đưa vào model", args.text)
        
        net_g = SynthesizerTrn(
            lensymbols,
            hps.data.filter_length // 2 + 1,
            hps.train.segment_size // hps.data.hop_length,
            **hps.model).to("cpu")
        _ = net_g.eval()

        _ = utils.load_checkpoint(args.model, net_g, None)
            
        
        stn_tst = get_text(args.text,args.is_character,  hps)
        with torch.no_grad():
            x_tst = stn_tst.to("cpu").unsqueeze(0)
            
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to("cpu")
            start = time.time()
            audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1.1)[0][0,0].data.cpu().float().numpy()
            
            end = time.time()

        date = datetime.now().strftime("%Y-%m-%d_%I-%M-%S")
        
        # Increase volume
        audio = np.int16(audio * MAX_INT)
        mean_volume_db = 20 * np.log10(np.abs(audio).mean() / MAX_INT)
        # print(f"Mean volume before: {mean_volume_db} dB, {np.abs(audio).mean()}")

        # Tăng volume theo giá trị db muốn đạt được
        target_volume_db = -25
        gain = 10 ** ((target_volume_db - mean_volume_db) / 20)
        # print(f"Audio gain: {gain}")
        if gain >= 1.0:
            audio_gain = audio * np.int16(gain)
            mean_volume_db = 20 * np.log10(np.abs(audio_gain).mean() / MAX_INT)
            if not mean_volume_db == -np.inf:
                print(f"Mean volume after: {mean_volume_db} dB, {np.abs(audio_gain).mean()}, {gain}")
                audio = audio_gain
            # else:
        write(f'/home/thhiep/mayt4/text-to-speech/infer_final/{date}.wav', hps.data.sampling_rate, audio)
        print(f'{date}.wav')
        import time
        time.sleep(1)
