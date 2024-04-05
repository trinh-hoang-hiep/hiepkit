# # thuộc nhóm 2, quan hệ giữa các đối tượng, giống decorator, nhưng decorator cần same interface, adapter thì ko cần, 
# # nó link 2 class,  allow two pre-existing objects to work together, even if their interfaces are not compatible
# # Ta có thể dựa vào class diagram để theo dõi mẫu này.
# # cả Adapter và Decorator đều sử dụng phương thức 'gói' (wrap) object, nhưng Decorator Pattern gói object để gán thêm trách nhiệm cho nó, còn Adapter Pattern gói object để biến hóa interface ban đầu thành interface client cần sử dụng. 
# # https://gpcoder.com/4483-huong-dan-java-design-pattern-adapter/
# # Một Adapter Pattern bao gồm các thành phần cơ bản sau:

# # Adaptee: định nghĩa interface không tương thích, cần được tích hợp vào.
# # Adapter: lớp tích hợp, giúp interface không tương thích tích hợp được với interface đang làm việc. Thực hiện việc chuyển đổi interface cho Adaptee và kết nối Adaptee với Client.
# # Target: một interface chứa các chức năng được sử dụng bởi Client (domain specific).
# # Client: lớp sử dụng các đối tượng có interface Target.
# # Solution: 2 cách: Composition (Chứa trong) và Class Adapter – Inheritance (Kế thừa)
# # Nó sử dụng Composition để giữ một thể hiện của Adaptee, cho phép một Adapter hoạt động với nhiều Adaptee nếu cần thiết.

# # Client: người Việt sẽ là Client trong ví dụ này,vì anh ta cần gửi một số message cho người Nhật.
# # Target: đây là nội dung message được Client cung cấp cho thông dịch viên (Translator / Adapter).
# # Adapter: thông dịch viên (Translator) sẽ là Adapter, nhận message tiếng Việt từ Client và chuyển đổi nó sang tiếng Nhật trước khi gởi cho người Nhật.
# # Adaptee: đây là interface hoặc class được người Nhật sử dụng để nhận message được chuyển đổi từ thông dịch viên (Translator).
# ##### ta cài theo cachs 1 Adaptee has a Adapter

# class JapaneseAdaptee:
#     def receive(self, words):
#         print("Retrieving words from Adapter ...")
#         print(words)

# class TranslatorAdapter:
#     def __init__(self, adaptee):##### has a
#         self.adaptee = adaptee

#     def send(self, words):
#         print("Reading Words ...")
#         print(words)
#         vietnamese_words = self.translate(words)
#         print("Sending Words ...")
#         self.adaptee.receive(vietnamese_words)

#     def translate(self, vietnamese_words):
#         print("Translated!")
#         return "こんにちは"

# def main():
#     client = TranslatorAdapter(JapaneseAdaptee())
#     client.send("Xin chào")

# if __name__ == "__main__":
#     main()



# VD 2

class AgeCalculator:
    def __init__(self, birthday):
        # this class formats the year month, day into int's from strings
        self.year, self.month, self.day = (
            int(x) for x in birthday.split('-'))
        
    def calculate_age(self,date):
        year, month, day = (
                int(x) for x in date.split('-'))
        age = year - self.year
        if (month,day) < (self.month,self.day):
            age -= 1
        return age
    
# nhưng muốn từ string sang datetime object instead  We could write an adapter that allows a normal date to be entered into a normal AgeCalculator class
# trong adapter (wrappẻ đó có hàm convert) with datetime.date.strftime('%Y-%m-%d')

import datetime
class DateAgeAdapter:
    def _str_date(self, date):
        return date.strftime("%Y-%m-%d")
    
    def __init__(self, birthday):
        birthday = self._str_date(birthday)
        self.calculator = AgeCalculator(birthday)##### ko phải cách 1, extend  mà là cách 2 has a
        
    def get_age(self, date): # method name can be different, and arguments can change
        date = self._str_date(date)
        return self.calculator.calculate_age(date)
    
    

d = DateAgeAdapter(datetime.date(1975,1,1))
print("Adapter Implementation: {}".format(d.get_age(datetime.date.today())))

d1 = AgeCalculator("1975-01-01")
print("String Implementation: {}".format(d1.calculate_age("2019-03-17")))