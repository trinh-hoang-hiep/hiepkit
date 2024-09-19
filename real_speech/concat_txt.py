import glob
data_dir='/home/thhiep/HNCL/split_audio_normfile'
txt_files = glob.glob(f'{data_dir}/**/*.txt')#####txt')
# txt_files.sort()
txt_files = sorted(txt_files, key=lambda x: "{:06d}_".format(int(x.split('/')[-2]))+x.split('/')[-1])
total_txt=[]
for txt_file in txt_files:
    with open(txt_file, mode='r', encoding="utf8") as f:
        f = open(txt_file)
        total_txt.append(txt_file+'|'+f.read()+'\n')


with open ("/home/thhiep/HNCL/total_txt_file.txt", mode='w', encoding='utf-8') as f:
    for line in total_txt:
        f.write(line)    