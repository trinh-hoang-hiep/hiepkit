import random
import json
import os
import time
from tqdm import tqdm
import csv
import numpy as np
import soundfile as sf

from pydub import AudioSegment
with open("/home/thhiep/vov_ngoc_anh_short_none_concat.csv",encoding='utf8') as f:
    csv_reader = csv.reader(f,delimiter=',')
    header = next(csv_reader)
    data = [{'audio_filepath':line[0],'text':line[1]} for line in csv_reader]#####

print('Length data:', len(data))
#####
with open('vov_ngoc_anh_short_none_concat2.csv', 'w', encoding='utf-8') as f:
    new_row_short=[]
    for dat in data:
        # f.write(json.dumps(doc, ensure_ascii=False)+'\n')
        old_filepath=dat['audio_filepath'].replace('E:\\Text_to_speech\\text_to_speech_dataset\\vov_ngoc_anh\\vov_ngoc_anh_labeled\\','/home/thhiep/vov_ngoc_anh_labeled/').split('/')
        filename=old_filepath[-1]
        newpath='/home/thhiep/hiep_audio_ngoc_anh_short/'+filename
        folder, file=filename.split("_audio_")
        indexfolder=folder.split("FILE")[-1]
        indexfile=file.split("_16k.wav")[0]
        file="audio_"+file
        
        # dest = shutil.copyfile(doc['audio_filepath'].replace('E:\\Text_to_speech\\text_to_speech_dataset\\vov_ngoc_anh\\vov_ngoc_anh_labeled\\','/home/thhiep/vov_ngoc_anh_labeled/'), newpath)#####
        # audio=AudioSegment.from_wav('/home/thhiep/vov_ngoc_anh_labeled/FILE'+indexfolder+'/File'+indexfolder+'_split_'+indexfile+'/audio_'+indexfile+'.wav')
        # print('/home/thhiep/vov_ngoc_anh_labeled/FILE'+indexfolder+'/File'+indexfolder+'_split_'+indexfile+'/audio_'+indexfile+'.wav')
        audio=AudioSegment.from_wav('/home/thhiep/vov_ngoc_anh_labeled/'+folder+'/'+file)
        
        sf.write(newpath, data = audio.get_array_of_samples(), format = 'wav',samplerate =16000, subtype='PCM_16')
        print('/home/thhiep/vov_ngoc_anh_labeled/'+folder+'/'+file)
        new_row_short.append([newpath,dat['text']])
        # if(len(dat['text'].split(' '))>5):#####
        #     new_row_short.append([newpath,dat['text']])
    # print("so video ngan bi loai bo", len(index_of_short_data) - len(new_row_short))
    writer = csv.writer(f)#####
    writer.writerow(['audio_path', 'text_add_equal'])
    writer.writerows(new_row_short)

os.system('wc -l vov_ngoc_anh_short_none_concat2.csv')