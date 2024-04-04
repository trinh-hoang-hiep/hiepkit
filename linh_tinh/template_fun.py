##### la su dung abstract
def phuong_thuc1():
    pass
def phuong_thuc2():
    pass
def phuong_thuc3():
    print('do something')

abstract=([phuong_thuc1,phuong_thuc2],phuong_thuc3)
algorithm_b=abstract
def phuong_thuc():
    print('implemented')
for i in range(len(abstract[0])):
    algorithm_b[0][i]=phuong_thuc

[i() for i in algorithm_b[0]]