# from abc import ABC ################https://github.com/MilovanTomasevic/Python-Design-Patterns/tree/master/src/1_patterns/3_StructuralPatterns/4_Decorator


# class Shape(ABC):
class Shape():
    def __str__(self):
        return ''


class Circle(Shape):##### class của instance _pizza
    def __init__(self, radius=0.0):
        self.radius = radius

    def resize(self, factor):
        self.radius *= factor

    def __str__(self):
        return f'A circle of radius {self.radius}'


# class Square(Shape):
#     def __init__(self, side):
#         self.side = side

#     def __str__(self):
#         return f'A square with side {self.side}'


class ColoredShape(Shape):######pizza decore _abstract
    def __init__(self, shape, color):
        # if isinstance(shape, ColoredShape):#####ngăn decore 2 lần 
        #     raise Exception('Cannot apply ColoredDecorator twice')
        self.shape = shape #####@property
        self.color = color

    def __str__(self):#####ghi đè 
        return f'{self.shape} has the color {self.color}'

class Decorator(Shape):######pizza decore _abstract
    def __init__(self, shape):
        # if isinstance(shape, ColoredShape):#####ngăn decore 2 lần 
        #     raise Exception('Cannot apply ColoredDecorator twice')
        self.shape = shape #####@property

    def __str__(self):#####ghi đè 
        return f'{self.shape} has the color'

class TransparentShape(Shape):
    def __init__(self, shape, transparency):
        self.shape = shape
        self.transparency = transparency

    def __str__(self):
        return f'{self.shape} has {self.transparency * 100.0}% transparency'

class ConcreteDecoratorA(Decorator):#####pizza hạt tiêu cài abstract
    """
    Decorators can execute their behavior either before or after the call to a
    wrapped object.
    """
    def __init__(self, *args, **kwargs):################ ko có cũng đc 
        super().__init__(*args, **kwargs)####################ko có cũng đc 
    def __str__(self) -> str:
        return f"ConcreteDecoratorA({self.shape})"


class ConcreteDecoratorB(ColoredShape):#####pizza hạt tiêu cài abstract
    """
    Decorators can execute their behavior either before or after the call to a
    wrapped object.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __str__(self) -> str:
        return f"ConcreteDecoratorB({self.shape})"

if __name__ == '__main__':
    circle = Circle(2)
    print(circle)

    red_circle = ColoredShape(circle, "red")
    print(red_circle)

    # ColoredShape doesn't have resize()
    # red_circle.resize(3)

    red_half_transparent_square = TransparentShape(red_circle, 0.5)
    print(red_half_transparent_square)

    # nothing prevents double application
    mixed = ColoredShape(ColoredShape(Circle(3), 'red'), 'blue')
    print(mixed)
    
    # trộn 2 decor
    mixed = TransparentShape(ColoredShape(Circle(3), 'red'), 0.5)
    print(mixed)
    
    ##### gọi instance
    mixed=ConcreteDecoratorA(Circle(3))
    print(mixed)
    
    
    ##### gọi instance
    mixed=ConcreteDecoratorB(ColoredShape(Circle(3), 'red'),'blue')
    print(mixed)
    
