import os
from typing import Text, Tuple, Any
import sys
sys.path.append('/home/thhiep/tts_tien_xu_ly/text-to-speech')
# sys.path.insert(1, '/home/thhiep/tts_tien_xu_ly/text-to-speech/normalize_input')
from normalize_input.vietnam_number_custom import n2w, n2w_single
import re
import unicodedata
# import numpy as np
import random
from normalize_input.word_to_phoneme import *
import traceback


def replace_punctuation_to_silence_voice(input: Text) -> Text:
    return


def normalize_sentence(sentence: Text) -> Text:
    sentence = str(sentence)
    sentence = " ".join(sentence.split())
    sentence = unicodedata.normalize("NFKC", sentence)
    sentence = sentence.replace("–", "-").replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
    # Chuẩn hóa việc không được có space sau và trước mở đóng ngoặc đơn và có space trước các dấu câu đặc biệt (VD:( 2140m2 ) => (2140m2) )
    sentence = re.sub(r'(?<=[\(\'])\s|\s(?=[\)\'])|\s(?=[.,!?])', '', sentence)
    return sentence


def remove_punctuation(word: Text) -> Text:
    # number: 1,2 1.2 45,34 213.123.12321 12312,123.123 123.545,12312
    number_pattern = r"[\(]{0,1}[0-9]{1,}[aA-zZ]{0,}([\.,\\/-][0-9]{1,}){1,}[\)]{0,1}"
    if re.search(number_pattern, word) or '@' in word:
        return word

    word = re.sub("[\"\'\[\]\(\)~\*#\|\\\/_\^\-]", " = ", word)
    word = re.sub("[;,:]", " = ", word)
    # word = re.sub("[\.?!]", " = ", word)  # dấu chấm ngắt dài hơn########################
    word = re.sub("[\?!]", " = ", word)  # dấu chấm ngắt dài hơn
    word = re.sub("\.", " chấm ", word)
    return word


def remove_last_punctuation_in_word(word: Text) -> Tuple[Text, Any, Any]:
    add_silence_last_word = False
    add_silence_first_word = False

    def recursive_remove_first_last(word: Text, add_silence_last_word=False, add_silence_first_word=False,
                                    is_first_loop: bool = False):
        is_next_loop = False
        if len(word) > 0:
            if word[0] in ['(', '[']:
                word = word[1:]
                is_next_loop = True
                if is_first_loop:
                    add_silence_first_word = True
            if word[-1] in [',', ';', '.', '\'', '\"', ')', ']']:
                word = word[:-1]
                is_next_loop = True
                if is_first_loop:
                    add_silence_last_word = True

            if is_next_loop:
                word, add_silence_last_word, add_silence_first_word = recursive_remove_first_last(word,
                                                                                                  add_silence_last_word,
                                                                                                  add_silence_first_word,
                                                                                                  is_first_loop=False)

        return word, add_silence_last_word, add_silence_first_word

    return recursive_remove_first_last(word, add_silence_last_word, add_silence_first_word, is_first_loop=True)


def convert_measurand(measurand: Text) -> Text:
    data_convert_measurand = {
        'mm': 'mi li mét',
        'cm': 'xăng ti mét',
        'dm': 'đề xi mét',
        'm': 'mét',
        'km': 'ki lô mét',
        'nm': 'na nô mét',
        'g': 'gam',
        'kg': 'ki lô gam',
        'mg': 'mi li gam',
        'gr': 'gam'
    }
    if measurand in data_convert_measurand.keys():
        return data_convert_measurand[measurand]
    else:
        return measurand


def convert_special_symbol_to_text(text, last_num, previous_word, next_word, org_word):
    # print(text, last_num)
    if text == 'h':
        list_time_word = ['lúc', 'khi', 'điểm', 'tại', 'vào', 'ngay', 'đến', 'trước', 'sau', 'khắc', 'giữa', 'trưa',
                          'sáng', 'tối', 'đêm', 'buổi', 'sớm', 'muộn', 'từ', 'mưa', 'nắng', 'gió', 'bão', 'khoảng',
                          'chừng',
                          'ngay', 'chớm', 'khuya', 'hồi', 'khắc', 'điểm']
        if previous_word.lower() in list_time_word or next_word.lower() in list_time_word or org_word[-1] == "h":
            text = 'giờ'
        else:
            text = 'hát'
    elif text == '%':
        text = 'phần trăm'
    elif text == 'ha' and last_num == '':
        text = 'hecta'
    elif text.find('m') > -1 or text.find('g') > -1:
        # 12m2, 53m3, 40cm2, 10m, 40g, 100kg(Trường hợp: Số + đại lượng vật lý kết thúc bởi số như m2, m3)
        text = convert_measurand(text)
        if last_num != '':
            if last_num == '2':
                last_num = "vuông"
            elif last_num == '3':
                last_num = "khối"
            else:
                last_num = convert_number_to_text(last_num)
    elif text in asr_phoneme_letter_dict.keys():
        text = asr_phoneme_letter_dict[text]
    elif org_word.isupper():
        start_idx = org_word.lower().find(text)
        text = convert_upper_word_to_text(org_word[start_idx:start_idx + len(text)])

    if last_num.isdigit():
        last_num = convert_number_to_text(last_num)

    return text, last_num


def convert_number_to_text(s: Text) -> Text:
    # if random.random() < 0.5:
    return n2w(s)


def reformat_num_string(word, org_word, list_words, idx):
    # Dạng số hỗn hợp kèm dấu ., VD: 1.999.530 94,36 0.29% 1.751,6 1,232,123.4
    groups = re.search(r'([0-9]{1,})([\.,][0-9]{1,}){1,}(.*)', word)
    # print(word, groups)
    if groups is not None:
        first_group_match = groups.group(1)
        last_group_match = groups.group(2)

        list_punc = [',', '.']
        punc_in_unit = last_group_match[0]  # dấu . hay dấu , ở đơn vị cuối cùng

        if not any(x in [',', '.'] for x in word.replace(last_group_match, '')):
            # print(word, last_group_match, len(last_group_match))
            if int(last_group_match[1:]) == 0 and len(last_group_match) == 4:
                # Không phải sổ thập phân, 100.000 và không để nhầm trường hợp 15.0%, 90000d
                num = (first_group_match + last_group_match).replace(punc_in_unit, '')
                # print(num, last_group_match)
                tmp_text = n2w(num)
            elif word[0] == '0' and (word.count('.') > 1 or word.count(',') > 1):
                # Số điện thoại 016.56.56
                num = word.replace(punc_in_unit, '')
                tmp_text = n2w_single(num)
            else:
                # là số thập phân 23.5 56,4 => Gặp lỗi trường hợp f/2.4
                if word[0] in ['\'', '(', '"'] and word[-1] in ['\'', ')', '"']:
                    word = word[1:-1]
                    # last_group_match = last_group_match[:-1]
                    # print(last_group_match)

                before_punc = word[:word.index(punc_in_unit)]
                after_punc = last_group_match[1:]

                if len(after_punc) == 3:
                    # Sẽ có trường hợp là số hàng nghìn cách nhau dấu phẩy: 1.073 3.085 => Set length after punc và random
                    tmp_text = n2w(before_punc + after_punc)
                else:
                    before_punc = n2w(before_punc)
                    after_punc = convert_number_to_text(after_punc)
                    punc_str = ' phẩy '
                    tmp_text = before_punc + punc_str + after_punc

        else:
            # Số có 2 dấu trở lên
            if word.replace(last_group_match, '').find(punc_in_unit) > -1:
                # print("in here: ", word, word.replace(punc_in_unit, ''))
                is_alpha = False
                for char in word:
                    if char.isalpha():
                        is_alpha = True
                        break
                if is_alpha:
                    # print("in here: ", word)
                    subwords = word.split(punc_in_unit)
                    tmp_text = ''
                    for w in subwords:
                        tmp_text += ' ' + (
                            convert_number_to_text(w) if w.isdigit() else asr_phoneme_letter_dict[w])
                else:
                    # print("in here: ", word, word.replace(punc_in_unit, ''))
                    tmp_text = convert_number_to_text(word.replace(punc_in_unit, ''))
            else:
                # Có 2 loại dấu: 1.751,6
                list_punc.remove(punc_in_unit)
                before_punc = n2w(word[:word.index(punc_in_unit)].replace(list_punc[0], ''))
                after_punc = convert_number_to_text(last_group_match[1:])
                punc_str = ' phẩy '
                tmp_text = before_punc + punc_str + after_punc

        tmp_text = tmp_text + ' phần trăm' if '%' in word else tmp_text

        last_special_symbol = re.sub('[,;\.%]', '', groups.group(3))  # 100.3m2, 45.6r65 90.000đ/ dấu

        if last_special_symbol != '':
            sub_groups = re.search(r'([a-zA-Z]{1,})([0-9]{0,})', last_special_symbol)
            if sub_groups:
                text, last_num = sub_groups.group(1), sub_groups.group(2)
                text, last_num = convert_special_symbol_to_text(text=text, last_num=last_num,
                                                                previous_word=list_words[idx - 1],
                                                                next_word=list_words[idx + 1 if idx + 1 < len(
                                                                    list_words) else idx - 1],
                                                                org_word=org_word)

                tmp_text = tmp_text + ' ' + text + ' ' + last_num
            else:
                tmp_text = tmp_text + ' ' + last_special_symbol
    else:
        tmp_text = convert_number_to_text(word)
    return tmp_text


def split_num_and_word(word: Text, list_words, idx, org_word) -> Text:
    # 15h30, xăng A92, boeing 727B, 565ha, tiểu lộ 523B, xăng A95, lớp 12A3, 12m2, 53m3, QL7A
    groups = re.search(r'^([0-9]{0,})([a-zA-Z\\/]{1,})([0-9]{0,})([a-zA-Z\\/]{0,})', word)
    # print(word, groups)
    if groups is not None:
        first_num = n2w(groups.group(1)) if groups.group(1) != '' else ''

        center_text = groups.group(2)
        last_num = groups.group(3) if groups.group(3) != '' else ''
        last_text = groups.group(4) if groups.group(4) != '' else ''

        center_text, last_num = convert_special_symbol_to_text(center_text, last_num,
                                                               previous_word=list_words[idx - 1],
                                                               next_word=list_words[idx + 1 if idx + 1 < len(list_words)
                                                               else idx - 1],
                                                               org_word=org_word)
        if first_num == '' and last_num == '':
            tmp_text = word
        else:
            tmp_text = first_num + ' ' + center_text + ' ' + last_num + ' ' + last_text
    else:
        # Only number
        tmp_text = reformat_num_string(word, org_word, list_words, idx)

    return tmp_text


def convert_upper_word_to_text(org_word, lang="en", add_silent=False):
    tmp_text = ''
    silent = ' = ' if add_silent else ' '
    letter_dict = asr_phoneme_letter_dict if lang == "vi" else asr_phoneme_eng_letter_dict
    for idx in range(len(org_word)):
        char = org_word[idx]
        if char.lower() in letter_dict.keys():
            tmp_text += letter_dict[char.lower()] + silent
        else:
            tmp_text += char + silent
    return tmp_text

def remove_punctuation_sentence(sentence: Text) -> Text:######################
    sentence = re.sub("\.(?= )", " = ", sentence)
    sentence = re.sub("\.$", "", sentence)
    return sentence
async def normalize_input_text_to_speech(input: Text, add_last_break: bool) -> Text:
    input=input.replace('@', ' a còng ')
    normalized_text = normalize_sentence(input)
    normalized_text=remove_punctuation_sentence(normalized_text)######################
    process_sent = re.sub("\s\s+", " ", " ".join(remove_punctuation(word) for word in normalized_text.split()))

    # lower tất cả text, bỏ space và thêm silence đầu và cuối câu
    # normalized_text = '= ' + normalized_text.lower().strip() + ' ='

    # Chuẩn hóa cách đọc số
    # Đọc đơn vị toán học: Số + (space) + (Ký tự đặc biệt: %, ha, cm, dm, m, kg, mg, ...)
    # Đọc giờ
    # Đọc nhiệt độ
    # convert cách đọc các từ tiếng anh phổ thông
    final_words = []
    list_words = process_sent.strip().split(' ')
    for idx, org_word in enumerate(list_words):
        try:
            # Xác định có phải là dạng 4.0 32,5 hay số âm không
            word, add_silence_last_word, add_silence_first_word = remove_last_punctuation_in_word(org_word.lower())
            if add_silence_first_word and idx != 0:
                final_words.append(' = ')
            tmp_text = word
            if word in common_conjunction.keys():
                print("Case 1")
                tmp_text = common_conjunction[word]
                final_words.append(tmp_text)
            elif re.search(r"([\w\.-]+)@([\w\.-]+)\.([\w\.]+)$", word):
                # email
                # Tách thành phần người dùng và phần còn lại
                print("Case 2")
                username, domain = word.split("@")

                # Tách thành phần tên miền và phần mở rộng
                domain_part = domain.split(".")
                domain_text = ''
                for j_part, part in enumerate(domain_part):
                    if part in common_email.keys():
                        part = common_email[part]
                    else:
                        part = convert_upper_word_to_text(part, add_silent=True)
                    domain_text += part
                    if j_part < len(domain_part) - 1:
                        domain_text += '-chấm '
                        #####################domain_text += ' = chấm '
                        

                tmp_text = convert_upper_word_to_text(username, add_silent=True) + ' = ' + 'a còng ' + domain_text
                final_words.append(tmp_text)

            #### Bo sung case doc dia chi IP
            elif re.search(r"(\d{3}[\s.-])(\d{3}[\s.-])(\d{1,3}[\s.-])\d{1,3}$",word):
                word = word.replace('-', '').replace('+', '')
                
                parts = word.split(".")
                for j, part in enumerate(parts):
                    tmp_text = ''
                    for idx_phone in range(len(part)):
                        # silent = ' ' if (idx_phone + 1) % stack_phone else ' = '
                        silent = ' = '
                        tmp_text += n2w(part[idx_phone]) + silent
                    if j < len(parts) - 1:
                        tmp_text += ' chấm '
                    final_words.append(tmp_text)

            #### Bo sung case doc so tai khoan ngan hang
            ## Có các case số tài khoản có 9,10,11,12,13,14,15 số
            ### TO DO
            elif re.search(r"^(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}$", word):
                print("Case 3")
                # Phone number: "+8433822315", "033.822.1235", "+123456789"
                # tmp_text = convert_upper_word_to_text(word.replace('-', '').replace('.', ''), add_silent=True)
                word = word.replace('-', '').replace('.', '').replace('+', '')
                tmp_text = ''
                stack_phone = 3 # đọc theo phong cách tiếng việt 033 - 811 - 2029
                for idx_phone in range(len(word)):
                    # silent = ' ' if (idx_phone + 1) % stack_phone else ' = '
                    silent = ' = '
                    tmp_text += n2w(word[idx_phone]) + silent
                final_words.append(tmp_text)
            elif re.search(r"[A-Za-z]+\d{5,}", word):
                print("Case 4")
                # Dạng mật mã Letter + dãy số (K123123123)
                tmp_text = ''
                for idx_pass in range(len(word)):
                    # silent = ' ' if (idx_phone + 1) % stack_phone else ' = '
                    tmp_text += (n2w(word[idx_pass]) if word[idx_pass].isdigit() else asr_phoneme_letter_dict[word[idx_pass]])+ '-'###########
                final_words.append(tmp_text[0:-1]+" ")###########
            elif re.search(r'([0-9]{2})([a-z]{1,})-([0-9]{3}.[0-9]{2})', word):
                print("Case 5")
                # print(word)
                # biển số xe: 49c-098.51 => Vẫn cần bổ sung tiếp
                groups = re.search(r'([0-9]{2})([a-z]{1,})-([0-9]{3}.[0-9]{2})', word)
                tmp_text = convert_number_to_text(groups.group(1)) + ' ' + ' '.join(
                    list(groups.group(2))) + ' ' + n2w_single(groups.group(3).replace('.', ''))
                final_words.append(tmp_text)
            elif re.search(r'.*([aA-zZ]{1,})(\/)([0-9]{1,})', word):
                print("Case 6")
                # Dạng phức hợp: 10-30mm/24h, có nơi trên 50mm/24h
                word = re.sub(r"[\"\'\[\]\(\)~\*#\|\\\/_\^\-]", " ", word.replace("/", " trong "))
                list_sub_word = word.split()
                tmp_text = ''
                for sub_word in list_sub_word:
                    tmp_text += split_num_and_word(sub_word, list_words, idx, org_word=sub_word) + " "
                final_words.append(tmp_text)
            elif "-" in word and re.search(r'^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$',word) is None and re.search(r'^http://|^https://', word) is None:
                print("Case 7")
                if re.search(
                        r'^[0-9]{1,}([\.,][0-9]{1,}){1,}(.*)-[0-9]{1,}([\.,][0-9]{1,}){1,}$|^([0-9]{1,})-([0-9]{1,})$',
                        word):
                    # Dạng hỗn hợp từ ... đến (có dấu gạch ngang ở giữa và ko chứa ký tự): 2.710-3.600, 15-32
                    index_split = word.index('-')
                    # idx_split_word, idx_split_num =
                    tmp_text = " từ " + convert_number_to_text(word[:index_split]).replace('.', '').replace(',', '') + \
                               " đến " + convert_number_to_text(word[index_split + 1:]).replace('.', '').replace(',',
                                                                                                                 '')
                    final_words.append(tmp_text)
                else:
                    list_sub_word = word.split("-")
                    tmp_text = ''
                    if re.search(
                        r'^-[0-9]{1,}([\.,][0-9]{1,}){1,}[^-]{1}|^-([0-9]{1,})[^-]{1}',
                        word):
                        tmp_text = " đến "
                    for sub_word in list_sub_word:
                        if(len(sub_word)>0):
                            tmp_text += split_num_and_word(sub_word, list_words, idx, org_word=sub_word) + " = "

                    final_words.append(tmp_text)

            elif re.search(r'^[0-9]{1,}([\.,][0-9]{1,}){1,}(.*)', word):
                print("Case 8")
                # Dạng số hỗn hợp kèm dấu ., VD: 1.999.530 94,36 0.29% 1.751,6 1,232,123.4
                tmp_text = reformat_num_string(word, org_word, list_words, idx)
                final_words.append(tmp_text)

            elif re.search(r'([0-9]{1,})([a-zA-Z])([0-9]{0,})', word) or \
                    re.search(r'([0-9]{0,})([a-zA-Z])([0-9]{1,})', word):
                # 15h30, xăng A92, boeing 727B, 565ha, tiểu lộ 523B, xăng A95, lớp 12A3, 12m2, 53m3, QL7A
                # print(first_num == '', center_text, last_num=='')
                print("Case 9")
                final_words.append(split_num_and_word(word, list_words, idx, org_word=org_word).strip())

            elif re.search(
                    r'^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$',
                    word):
                # dd/mm/yyyy, dd-mm-yyyy or dd.mm.yyyy
                # print(word)
                print("Case 10")
                groups = re.search(
                    r'^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$',
                    word)
                tmp_text = convert_number_to_text(groups.group(1)) + ' tháng ' + n2w(
                    groups.group(3)) + ' năm ' + convert_number_to_text(groups.group(5))
                final_words.append(tmp_text)

            elif re.search(r'^\d{1,2}[/-]\d{1,4}', word):
                print("Case 11")
                # dd/mm mm/yyyy hoặc phân số
                groups = re.search(r'^(\d{1,2})[/-](\d{1,4})', word)
                first_num = groups.group(1)
                last_num = groups.group(2)
                if len(last_num) == 4:
                    # mm/yyyy
                    tmp_text = n2w(first_num) + ' năm ' + convert_number_to_text(last_num)
                else:
                    # dd/mm hoặc phân số
                    center_text = 'tháng' if idx > 0 and list_words[idx - 1].lower() in ['từ', 'ngày', 'nay', 'đêm',
                                                                                         'mai', 'khi',
                                                                                         'trước', 'sáng', 'qua', 'kia',
                                                                                         'sớm', 'muộn',
                                                                                         'chiều', 'đến', 'từ', 'lúc',
                                                                                         'này', 'đó', 'lúc',
                                                                                         'điểm', 'tại', 'vào', 'ngay',
                                                                                         'đến', 'trước', 'sau',
                                                                                         'khắc', 'giữa', 'trưa', 'sáng',
                                                                                         'tối', 'đêm', 'buổi','mùng',
                                                                                         'hôm'] else 'phần'
                    if first_num[0] == '1':
                        first_num = n2w(first_num)
                    else:
                        first_num = convert_number_to_text(first_num)
                    tmp_text = first_num + ' ' + center_text + ' ' + n2w(last_num)
                final_words.append(tmp_text)

            elif re.search(r'[0-9]{1,}[-\/\\][0-9]{1,}', word):
                print("Case 12")
                # 100-120
                # print(word)
                groups = re.search(r'([0-9]{1,})([-\/\\])([0-9]{1,})', word)
                num_text_1 = groups.group(1)
                num_text_2 = groups.group(3)
                match_symbol = ' đến ' if groups.group(2) == '-' else ' '
                tmp_text = n2w(num_text_1) + match_symbol + n2w(num_text_2)
                final_words.append(tmp_text)

            elif re.search(r'20([0-9]{2})', word):
                print("Case 13")
                # Năm 20xx
                # print(f"Năm: {word}")
                tmp_text = random.choice(
                    [n2w(word), n2w_single(word),
                     n2w_single('20') + ' ' + convert_number_to_text(re.search(r'20([0-9]{2})', word).group(1))])

                final_words.append(tmp_text)       
            elif re.search(r'^http://|^https://', word):
                print(word)
                print("Case 14 http, https")
                # đọc case http ip, hoặc http website
                prefix, link= word.replace("-", " ").split('://')
                tmp_text=''
                if prefix=='http':
                    tmp_text=" hát-tê-tê-pê hai chấm xược xược "
                if prefix=='https':
                    tmp_text=" hát-tê-tê-pê-ét hai chấm xược xược "
                link=link.replace("/", " xược ").replace("."," chấm ").replace(":"," hai chấm ")
                print("link", link)
                list_sub_word=link.split(" ")
                for sub_word in list_sub_word:
                        if(len(sub_word)>0):
                            tmp_text += split_num_and_word(sub_word, list_words, idx, org_word=sub_word) + " "########### =-> -
                final_words.append(tmp_text )

            elif re.search(r'[0-9]+', word):
                print("Case 14")
                # Số đơn giản 10, 30, 5 hoặc là số điện thoại hoặc số % nguyên (15%, 35%)
                # print(word)
                groups = re.search(r'([0-9]+)', word)
                num_text = groups.group(1)
                tmp_text = n2w(num_text) if num_text[0] != '0' else n2w_single(num_text)

                if word[-1] == '%': tmp_text = tmp_text + ' phần trăm'
                final_words.append(' ' + tmp_text + ' ')

            else:
                print("Case 15")
                if tmp_text in common_english_phoneme_dict.keys():
                    tmp_text = common_english_phoneme_dict[tmp_text]
                elif tmp_text in common_acronyms.keys():
                    tmp_text = common_acronyms[tmp_text]
                elif org_word in common_acronyms.keys():
                    tmp_text = common_acronyms[org_word]
                elif org_word.isupper():
                    if idx != 0 and (list_words[idx - 1], org_word) in common_pair_conjunction:
                        tmp_text = common_pair_conjunction[(list_words[idx - 1], org_word)]
                    else:
                        tmp_text = convert_upper_word_to_text(org_word)

                final_words.append(tmp_text)

            if add_silence_last_word and idx != len(list_words) - 1:
                final_words.append('=')

        except Exception as e:
            traceback.print_exc()
            print(f"Error sentence: {normalized_text}")
            # final_words.append(word)
            # list_words_label.pop(idx)
            break

    ####################### output = re.sub("[\"\'\[\]\(\)~\*#\|\\\/_\^\-]", " = ", " ".join(final_words)).lower().strip()
    output = re.sub("[\"\'\[\]\(\)~\*#\|\\\/_\^]", " = ", " ".join(final_words)).lower().strip()
    if output[0] == "=": output = output[1:].strip()
    if output[-1] == "=": output = output[:-1].strip()
    if add_last_break: output = output + " ="
    # if add_last_break and output[-1] != "=": output = output + " = "

    output = re.sub("\s\s+", " ", output.replace('cô vít = mười chín', 'cô vít mười chín').replace("= =", "="))
    print(f"Output len {len(output)}, content: {output}")
    return output


if __name__ == '__main__':
    import asyncio

    text = 'email tôi là ntdong@cmc.com.vn, số điện thoại 033.822.1235, mật mã lấy ở đường km504 có giá trị là k341234123.  Toi'
    output = asyncio.run(normalize_input_text_to_speech(text, False))
    # print(output)

    # print(re.search(r'[0-9]{0,}([\.,][0-9]{0,}){0,}(.*)-[0-9]{0,}([\.,][0-9]{0,}){0,}', "2.710-3.600"))
