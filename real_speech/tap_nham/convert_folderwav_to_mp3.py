# from pydub import AudioSegment
# import glob
# import soundfile as sf
# import librosa

# old_path="/home/thhiep/ttsopenai_vietnam"
# def audiosegment_load_audio(path):
#     if('mp3' in path):
#         return AudioSegment.from_mp3(path)
#     if('wav'in path):
#         return AudioSegment.from_wav(path)
# def convert_wav(path):
    
#     audio=audiosegment_load_audio(path)
#     new_path=path.replace("mp3","wav").replace("ttsopenai_vietnam","ttsopenai_audio_wav")
#     sf.write(new_path, data = audio.get_array_of_samples(), format = 'wav',samplerate =24000*1, subtype='PCM_16')
#     x, s = librosa.load(new_path, sr=24000*1)
#     y = librosa.resample(x, 24000*1, 16000)
#     # librosa.output.write_wav("Test3.wav", y, sr=16000, norm=False)
    
#     # audio=audiosegment_load_audio(new_path)
#     sf.write(new_path, data = y, format = 'wav',samplerate =16000, subtype='PCM_16')
    
    

# audio_files = glob.glob(f'{old_path}/*')#####/**/*
# for audio_file in audio_files:
#     if audio_file.endswith(".mp3"):
#         convert_wav(audio_file)
        
        
# # from pydub import AudioSegment
# # import glob

# # old_path="/home/thhiep/audio_1"
# # def convert_mp3(path):
# #     audio = AudioSegment.from_file(path)
# #     audio = audio.set_frame_rate(44100)
# #     audio.export(path.replace("wav","mp3").replace("audio_1","audio_mp3"), format="mp3")

# # audio_files = glob.glob(f'{old_path}/*')#####/**/*
# # for audio_file in audio_files:
# #     if audio_file.endswith(".wav"):
# #         convert_mp3(audio_file)



from pydub import AudioSegment
import glob
import soundfile as sf
import librosa
old_path="/home/thhiep/oov_openai_numienbac32"
newpath="/home/thhiep/oov_openai_numienbac"
audio_files = glob.glob(f'{old_path}/*')

def audiosegment_load_audio(path):
    if('mp3' in path):
        return AudioSegment.from_mp3(path)
    if('wav'in path):
        return AudioSegment.from_wav(path)
    
for audio_file_path in audio_files:
    TARGET_DB=-23.40152408801259
    audio=audiosegment_load_audio(audio_file_path)
    audio=audio.apply_gain(TARGET_DB-audio.dBFS)
    sf.write(newpath+'/'+audio_file_path.split('/')[-1], data = audio.get_array_of_samples(), format = 'wav',samplerate =16000, subtype='PCM_16')
