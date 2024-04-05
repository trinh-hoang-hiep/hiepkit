#####interface của các method VD fly, driving sẽ cài đặt
#####1 abstract có phươg thức set algo

# nhóm 3


light=["light off","light on"]

def CommandOff():
    print(light[0])

def CommandOn():
    print(light[1])

RemoteControl=[CommandOff,CommandOn ]

RemoteControl[0]()