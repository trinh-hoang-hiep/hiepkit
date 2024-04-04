# Observed object (also referred to as publisher) https://viblo.asia/p/design-pattern-observer-V3m5WO8W5O7
class Inventory:
    def __init__(self):
        self.observers = []
        self._product = None
        self._quantity = 0
    
    # Attach observer to the inventory object
    # Also known as: attach subscriber to publisher
    def attach(self, observer):#####
        self.observers.append(observer)
    
    # Set product and update observers
    @property
    def product(self):
        return self._product
    @product.setter
    def product(self, value):
        self._product = value
        self._update_observers()##### sửa hàm set = ko cần vòng while
    
    # Set quantity and update observers
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        self._update_observers()
    
    # Call observer to update
    def _update_observers(self):#####
        for observer in self.observers:
            observer()
            
            
            
            
            
# Simple observer object that prints info from observed
class ConsoleObserver:
    def __init__(self, inventory):
        self.inventory = inventory
        
    def __call__(self):
        print(self.inventory.product)
        print(self.inventory.quantity)
        
        
        
# Instance of observed (publisher)
i = Inventory()

# Instance of observer (subscriber)
c = ConsoleObserver(i)

# Attach observer to observed
i.attach(c)#####

# Changes to observed result in call to observer
i.product = "Widget"##### alway, ko cần while do sửa hàm set
i.quantity = 5