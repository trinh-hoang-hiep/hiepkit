# # nhom 2
# # Composite Pattern là một sự tổng hợp những thành phần có quan hệ với nhau để tạo ra thành phần lớn hơn. 
# # xo the  thực hiện các tương tác với tất cả đối tượng trong mẫu 
# # 1 container chua cac child components
# # cấu trúc dạng cây: 1 component là một nút lá không thể chứa các đối tượng khác hoặc nó là một nút tổng hợp  composite node
# # Allows clients to treat individual objects and composositions uniformly
# # Nút là 1 abstract và các dẫn xuất của nó là các lá hoặc collections nút khác Node is an abstract base class, and its derivatives are either leaves or collections of other nodes
# # Khi một thao tác được thực hiện trên gốc, thao tác đó sẽ được truyền đệ quy xuống con 
# # Đối với mỗi composite object, chúng tôi giữ một dictionary of children (thường là một list là đủ)
# # Sử dụng từ điển cho phép chúng ta tra cứu trẻ em theo tên
# # Ví dụ: bạn có hai loại đối tượng: Sản phẩm và Hộp. Một Hộp có thể chứa nhiều Sản phẩm cũng như một số Hộp nhỏ hơn. Những chiếc Hộp nhỏ này có thể cũng giữ một số Sản phẩm hoặc thậm chí các Hộp nhỏ hơn, v.v.
# Giả sử bạn quyết định tạo một hệ thống đặt hàng. Làm thế nào bạn sẽ xác định tổng giá của một đơn đặt hàng như vậy? Bạn có thể mở tất cả các hộp, xem qua tất cả các sản phẩm và sau đó tính tổng. Nhưng cách tiếp cận này khi thực thi chương trình đòi hỏi mức độ lồng ghép và cấu trúc phức tạp.
# Giải pháp: 1 giao diện chung khai báo một phương pháp tính tổng giá. Đối với một hộp, nó sẽ đi qua từng mục trong hộp chứa, hỏi giá của nó và sau đó trả lại tổng giá cho hộp này.
# Các thành phần trong mô hình:

# Component: là một interface hoặc abstract class quy định các method chung cần phải có cho tất cả các thành phần tham gia vào mẫu này
# Leaf: là lớp hiện thực (implements) các phương thức của Component - các object không có con.
# Composite: lưu trữ tập hợp các Leaf và cài đặt các phương thức của Component. Composite cài đặt các phương thức được định nghĩa trong interface Component bằng cách ủy nhiệm cho các thành phần con xử lý.
# Client: sử dụng Component để làm việc với các đối tượng trong Composite.
# 3. Kiến trúc


from abc import ABC, abstractmethod
from typing import List
# Tạo Component
class GiftBase(ABC):
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    @abstractmethod
    def calculate_total_price(self) -> int:
        pass

class IGiftOperations(ABC):
    @abstractmethod
    def add(self, gift: 'GiftBase'):
        pass

    @abstractmethod
    def remove(self, gift: 'GiftBase'):
        pass

# Tạo Composite
class CompositeGift(GiftBase, IGiftOperations):
    def __init__(self, name: str, price: int):
        super().__init__(name, price)
        self._gifts: List[GiftBase] = []

    def add(self, gift: 'GiftBase'):
        self._gifts.append(gift)

    def remove(self, gift: 'GiftBase'):
        self._gifts.remove(gift)

    def calculate_total_price(self) -> int:
        total = 0
        print(f"{self.name} contains the following products with prices:")
        for gift in self._gifts:#####duyet GiftBase_CompositeGift or SingleGift -> dequy
            total += gift.calculate_total_price()
        return total
# Tạo Leaf
class SingleGift(GiftBase):
    def calculate_total_price(self) -> int:
        print(f"{self.name} with the price {self.price}")
        return self.price
# Tạo Client
def main():
    phone = SingleGift("Phone", 256)
    print(phone.calculate_total_price())

    # composite gift
    root_box = CompositeGift("RootBox", 0)
    truck_toy = SingleGift("TruckToy", 289)
    plain_toy = SingleGift("PlainToy", 587)
    root_box.add(truck_toy)
    root_box.add(plain_toy)
    child_box = CompositeGift("ChildBox", 0)
    soldier_toy = SingleGift("SoldierToy", 200)
    child_box.add(soldier_toy)
    root_box.add(child_box)
    print(f"Total price of this composite present is: {root_box.calculate_total_price()}")

if __name__ == "__main__":
    main()

