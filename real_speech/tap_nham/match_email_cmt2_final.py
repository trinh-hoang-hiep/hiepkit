import numpy as np

def match_name_email(reference, hypothesis):
    # hyp_words = hypothesis.split()
    ref_words = list(reference)
    hyp_words = list(hypothesis)
    # Initialize a matrix with size |ref_words|+1 x |hyp_words|+1
    # The extra row and column are for the case when one of the strings is empty
    d = np.zeros((len(ref_words) + 1, len(hyp_words) + 1))
    # # The number of operations for an empty reference to become the hypothesis
    # # is just the number of words in the hypothesis (i.e., inserting all words)
    # for j in range(len(hyp_words) + 1):
    #     d[0, j] = j
    # # Iterate over the words in the reference and hypothesis
    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i - 1] == hyp_words[j - 1] or ref_words[i - 1] =="*" or hyp_words[j - 1] =='*':
                d[i, j] = d[i - 1, j - 1]+1
            else:
                # substitution = d[i - 1, j - 1] + 1
                # insertion = d[i, j - 1] + 1
                # deletion = d[i - 1, j] + 1
                d[i, j] = 0
    # wer = d[len(ref_words), len(hyp_words)] / len(ref_words)
    dmax=d.max()
    if dmax==float(len(ref_words)):
        end=list(d[-1,:]).index(dmax)
        return dmax, (end-int(dmax),end)
    else:
        return 0, (0,0)


# prefix ="ntdong218.net"
# result=match_name_email("nguyen",prefix)#####nguyen, uyen, uy, yen#####("pn**hie*", "n_d*ng_hiep_h*e*")
# print(result)
from normalize_input.vietnamese_name import cmc_name_dict 
from collections import defaultdict
import random

def match_username(prefix):
    dict_result=defaultdict(list)
    for norm_name in cmc_name_dict.keys():
        result=match_name_email(norm_name,prefix)
        dict_result[result[0]].append((norm_name,result[1]))
    order_dict_result=dict(sorted(dict_result.items()))
    # print(list(order_dict_result.items())[-1])#####(6.0, [('nguyen', (0, 6))])
    best_match_result=order_dict_result[list(order_dict_result.keys())[-1]][0]
    if(list(order_dict_result.items())[-1][0]>0):
        return  ([prefix[0:best_match_result[1][0]], random.choice(cmc_name_dict[best_match_result[0]]), prefix[best_match_result[1][1]:]],[0,1,0])
    else:
        return ([prefix],[0])

print(match_username("ntdong218.net"))

    