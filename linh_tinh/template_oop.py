# similar to strategy pattern, but selection of implementation method does not happen runtime, but rather at compile-time by subclassing the template
# class abstract (trừu tượng), cung cấp các cách để chạy chạy phương thức của nó Các bước chung được triển khai, và các bước riêng biệt được ghi đè trong lớp con
# useful for DRY code; ubclasses can share a core set of functionality and have the ability to override 
# Inversion of Control (IoC): Abstract: - decouples the execution of a task from its implementation 
# khách không gọi trực tiếp các phương thức triển khai mà gọi một template_method để sau đó gọi các phương thức triển khai
# rong thiết kế web, khi chúng ta có 1 trang template đã có sẵn header, footer, navigation, chỉ riêng phần boby là để trống và sẽ display nội dung theo từng page
# From https://github.com/jackdbd/design-patterns
import sys
from abc import ABC, abstractmethod

# Base class defining the template_method
class algorithm(ABC):

    def template_method(self):
        """Skeleton of operations to perform. DON'T override me.

        The Template Method defines a skeleton of an algorithm in an operation,
        and defers some steps to subclasses.
        """
        self.__do_absolutely_this()
        self.do_step_1()
        self.do_step_2()
        self.do_something()

    def __do_absolutely_this(self): # indicates that cannot be overridden by subclass
        """Protected operation. DON'T override me."""
        this_method_name = sys._getframe().f_code.co_name
        print('{}.{}'.format(self.__class__.__name__, this_method_name))

    @abstractmethod # indicates that must be overridden by subclass
    def do_step_1(self):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    @abstractmethod # indicates that must be overridden by subclass
    def do_step_2(self):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    def do_something(self): # can be overridden by subclass or simply used a default
        """Hook. You CAN override me, I'm NOT a placeholder."""
        print('do something')





# Subclass override of abstract methods
# Subclass use of default for do_something
class algorithm_a(algorithm):

    def do_step_1(self):
        print('do step 1 for Algorithm A')

    def do_step_2(self):
        print('now do step 2 for Algorithm A')

# Subclass override of abstract methods
# Subclass override of do_something
class algorithm_b(algorithm):

    def do_step_1(self):
        print('do different step 1 for Algorithm B')

    def do_step_2(self):
        print('now do different step 2 for Algorithm B')

    def do_something(self):
        print('do something else')




# Client code
def main():
    print('Algorithm A')
    a = algorithm_a()
    a.template_method()

    print('\nAlgorithm B')
    b = algorithm_b()
    b.template_method()

if __name__ == '__main__':
    main()

