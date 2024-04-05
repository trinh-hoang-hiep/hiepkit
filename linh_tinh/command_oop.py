# nhóm 3
# Đóng gói tất cả thông tin cần thiết vào 1 đối tượng để thực hiện hành động hay kích hoạt một sự kiện thực hiện sau đó. Các thông tin có thể bao gồm tên phương thức, các biến và giá trị cần thiết...hay đơn giản hơn đó là nó cho phép chuyển yêu cầu thành đối tượng độc lập, có thể được sử dụng để tham số hóa các đối tượng với các yêu cầu khác nhau như log, queue (undo/redo), transtraction.
# Express a request, including the call to be made and all of its required paraemtersl, IN A COMMAND OBJECT 
# Adds a level of abstraction between actions , and the object that invokes those actions
# Trong đó:

# Command : là một interface hoặc abstract class, chứa một phương thức trừu tượng thực thi (execute) một hành động (operation). Request sẽ được đóng gói dưới dạng Command.
# ConcreteCommand : là các implementation của Command. Định nghĩa một sự gắn kết giữa một đối tượng Receiver và một hành động. Thực thi execute() bằng việc gọi operation đang hoãn trên Receiver. Mỗi một ConcreteCommand sẽ phục vụ cho một case request riêng.
# Client : tiếp nhận request từ phía người dùng, đóng gói request thành ConcreteCommand thích hợp và thiết lập receiver của nó.
# Invoker : tiếp nhận ConcreteCommand từ Client và gọi execute() của ConcreteCommand để thực thi request.
# Receiver : đây là thành phần thực sự xử lý business logic cho case request. Trong phương thức execute() của ConcreteCommand chúng ta sẽ gọi method thích hợp trong Receiver.
# https://viblo.asia/p/vai-net-ve-command-pattern-Do754bQBZM6

# Dưới đây là sequence diagram của command pattern.
#  switchOn và switchOff: Đây đóng vai trò là 1 class request
class Light:
    def switch_on(self):
        print("light on")

    def switch_off(self):
        print("light off")
# 1 interface tên là Command không trực tiếp tắt bật đèn mà chỉ ra lệnh cho light on or off.
class Command:
    def execute(self):
        pass
# sau đó chúng ta sẽ khởi tạo 2 class CommandOff và CommandOn implement Command: 2 class này chính là ConcreteCommand
class CommandOff(Command):
    def execute(self):
        Light().switch_off()

class CommandOn(Command):
    def execute(self):
        Light().switch_on()

# Tiếp theo tiến hành đóng gói các command này vào trong 1 bộ điều khiển gọi là Remote Control: class này đóng vai trò là invoker
class RemoteControl:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def run(self):
        self.command.execute()

# Chúng ta tạo 1 client để thực thi và xem kết quả:

remote = RemoteControl()
command_off = CommandOff()
remote.set_command(command_off)
remote.run()


















# # Common Use for Command Pattern: Graphical Windows
# # Buttons that exist in a simple GUI are essentially just functionility that is built and ready but waiting to be executed
# # Executing something when it is selected is called invoking
# # Actions that occur when you select a menu item, a keyboard shortcut, or a toolbar icon are all examples of invoker objects!
# # Example: Simple command pattern to provide Save and Exit actions

# import sys 

# class Window:
#     def exit(self):
#         sys.exit(0)

# class Document:
#     def __init__(self,filename):
#         self.filename = filename 
#         self.contents = "This file cannot be modified"
#     def save(self):
#         with open(self.filename, 'w') as file:
#             file.write(self.contents)

# # Note:

# # These objects are trivially simple.
# # In a real environment the Window would need to handle things like mouse clicks and movement. The document would need to handle things like insertion and deletion.

# # define invoker classes
# class ToolbarButton:
#     def __init__(self,name, iconname):
#         self.name = name 
#         self.iconname = iconname
    
#     def click(self):
#         self.command.execute()
    
# class MenuItem:
#     def __init__(self, menu_name, menuitem_name):
#         self.menu = menu_name 
#         self.item = menuitem_name
        
#     def click(self):
#         self.command.execute()

# class KeyboardShortcut:
#     def __init__(self, key, modifier):
#         self.key = key 
#         self.modifier = modifier 
        
#     def keypress(self):
#         self.command.execute()
        
        
# # hook up the commands 
# class SaveCommand:
#     def __init__(self, document):
#         self.document = document 
    
#     def execute(self):
#         self.document.save()
        
# class ExitCommand:
#     def __init__(self, window):
#         self.window = window
    
#     def execute(self):
#         self.window.exit()
        
        
        
# window = Window()
# document = Document("C:\\Users\\sodalab\\Documents\\hiep_toolkit\\linh_tinh\\a_document.txt")
# save = SaveCommand(document)
# exit = ExitCommand(window)

# # create save button that can be used later 
# save_button = ToolbarButton('save', 'save.png')
# save_button.command = save
# save_keystroke = KeyboardShortcut("s", "ctrl")
# save_keystroke.command = save
# exit_menu = MenuItem("File", "Exit")
# exit_menu.command = exit