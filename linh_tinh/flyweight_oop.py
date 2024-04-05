# ##### thuộc nhóm 2
# # python tự garbage collector, nhưng cần thêm:
# # ý tường: Concept: khi nào oom thì ms cần "Premature optimization is the most effective way to create a program that is too complicated to maintain"
# # Ensures that objects that share a state can use the same memory for that shared state.
# # Đảm bảo rằng các đối tượng chia sẻ trạng thái có thể sử dụng cùng bộ nhớ cho trạng thái chia sẻ đó.
# # RAM có sẵn bằng cách chia sẻ, phân phối các phần trạng thái chung - riêng giữa nhiều đối tượng thay vì giữ tất cả dữ liệu trong mỗi đối tượng.
# # Tần suất sử dụng: Thấp
# # Dữ liệu không đổi này của một đối tượng thường được gọi là trạng thái intrinsic
# # nó tồn tại bên trong đối tượng; các đối tượng khác chỉ có thể đọc nó, không thay đổi nó. Phần còn lại của trạng thái của đối tượng, thường bị thay đổi “từ bên ngoài” bởi các đối tượng khác, được gọi là trạng thái extrinsic.
# #  Trạng thái được truyền cho các phương thức của flyweight được gọi là “extrinsic”.
# # VD kiểm kê ô tô
# # Mỗi chiếc xe đều có số seri và màu sắc riêng biệt, nhưng đã là ô tô thì phải có 4 bánh, có gương có,....Thông thường chúng ta sẽ phải lưu trữ một danh sách tất cả các thuộc tính mà một chiếc ô tô nhất định có hoặc không có. Nếu bạn có nhiều mẫu xe thì điều này sẽ nhanh chóng gây lãng phí bộ nhớ
# # Solution: sd flyweight chứa shared objects for the list of features for each mẫu xe, and reference mẫu xe with the serial number and color to find an individual vehicle!
# code: ta sd __new__ constructur để implement the flyweight pattern, However, this will only return one instance of the class, and we want to have different instances depending on the keys
# NHƯNG, khi chúng tôi bán hết một mẫu ô tô, nó vẫn tồn tại trong từ điển và do đó vẫn chiếm bộ nhớ
# Thay vào đó, hãy sử dụng trình thu gom rác của python để giải quyết vấn đề này cho chúng ta
# Using the weakref module:
#     provides a WeakValueDictionary object
#     If we end up with an object reference location that has no values stored at that time, the garbage collector will come along and clean it

# 1. Xây dựng nhà máy
# Chúng tôi sử dụng một nhà máy để xây dựng và xây dựng các phiên bản flyweight
# Chúng tôi cần một nhà máy cho từng loại phiên bản flyweight
# Bất cứ khi nào chúng ta xây dựng một flyweight mới với một tên cụ thể, chúng ta sẽ tra cứu tên đó trong lệnh tham chiếu yếu
# Nếu nó tồn tại
#   trả lại mô hình
# Nếu không
#   tạo mô hình mới
# Bất chấp điều đó, chúng tôi sẽ gọi phương thức __init__ của flyweight mỗi lần

import weakref
class CarModel:
    _models = weakref.WeakValueDictionary()#####cls._models
    
    def __new__(cls, model_name, *args, **kwargs):
        model = cls._models.get(model_name)##### ko có
        if not model: 
            model = super().__new__(cls)#####đc 1 carmodel
            cls._models[model_name] = model
            
        return model
    
    def __init__(self, model_name, air = False, tilt = False,##### chạy new trc r chạy init
                cruise_control=False, power_locks=False,
                alloy_wheels=False, usb_charger=False):
        if not hasattr(self,"initted"): # ensure we only initialize object once
            self.model_name = model_name
            self.air = air
            self.tilt = tilt
            self.cruise_control = cruise_control
            self.power_locks = power_locks
            self.alloy_wheels = alloy_wheels
            self.usb_charger = usb_charger
            self.initted=True
            
    def check_serial(self, serial_number):
        print("Sorry, we can't check that"
             "The serial number {0} on the {1}"
             "at this time".format(
             serial_number, self.model_name))
        

# Define class that stores additional info and references the flyweight:

class Car: 
    def __init__(self, model, color, serial):
        self.model = model
        self.color = color 
        self.serial = serial
        
    def check_serial(self):
        return self.model.check_serial(self.serial)
    
    
    

dx = CarModel("FIT DX")
lx = CarModel("FIT LX", air=True, cruise_control=True,
              power_locks=True, tilt=True)
car1 = Car(dx, "blue", "122345")
car2 = Car(dx, "black", "12346")
car3 = Car(lx, "red", "12347")



print(id(lx))
del lx
del car3

import gc
gc.collect()
# 4533179504
# 0




lx = CarModel("FIT LX", air=True, cruise_control=True,
             power_locks=True, tilt=True)#####lại __new__
print(id(lx))

lx = CarModel("FIT LX")#### gọi lx lần 2 nhưng same id, ko tạo lại, ko init lại
print(id(lx))

print(lx.air)
# 4533178832
# 4533178832
# True