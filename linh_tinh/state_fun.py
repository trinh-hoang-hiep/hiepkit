#####interface của các method VD fly, driving sẽ cài đặt
#####1 abstract có phươg thức set algo

# # nhóm 3
# class pointer():
#     value=1


# def observedfunction1():
#     if ("helicopstate"):
#         print("bảo trì trên trời")
#     if ("streetracerstate"):
#         print("bảo trì dưới đất")

# def observedfunction2needcall():
#     if ("helicopstate"):
#         print("đang bay trên trời")
#     if ("streetracerstate"):
#         print("đang chạy dưới đất")

# # index=0
# # a=("streetracer", deepcopy(index),[observedfunction1, observedfunction2needcall])
# x = pointer() 
# a=(["streetracerstate", "helicopstate"], x,[observedfunction1, observedfunction2needcall])
# a[2][a[1].value]()

# # index=1
# x.value= 0
# a[2][a[1].value]()



##### áp dụng state
# nhóm 3
class pointer():
    value=1


def observedfunction1():
    state.observedfunction1()

def observedfunction2needcall():
    state.observedfunction2needcall()

############# đẩy việc cho state pointer
streetracerstate.observedfunction1="bảo trì dưới mặt đất"
streetracerstate.observedfunction2needcall="đang chạy dưới mặt đất"

helicopstate.observedfunction1="bảo trì trên trời"
helicopstate.observedfunction2needcall="đang chạy trên trời"
# index=0
# a=("streetracer", deepcopy(index),[observedfunction1, observedfunction2needcall])
x = pointer() 
a=(["streetracerstate", "helicopstate"], x,[observedfunction1, observedfunction2needcall])
a[2][a[1].value]()

# index=1
x.value= 0
a[2][a[1].value]()