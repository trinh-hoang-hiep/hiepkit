#####interface của các method VD fly, driving sẽ cài đặt
#####1 abstract có phươg thức set algo

# nhóm 3
class pointer():
    value=1


def observedfunction1():
    print("fly")

def observedfunction2needcall():
    print("race")

# index=0
# a=("streetracer", deepcopy(index),[observedfunction1, observedfunction2needcall])
x = pointer() 
a=("streetracer", x,[observedfunction1, observedfunction2needcall])
a[2][a[1].value]()

# index=1
x.value= 0
a[2][a[1].value]()