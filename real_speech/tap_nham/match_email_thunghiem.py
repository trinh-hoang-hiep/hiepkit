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

result=match_name_email("nguyen","nguyenlm")#####nguyen, uyen, uy, yen#####("pn**hie*", "n_d*ng_hiep_h*e*")
print(result)
from vietnamese_name import cmc_name_dict 
print(cmc_name_dict)