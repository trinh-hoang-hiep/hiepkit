import re
import os
import json
import string
import random
import argparse
import soundfile as sf
from collections import defaultdict
import sys 
sys.path.append('/home/thhiep/data_raw_nam_mienbac/')
from lib.preprocess_utils.text_processing.libs.text_preprocess.preprocessing import clean_text, run_strip_accents
from tqdm import tqdm
from normalize_input.normalize import normalize_input_text_to_speech

random.seed(12345)

LABELED_DATA = "/home/thhiep/HNCL.json"
RAW_DATA = "/home/thhiep/HNCL/meetings_16k"
OUTPUT_DIR = "/home/thhiep/HNCL/split_audio_normfile"


punc_pattern = re.compile(r"[{}]".format(re.escape(string.punctuation)))


def remove_punc(text):
    text = punc_pattern.sub(" ", text)
    text = re.sub(" {2,}", " ", text)
    return text.strip()


def pipeline(text):
    text = text.lower()
    text = clean_text(text, replace_newline=True)
    text = remove_punc(text)
    text=normalize_input_text_to_speech(text)#####################
    final_text = re.sub("=+", "=", text).strip()
    final_text = final_text[1:] if final_text[0] == "=" else final_text
    return final_text.strip()


def get_key_func(key):
    ns = []
    matches = re.finditer(r"\d+", key)
    for m in matches:
        ns.append(int(m.group()))
    return ns


def compare_func(a, b):
    a = get_key_func(a)
    b = get_key_func(b)
    L = max(len(a), len(b))
    for i, j in zip(a, b):
        if i < j:
            return -1
        if i > j:
            return 1
    if len(a) < len(b):
        return -1
    if len(a) > len(b):
        return 1
    return 0


def cut_audio(input, start, end, save_path):
    if isinstance(input, str):
        speech_array, sampling_rate = sf.read(input)
    else:
        speech_array, sampling_rate = input
    start_cut = int(float(start) * sampling_rate)
    end_cut = int(float(end) * sampling_rate)
    cut_audio = speech_array[start_cut : end_cut]
    sf.write(save_path, cut_audio, sampling_rate)


def get_name_in_json_labels(file_name):
    file_name = run_strip_accents(file_name.replace(" ", "_"))
    file_name = re.sub(r"[Đđ()]", "", file_name)
    return file_name


def separate_file(input_file, output_dir, file_name, segmentations, augment: bool = True):
    if augment is False:
        raise Exception("Not implemented")
    else:
        separate_file_augmented(input_file, output_dir, file_name, segmentations)


def separate_file_augmented(input_file, output_dir, file_name, segmentations):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    f_noext, ext = os.path.splitext(file_name)

    adj = defaultdict(list)
    # for i, segment in enumerate(segmentations):
    #     adj[i].append(i)
    #     j = i + 1
    #     while j < len(segmentations):
    #         force_unmerge = segmentations[j].get("not_merge")
    #         if force_unmerge:
    #             break
    #         delta = segmentations[j]["end_time"] - segment["start_time"]
    #         if delta > 20:
    #             break
    #         if delta >= 2:
    #             adj[i].append(j)
    #         j += 1

    # i = 0
    # count = 0
    # speech_array, sampling_rate = sf.read(input_file)
    # while i < len(segmentations):
    #     if len(adj[i]) <= 1:
    #         i += 1
    #         continue
    #     picked_j = random.choice(adj[i][1:])

    #     # merge text
    #     contents = []
    #     for k in range(i, picked_j + 1):
    #         segment = segmentations[k]
    #         if segment["transcription"]:
    #             content = pipeline(segment["transcription"])
    #             contents.append(content)
    #     merged_content = " ".join(contents)

    #     # merge audio
    #     start = segmentations[i]["start_time"]
    #     end = segmentations[picked_j]["end_time"]
    
    count=0
    speech_array, sampling_rate = sf.read(input_file)
    for i, segment in enumerate(segmentations):
        merged_content=pipeline(segment["transcription"])
        
        start=segmentations[i]["start_time"]
        if (start > 0.05):
            start=start-0.05
        end = segmentations[i]["end_time"]+0.05

        
        save_path = os.path.join(output_dir, "{}_{:06d}{}".format(f_noext, count, ext))
        save_path_txt = os.path.join(output_dir, "{}_{:06d}{}".format(f_noext, count, ".txt"))
        count += 1
        cut_audio(input=[speech_array, sampling_rate], start=start, end=end, save_path=save_path)
        with open(save_path_txt, "w") as writer:
            writer.write(merged_content)
        # i = picked_j + 1


def list_files(input_path, relative=True, ignore_pattern=None):
    stack = [input_path]
    ret = []
    ignore_patterns = None
    if ignore_pattern:
        ignore_patterns = ignore_pattern.split(",")
    while stack:
        node = stack.pop()
        files = os.listdir(node)
        paths = [os.path.join(node, f) for f in files]
        for f in paths:
            if ignore_patterns:
                ignore = False
                for patt in ignore_patterns:
                    if patt in f:
                        ignore = True
                        break
                if ignore:
                    continue
            if os.path.isdir(f):
                stack.append(f)
            elif os.path.isfile(f):
                if relative:
                    ret.append(os.path.relpath(f, input_path))
                else:
                    ret.append(f)
    return ret


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_data", "-r", default=RAW_DATA)
    parser.add_argument("--output_dir", "-o", default=OUTPUT_DIR)
    parser.add_argument("--label_data", "-l", default=LABELED_DATA)
    global args

    args = parser.parse_args()
    run()


def run():
    files = list_files(input_path=args.raw_data, relative=True)
    files = [f for f in files if f.endswith(".wav") or f.endswith(".mp3")]

    # print(len(files))
    # tracker = defaultdict(list)
    # check_names = []
    # for f in files:
        # _f = f
        # f = os.path.basename(f)
        # check_names.append(get_name_in_json_labels(f))
        # tracker[check_names[-1]].append(_f)

    with open(args.label_data, "r") as reader:
        labels = json.load(reader)
    # print(len(labels))

    global dict_labels
    dict_labels = {}
    for item in labels:
        dict_labels[item["original_filename"]] = item

    # check_labels = list(dict_labels.keys())

    for f in tqdm(files):
        # print("file là", f)
        if( f.split("/")[0] in ["81","122","123","121","140","124","147","157","149","150","151","152"]):
            f_dirname = os.path.dirname(f)
            f_path = os.path.join(args.raw_data, f)
            f_basename = os.path.basename(f)
            f_basename = get_name_in_json_labels(f_basename)
            try:
                item = dict_labels[f_basename]
            except Exception as e:
                continue
            separate_file(input_file=f_path, output_dir=os.path.join(args.output_dir, f_dirname), file_name=f_basename, segmentations=item["segmentations"], augment=True)


if __name__ == "__main__":
    main()
