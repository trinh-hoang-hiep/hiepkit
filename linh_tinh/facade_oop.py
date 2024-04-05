# # ##### nhóm 2
# # Khi ta chúng ta có chuỗi các hành động được thực hiện theo thứ tự phải xử lý chính xác với bên thứ 3. Từ đó logic nghiệp vụ của các lớp trở nên gắn kết chặt chẽ với thư viện thử 3,  ở nhiều file 
# # cần cấu trúc lại tránh  copy/paste => chúng ta sẽ chỉ cần gọi Facade để thực thi các hành động dựa trên các parameters được cung cấp.
# # Bây giờ nếu chúng ta cần bất kỳ thay đổi nào trong quá trình trên, công việc sẽ đơn giản hơn rất nhiều, chỉ cần thay đổi các xử lý trong façade, mọi thứ sẽ được đồng bộ
# # https://viblo.asia/p/facade-design-pattern-tro-thu-dac-luc-cua-developers-924lJBLNlPM
# # Các thành phần trong mô hình:

# # Facade: Facade nắm rõ được hệ thống con nào đảm nhiệm việc đáp ứng yêu cầu của client, nó sẽ chuyển yêu cầu của client đến các đối tượng hệ thống con tương ứng.
# # Addition Facade: có thể được tạo ra để tránh việc làm phức tạp một facade. Có thể được sử dụng bởi cả client và facade.
# # Complex Subsystems: Bao gồm nhiều object khác nhau, được cài đặt các chức năng của hệ thống con, xử lý công việc được gọi bởi Facade. Các lớp này không cần biết Facade và không tham chiếu đến nó.
# # Client: Đối tượng sử dụng Facade để tương tác với các subsystem thay vì gọi subsystem trực tiếp
# # Các đối tượng Facade thường là Singleton bởi vì chỉ cần duy nhất một đối tượng Facade.

# # Nhược điểm
# # Class Facade của bạn có thể trở lên quá lớn, làm quá nhiều nhiệm vụ với nhiều hàm chức năng trong nó.
# # Dễ bị phá vỡ các quy tắc trong SOLID.

# # Khi nào thì sử dụng
# # Muốn gom nhóm chức năng lại để Client dễ sử dụng.
# # Giảm sự phụ thuộc ht con. Khi bạn muốn phân lớp các hệ thống con. Dùng Façade Pattern để định nghĩa cổng giao tiếp chung cho mỗi hệ thống con, 


# # Tạo Subsystem
# class AccountService:
#     def get_account(self, email):
#         print(f"Getting the account of {email}")

# class EmailService:
#     def send_mail(self, mail_to):
#         print(f"Sending an email to {mail_to}")

# class PaymentService:
#     def payment_by_paypal(self):
#         print("Payment by Paypal")

#     def payment_by_credit_card(self):
#         print("Payment by Credit Card")

#     def payment_by_ebanking_account(self):
#         print("Payment by E-banking account")

#     def payment_by_cash(self):
#         print("Payment by cash")

# class ShippingService:
#     def free_shipping(self):
#         print("Free Shipping")

#     def standard_shipping(self):
#         print("Standard Shipping")

#     def express_shipping(self):
#         print("Express Shipping")

# class SmsService:
#     def send_sms(self, mobile_phone):
#         print(f"Sending an message to {mobile_phone}")



# # Tạo Facade
# class ShopFacade:
#     _instance = None

#     def __init__(self):
#         self.account_service = AccountService()
#         self.payment_service = PaymentService()
#         self.shipping_service = ShippingService()
#         self.email_service = EmailService()
#         self.sms_service = SmsService()

#     @classmethod
#     def get_instance(cls):
#         if cls._instance is None:
#             cls._instance = ShopFacade()
#         return cls._instance

#     def buy_product_by_cash_with_free_shipping(self, email):
#         self.account_service.get_account(email)
#         self.payment_service.payment_by_cash()
#         self.shipping_service.free_shipping()
#         self.email_service.send_mail(email)
#         print("Done\n")

#     def buy_product_by_paypal_with_standard_shipping(self, email, mobile_phone):
#         self.account_service.get_account(email)
#         self.payment_service.payment_by_paypal()
#         self.shipping_service.standard_shipping()
#         self.email_service.send_mail(email)
#         self.sms_service.send_sms(mobile_phone)
#         print("Done\n")

# def main():
#     shop_facade = ShopFacade.get_instance()
#     shop_facade.buy_product_by_cash_with_free_shipping("18520282@gm.uit.edu.vn")
#     shop_facade.buy_product_by_paypal_with_standard_shipping("uit@gmail.edu.vn", "0123456789")


# # Client gọi Facade
# if __name__ == "__main__":
#     main()



##### bsung
import smtplib
import smtplib

class EmailFacade:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
    
    def send_email(self, to_email, subject, message):
        if not "@" in self.username: # is username wino6687 or wino6687@colorado.edu
            from_email = "{0}@{1}".format(
                    self.username, self.host)
        else:
            from_email = self.username
        message = ("From: {0}\r\n"
                  "To: {1}\r\n"
                  "Subject: {2}\r\n\r\n{3}").format(
                            from_email,
                            to_email,
                            subject,
                            message)
        
        smtp = smtplib.SMTP(self.host)
        smtp.login(self.username, self.password)
        smtp.sendmail(from_email, [to_email],message)    
        
        
        
        
        
        
    def get_inbox(self):
        mailbox = imap.IMAP4(self.host)
        mailbox.login(bytes(self.username, 'utf8'),
                    bytes(self.password, 'utf8'))
        mailbox.select()
        x,data = mailbox.search(None, 'ALL')
        messages = []
        for num in data[0].split():
            x,message = mailbox.fetch(num, '(RFC822)')
            messages.append(message[0][1])
        return messages