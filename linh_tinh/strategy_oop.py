# # Behavior Pattern nhóm 3
# #sửa method của các class
# # VD bài toán Car kế thừa Vehicle, đỡ phải override hàm go cho lớp Helicopter , chỉ thay đổi 1 file
# # SOLUTION thay đổi Car "is-a" sang "has-a" trích những đoạn code dễ thay đổi và đóng gói chúng vào đối tượng
# # sd  “sự kết hợp” composites các đối tượng  chọn ra và sử dụng đối tượng cần thiết
# # Từng đối tượng sẽ thực hiện hành động của riêng nó. Một đối tượng, một nhiệm vụ thường là có ý nghĩa hơn là việc kế thừa các lớp, và tạo ra hàng tá các lớp con. Nói cách khác, chúng ta sắp xếp lại dựa trên nhiệm vụ của lớp, chứ không phải trên sự kế thừa.
class GoAlgorithm():
    def go(self):
        pass

class GoByDrivingAlgorithm(GoAlgorithm):
    def go(self):
        print("Now I'm driving.")

class GoByFlyingAlgorithm(GoAlgorithm):
    def go(self):
        print("Now I'm flying.")

class GoByDrivingFastAlgorithm(GoAlgorithm):####tự super()
    def go(self):
        print("Now I'm driving fast.")

#####hết 1 file




from abc import ABC, abstractmethod
class Vehicle(ABC): #####public abstract class Vehicle
    # private GoAlgorithm goAlgorithm

    # public void setGoAlgorithm(GoAlgorithm algorithm) {
    #     goAlgorithm = algorithm;
    # }
    
    def setGoAlgorithm(self,algorithm)->GoAlgorithm:
        self.goAlgorithm=algorithm
        return algorithm
    # public void go() {
    #     goAlgorithm.go();
    # }
    # @abstractmethod #####cách 2
    def go(self):
        self.goAlgorithm.go()

# public class Helicopter extends Vehicle {
#     public Helicopter() {
#         setGoAlgorithm(new GoByFlyingAlgorithm());
#     }
# }

class Helicopter (Vehicle):
    def __init__(self, *args, **kwargs):################ ko có cũng đc 
        
        super().__init__(*args, **kwargs)####################ko có cũng đc 
        self.setGoAlgorithm( GoByFlyingAlgorithm())
    # #####cách 2
    # def go(self): 
    #     self.goAlgorithm.go()

helicopter = Helicopter()
helicopter.go()

class StreetRacer  (Vehicle):
    def __init__(self, *args, **kwargs):################ ko có cũng đc 
        
        super().__init__(*args, **kwargs)####################ko có cũng đc 
        self.setGoAlgorithm( GoByDrivingFastAlgorithm())
 


streetRacer = StreetRacer()
streetRacer.go()
streetRacer.setGoAlgorithm(GoByFlyingAlgorithm())##### nếu khách đòi sửa thì có ngay
streetRacer.go()





# from abc import ABC
# from enum import Enum, auto


# class OutputFormat(Enum):
#     MARKDOWN = auto()
#     HTML = auto()


# # not required but a good idea
# class ListStrategy(ABC):
#     def start(self, buffer): pass

#     def end(self, buffer): pass

#     def add_list_item(self, buffer, item): pass


# class MarkdownListStrategy(ListStrategy):

#     def add_list_item(self, buffer, item):
#         buffer.append(f' * {item}\n')


# class HtmlListStrategy(ListStrategy):

#     def start(self, buffer):
#         buffer.append('<ul>\n')

#     def end(self, buffer):
#         buffer.append('</ul>\n')

#     def add_list_item(self, buffer, item):
#         buffer.append(f'  <li>{item}</li>\n')


# class TextProcessor:
#     def __init__(self, list_strategy=HtmlListStrategy()):
#         self.buffer = []
#         self.list_strategy = list_strategy

#     def append_list(self, items):
#         self.list_strategy.start(self.buffer)
#         for item in items:
#             self.list_strategy.add_list_item(
#                 self.buffer, item
#             )
#         self.list_strategy.end(self.buffer)

#     def set_output_format(self, format):
#         if format == OutputFormat.MARKDOWN:
#             self.list_strategy = MarkdownListStrategy()
#         elif format == OutputFormat.HTML:
#             self.list_strategy = HtmlListStrategy()

#     def clear(self):
#         self.buffer.clear()

#     def __str__(self):
#         return ''.join(self.buffer)


# if __name__ == '__main__':
#     items = ['foo', 'bar', 'baz']

#     tp = TextProcessor()
#     tp.set_output_format(OutputFormat.MARKDOWN)
#     tp.append_list(items)
#     print(tp)

#     tp.set_output_format(OutputFormat.HTML)
#     tp.clear()
#     tp.append_list(items)
#     print(tp)