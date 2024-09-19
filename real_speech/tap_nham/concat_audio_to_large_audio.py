import os
import argparse
from tqdm import tqdm
from lib.preprocess_utils.utils import pairing
from collections import defaultdict
import soundfile as sf
# newdict = defaultdict(dict)#####{} chả khác mấy, nếu ko có trong k thì khởi tạo list rỗng

from pydub import AudioSegment
def con_cat_list_audio(list):
    
    for i, wav_file in enumerate( list):
        if(i==0):
            audio_concat = AudioSegment.from_file(str(wav_file))
        else:
            audio = AudioSegment.from_file(wav_file)
            audio_concat = audio_concat  + audio
    return audio_concat
    
# append_dict={}
def concat_audio_with_sort(args):
    newdict = defaultdict(list)
    for k, v in tqdm(paired_files.items()):#####'122/streaming/segments/1698542873_HT 091123_1_0001'#'121/streaming/1698552590_HT 091123_1' , {'audio': '121/streaming/1698552590_HT 091123_1.wav'}
        if ('/streaming/segments/'in k):
            if('81/streaming/segments/' in k):
                ksplit=k.split('/')
                folderid=ksplit[0]
                tail_file=ksplit[-1].split(" ")[-1]
                input_audio_path = os.path.join(args.input_path, v["audio"])
                newdict[folderid].append((tail_file, input_audio_path ))
            else:
                ksplit=k.split('/')
                folderid=ksplit[0]
                tail_file=ksplit[-1].split(" ")[-1]
                input_audio_path = os.path.join(args.input_path, v["audio"])
                newdict[folderid].append((tail_file, input_audio_path ))
                
    for k, v in tqdm(newdict.items()):#####('091123_15_0019', '/home/thhiep/HNCL/meetings_16k/81/streaming/segments/1698501534_HT 091123_15_0019.wav')
        newdict[k].sort(key=lambda a: a[0])
        list_audio=[path[1] for path in newdict[k]]
        audio_concated=con_cat_list_audio(list_audio)
        new_path='/home/thhiep/HNCL/meetings_16k/'+str(k)+'/'+str(k)+".wav"
        # audio_concated.export(new_path)
        sf.write(new_path, data = audio_concated.get_array_of_samples(), format = 'wav',samplerate =16000, subtype='PCM_16')
        
        
    newdict=newdict
        # input_audio_path = os.path.join(args.input_path, v["audio"])
        # output_audio_path = os.path.join(args.output_path, v["audio"])
        # output_dir = os.path.dirname(output_audio_path)
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)
        # command = f"ffmpeg -v quiet -i '{input_audio_path}' -ar 16000 -ac 1 -resampler soxr '{output_audio_path}'"
        # exit_code = os.system(command)
        # if exit_code != 0:
        #     print(exit_code)
        #     raise Exception
    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", default="/home/thhiep/HNCL/meetings_16k")
    parser.add_argument("--output_path", default="/home/thhiep/HNCL/meetings_16k")
    args = parser.parse_args()
    global paired_files
    paired_files = pairing(args.input_path, relative=True)
    concat_audio_with_sort(args)


if __name__ == "__main__":
    main()
