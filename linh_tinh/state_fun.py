# #####interface của các method VD fly, driving sẽ cài đặt
# #####1 abstract có phươg thức set algo

# # # nhóm 3
# # class pointer():
# #     value=1


# # def observedfunction1():
# #     if ("helicopstate"):
# #         print("bảo trì trên trời")
# #     if ("streetracerstate"):
# #         print("bảo trì dưới đất")

# # def observedfunction2needcall():
# #     if ("helicopstate"):
# #         print("đang bay trên trời")
# #     if ("streetracerstate"):
# #         print("đang chạy dưới đất")

# # # index=0
# # # a=("streetracer", deepcopy(index),[observedfunction1, observedfunction2needcall])
# # x = pointer() 
# # a=(["streetracerstate", "helicopstate"], x,[observedfunction1, observedfunction2needcall])
# # a[2][a[1].value]()

# # # index=1
# # x.value= 0
# # a[2][a[1].value]()



# ##### áp dụng state
# # nhóm 3
# class pointer():
#     value=1


# def observedfunction1():
#     state.observedfunction1()

# def observedfunction2needcall():
#     state.observedfunction2needcall()

# ############# đẩy việc cho state pointer
# streetracerstate.observedfunction1="bảo trì dưới mặt đất"
# streetracerstate.observedfunction2needcall="đang chạy dưới mặt đất"

# helicopstate.observedfunction1="bảo trì trên trời"
# helicopstate.observedfunction2needcall="đang chạy trên trời"
# # index=0
# # a=("streetracer", deepcopy(index),[observedfunction1, observedfunction2needcall])
# x = pointer() 
# a=(["streetracerstate", "helicopstate"], x,[observedfunction1, observedfunction2needcall])
# a[2][a[1].value]()

# # index=1
# x.value= 0
# a[2][a[1].value]()


# #####just pseudo chưa chạy đc



class Context:
    def __init__(self, state):
        self.transition_to(state)

    def transition_to(self, state):
        print(f"Context: Transition to {type(state).__name__}.")
        self._state = state
        self._state.set_context(self)

    def request1(self):
        self._state.handle1()

    def request2(self):
        self._state.handle2()

class State:
    def set_context(self, context):
        self._context = context

    def handle1(self):
        raise NotImplementedError

    def handle2(self):
        raise NotImplementedError

class ConcreteStateA(State):
    def handle1(self):
        print("ConcreteStateA handles request1.")
        print("ConcreteStateA wants to change the state of the context.")
        self._context.transition_to(ConcreteStateB())

    def handle2(self):
        print("ConcreteStateA handles request2.")

class ConcreteStateB(State):
    def handle1(self):
        print("ConcreteStateB handles request1.")

    def handle2(self):
        print("ConcreteStateB handles request2.")
        print("ConcreteStateB wants to change the state of the context.")
        self._context.transition_to(ConcreteStateA())

def main():
    context = Context(ConcreteStateA())
    context.request1()
    context.request2()

if __name__ == "__main__":
    main()

# https://www.codeconvert.ai/csharp-to-python-converter
# https://viblo.asia/p/strategy-design-pattern-tro-thu-dac-luc-cua-developers-bJzKmdwP59N