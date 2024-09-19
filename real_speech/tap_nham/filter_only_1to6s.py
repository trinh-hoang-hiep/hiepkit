import librosa
import soundfile as sf
import glob
from pydub import AudioSegment
from tests.nguyenlm_text_normalization import norm_text_extend


def audiosegment_load_audio(path):
    if('mp3' in path):
        return AudioSegment.from_mp3(path)
    if('wav'in path):
        return AudioSegment.from_wav(path)


path="/home/thhiep/data_raw_nam_mienbac/file_force_align_doctruyen.txt"
total_line=[]
with open (path, mode='r', encoding='utf-8') as f:
    lines=f.readlines()
    for lin in lines:
        if ("quang_cao" not in lin):
            filename=lin.split("|")[0]
            text=lin.split("|")[1]
            total_line.append((filename, text))

filter_durations=[]
for (filename, text) in total_line:
    print(filename)
    # y, sr = librosa.core.load(filename, sr=16000, mono=True) # 16000Hz
    # sf.write(filename, y, sr, subtype="PCM_16") #16b
    # dur=librosa.get_duration(y=y, sr=sr)
    
    text=norm_text_extend(text)
    # text = re.sub("=+", "=", text).strip()
    # text = text[1:] if text[0] == "=" else text
    text = text[1:] if text[0] == "-" else text
    text=text.strip()+"\n"
    if("quang_cao" not in filename):
        audio=audiosegment_load_audio(filename)
        dur=audio.duration_seconds
        if (dur>=0.5)and(dur<=9.5):
            filter_durations.append(filename+"|"+text)

with open ("/home/thhiep/data_raw_nam_mienbac/total_file_doc_truyen_1to6s.txt", mode='w', encoding='utf-8') as f:
    for line in filter_durations:
        f.write(line)
