# class Buffer:
#   def __init__(self, width=30, height=20):
#     self.width = width
#     self.height = height
#     self.buffer = [' '] * (width*height)

#   def __getitem__(self, item):
#     return self.buffer.__getitem__(item)

#   def write(self, text):
#     self.buffer += text

# class Viewport:
#   def __init__(self, buffer=Buffer()):
#     self.buffer = buffer
#     self.offset = 0

#   def get_char_at(self, index):
#     return self.buffer[self.offset+index]

#   def append(self, text):
#     self.buffer += text

# class Console:
#   def __init__(self):
#     b = Buffer()
#     self.current_viewport = Viewport(b)
#     self.buffers = [b]
#     self.viewports = [self.current_viewport]

#   # high-level
#   def write(self, text):
#     self.current_viewport.buffer.write(text)

#   # low-level
#   def get_char_at(self, index):
#     return self.current_viewport.get_char_at(index)


# if __name__ == '__main__':
#   c = Console()
#   c.write('hello')
#   ch = c.get_char_at(0)

import json

class Flyweight:
    def __init__(self, car):
        self._shared_state = car

    def operation(self, unique_state):
        s = json.dumps(self._shared_state)
        u = json.dumps(unique_state)
        print(f"Flyweight: Displaying shared {s} and unique {u} state.")

from typing import Tuple, List

# class Flyweight:
#     def __init__(self, shared_state: dict):
#         self.shared_state = shared_state

#     def operation(self, unique_state: dict):
#         print(f"Flyweight: Displaying shared ({self.shared_state}) and unique ({unique_state}) state.")

class FlyweightFactory:
    def __init__(self, cars: List[dict]):
        self.flyweights: List[Tuple[Flyweight, str]] = []
        for car in cars:
            self.flyweights.append((Flyweight(car), self.get_key(car)))

    def get_key(self, car: dict) -> str:
        elements = [
            car["Model"],
            car["Color"],
            car["Company"],
            car.get("Number", ""),
            car.get("Owner", "")
        ]
        elements.sort()
        return "_".join(elements)

    def get_flyweight(self, shared_state: dict) -> Flyweight:
        key = self.get_key(shared_state)
        for flyweight, flyweight_key in self.flyweights:
            if flyweight_key == key:
                print("FlyweightFactory: Reusing existing flyweight.")
                return flyweight
        print("FlyweightFactory: Can't find a flyweight, creating new one.")
        new_flyweight = Flyweight(shared_state)
        self.flyweights.append((new_flyweight, key))
        return new_flyweight

    def list_flyweights(self):
        print(f"\nFlyweightFactory: I have {len(self.flyweights)} flyweights:")
        for _, key in self.flyweights:
            print(key)

def add_car_to_police_database(factory: FlyweightFactory, car: dict):
    print("\nClient: Adding a car to database.")
    flyweight = factory.get_flyweight({
        "Color": car["Color"],
        "Model": car["Model"],
        "Company": car["Company"]
    })
    flyweight.operation({
        "Number": car["Number"],
        "Owner": car["Owner"]
    })
if __name__ == "__main__":
    factory = FlyweightFactory([
        {"Company": "Chevrolet", "Model": "Camaro2018", "Color": "pink"},
        {"Company": "Mercedes Benz", "Model": "C300", "Color": "black"},
        {"Company": "Mercedes Benz", "Model": "C500", "Color": "red"},
        {"Company": "BMW", "Model": "M5", "Color": "red"},
        {"Company": "BMW", "Model": "X6", "Color": "white"}
    ])
    factory.list_flyweights()

    add_car_to_police_database(factory, {
        "Number": "CL234IR",
        "Owner": "James Doe",
        "Company": "BMW",
        "Model": "M5",
        "Color": "red"
    })

    add_car_to_police_database(factory, {
        "Number": "CL234IR",
        "Owner": "James Doe",
        "Company": "BMW",
        "Model": "X1",##### add thêm
        "Color": "red"
    })

    factory.list_flyweights()

# https://www.codeconvert.ai/csharp-to-python-converter
# https://viblo.asia/p/flyweight-design-pattern-tro-thu-dac-luc-cua-developers-maGK7B4b5j2