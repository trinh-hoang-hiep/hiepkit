# import json
# import matplotlib.pyplot as plt
# with open("/home/thhiep/data_raw_nam_mienbac/TTSData/label_fixed/ptv_pham_nguyen_son_tung_dot_2.json", encoding='utf-8') as f:
#     txt=f.read()
#     arrdictionary=json.loads(txt)

# time_intervals=[]

# for row in arrdictionary:
#     if("quang_cao" not in row["original_filename"]):
#         for audio in row["segmentations"]:
#             start=audio["start_time"]
#             end=audio["end_time"]
#             time_intervals.append((start, end))

# time_durations=[]
# for interval in time_intervals:
#     time_durations.append(interval[1]-interval[0])


import librosa
import soundfile as sf
import glob
from pydub import AudioSegment
import matplotlib.pyplot as plt


def audiosegment_load_audio(path):
    if('mp3' in path):
        return AudioSegment.from_mp3(path)
    if('wav'in path):
        return AudioSegment.from_wav(path)


# path="/home/thhiep/data_raw_nam_mienbac/TTSData/prealign/25.TTS_pham_nguyen_son_tung_dot_2"
# filenames  = glob.glob(f'{path}/**/**/*.wav')#####/**/*
filenames=[]
all_lines=[]
with open("/home/thhiep/data_raw_nam_mienbac/total_file_doc_truyen_1to6s_fine_grain.txt", "r") as f:
    for line in f:
        all_lines.append(line)
        filenames.append(line.split("|")[0])
        

total_time=[]
time_durations=[]
count4_5=0
for filename in filenames:
    print(filename)
    # y, sr = librosa.core.load(filename, sr=16000, mono=True) # 16000Hz
    # sf.write(filename, y, sr, subtype="PCM_16") #16b
    # dur=librosa.get_duration(y=y, sr=sr)
    if("quang_cao" not in filename):
        audio=audiosegment_load_audio(filename)
        dur=audio.duration_seconds
        # if (dur>=4)and(dur<=5):
        #     count4_5+=1
        total_time.append(dur)
        time_durations.append(dur)
print(sum(total_time))
# print(count4_5)#####4625


# bins = [0,10,20,30,40,50]
bins=list(range(0,10,1))

plt.hist(time_durations, bins, histtype='bar', rwidth=0.8)

plt.xlabel('thoigian')
plt.ylabel('so_luong_audio')
plt.title('Thong ke thoi gian data doctruyen ')
# plt.legend()
# plt.show()
plt.savefig('foo.png')

# num_bin=[0]*10

# import numpy as np
# mean=5
# variance=1.9*1.9 ######https://homepage.divms.uiowa.edu/~mbognar/applets/normal.html thì sẽ từ 0-10
# def pdf(x):
#     return 1/(np.sqrt(2*np.pi*variance))*np.exp(-(x-mean)**2/(2*variance))


# num_bin_pdf=[]
# for i in range(0,10):
#     num_bin_pdf.append(4625/pdf(4.5)*pdf(i+0.5))
    
    
# fine_grain_file=[]
# for dur,line in zip(time_durations,all_lines):
#     num_bin[int(dur)]+=1
#     if(num_bin[int(dur)]<=num_bin_pdf[int(dur)]) and ("TIN TUC" not in line):
#         fine_grain_file.append(line)

# with open("/home/thhiep/data_raw_nam_mienbac/total_file_doc_truyen_1to6s_fine_grain.txt", "w") as f:
#     for line in fine_grain_file:
#         f.write(line)