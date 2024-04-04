# nhóm 1 nhóm khởi tạo, tránh keyword new 
# Đảm bảo rằng một class chỉ có duy nhất một instance = cách Private constructor của class đó để đảm bảo rằng class lớp khác không thể, và Tạo một biến private static là instance của class đó chỉ được tạo ra trong class đó thôi
# Và cung cấp một cáchs toàn cầu để truy cấp tới instance đó.= cách Tạo một public static menthod trả về instance vừa khởi tạo bên trên, đây là cách duy nhất truy cập
# minimizes the need to pass around the reference to the manager object
# https://viblo.asia/p/hoc-singleton-pattern-trong-5-phut-4P856goOKY3
from threading import Lock

class ThreadSafeSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ThreadSafeSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        pass

a=ThreadSafeSingleton()
print(a)

# 1 thresh
# và multi thresh