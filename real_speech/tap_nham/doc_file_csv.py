import csv
import argparse
import os
import json
import sys
sys.stdout = open("out.txt", "w",encoding='utf8')

def audio_wise_estimate_space_time(arr):
    # arr.pop()#####
    # arr.pop(0)##### nếu là aligned
    total_space_time=[]
    number_space_time=[]
    for i in range(len(arr)-1):
        total_space_time.append(arr[i+1][0]-arr[i][1])
        number_space_time.append([arr[i][1],arr[i+1][0]])
    # for i in range(len(arr)):#####time word
    #     total_space_time.append(arr[i][1]-arr[i][0])
    #     number_space_time.append([arr[i][1],arr[i][0]])
    return total_space_time, len(number_space_time)
def add_equal(arr, textarr):
    for i in range(len(arr)-1):
        if(arr[i+1][0]-arr[i][1])>(0.081*2.5):
            textarr[i]+=" ="
        
    return textarr
def add_two_equal(arr, textarr):
    for i in range(len(arr)-1):
        if(arr[i+1][0]-arr[i][1])>(0.081*8.5):#####???
            textarr[i]+=" ="
        
    return textarr
def estimate_space_time(data_path):
    total_space_time_file = []
    number_space_time_file = []
    new_rows=[]
    with open(data_path + "/gt_force_aligned_with_time_and_api_new_align.csv",encoding='utf8') as f:#####,encoding='utf8'
        csv_reader = csv.reader(f,delimiter=',')
        header = next(csv_reader)
        for row in csv_reader:
            filename = row[0]
            text=row[1]
            numword=row[3]
            # aligned =  eval(row[4])
            cut_video_start=row[5]
            cut_video_end=row[6]
            align_result = eval(row[8])
            align_result_array=[ [word['start'], word['end']] for word in align_result]
            # #####count space time
            # time, count=audio_wise_estimate_space_time(align_result_array)
            # # total_space_time_file.append(time) # tính trung bình
            # total_space_time_file+=time
            # number_space_time_file.append(count)
            # #####/count space time
            ##### add =
            text_array=[ word['word'] for word in align_result]
            text_add_equal=add_equal(align_result_array, text_array)
            text_add_equal=add_two_equal(align_result_array, text_array)#####dau cham
            new_rows.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],' '.join(text_add_equal)])
            if('=' in ' '.join(text_add_equal)):
                print(filename,' '.join(text_add_equal))#####sd khi >out.txt ở cmd .encode('utf8') )
        with open(f'{data_path}/gt_force_aligned_with_time_and_api_new_align_add_equal.csv','w', encoding='UTF8', newline='') as g:
            writer = csv.writer(g)
            writer.writerow(['audio_path','raw_text','true_label','last_words','all_words_time','time_start','time_end','api_request','api_metadata', 'text_add_equal'])
            writer.writerows(new_rows)
            #####/add =
        return total_space_time_file, sum(number_space_time_file)
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="E:\\Text_to_speech\\text_to_speech_dataset\\vov_ngoc_anh\\vov_ngoc_anh_labeled")   
    args = parser.parse_args()   
    sum_total_space_time_all_file=[]
    sum_number_space_time_all_file=[]
    for part in os.listdir(args.data_path):
        data_folder = os.path.join(args.data_path, part)
        # if(part in ['FILETEST'] ): 
        if(os.path.isdir(data_folder)==True) and (part not in ['FILETEST'] ):
            print(part)
            ##### add =
            estimate_space_time(data_folder)
            #####/add=
#             sum_total_space_time_file, sum_number_space_time_file= estimate_space_time(data_folder)
#             # sum_total_space_time_all_file.append(sum_total_space_time_file)
#             sum_total_space_time_all_file+=sum_total_space_time_file
#             sum_number_space_time_all_file.append(sum_number_space_time_file)
#     print("Tong thoi gian", sum(sum_total_space_time_all_file) )
#     print("so luong khoang trang", sum(sum_number_space_time_all_file) )
#     # print("thoi gian nghi trung binh", sum(sum_total_space_time_all_file)/sum(sum_number_space_time_all_file))
#     from statistics import *
#     print("thoi gian nghi trung vi", median(sum_total_space_time_all_file))
    
# import numpy as np
# import matplotlib.pyplot as plt
# plt.hist(sum_total_space_time_all_file,bins=100)
# plt.show()



sys.stdout.close()