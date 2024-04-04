# Bridge, State, Strategy có cấu trúc rất giống nhau. Tất cả các pattern này đều dựa trên bố cục, giao công việc nào đó cho các object khác. Tuy nhiên, chúng đều giải quyết các vấn đề khác nhau.
# https://cppdeveloper.com/design-patterns/design-patterns-8-state-pattern/
# robot với 4 trạng thái, khi có khách đến,  hàm nào cũng phải check xem state hiện tại là state nào trong 4 cái state kia để đưa ra action tương ứng. VD  void getForm() lại if else , void rentApartment(), void checkForm(), void dispenseKeys() 4 if else
# SOLUTION sử dụng object để đóng gói state lại thay vì lưu state bằng một biến , mỗi state 1 class khi đó: RentalRobot robot(10) #ko biết state~ random; robot.getForm();
# sử dụng một con trỏ state trỏ đúng vào cái state object tương ứng với trạng thái hiện tại và call các method thông qua con trỏ đó.
# khác vs strategy thì state nội bộ của nó thay đổi, VD thêm 1 state mới

# https://www.codeconvert.ai/java-to-python-converter



class RentalRobot:
    def __init__(self, count):
        self.mCount = count
        self.mWaitingState = WaitingState(self)
        self.mReceivingFormState = ReceivingFormState(self)
        self.mRentApartmentState = RentApartmentState(self)
        self.mFullyRentedState = FullyRentedState(self)
        self.mCurentState = self.mWaitingState
        # self.mCurentState =random.choice([self.mWaitingState,self.mReceivingFormState,self.mRentApartmentState,self.mFullyRentedState   ])

    def __del__(self):
        if self.mWaitingState is not None:
            del self.mWaitingState
            self.mWaitingState = None

        if self.mReceivingFormState is not None:
            del self.mReceivingFormState
            self.mReceivingFormState = None

        if self.mRentApartmentState is not None:
            del self.mRentApartmentState
            self.mRentApartmentState = None

        if self.mFullyRentedState is not None:
            del self.mFullyRentedState
            self.mFullyRentedState = None

        self.mCurentState = None

    def getForm(self):
        self.mCurentState.getForm()

    def checkForm(self):
        self.mCurentState.checkForm()

    def rentApartment(self):
        self.mCurentState.rentApartment()

    def setState(self, state):
        self.mCurentState = state

    def getState(self):
        return self.mCurentState

    def getWaitingState(self):
        return self.mWaitingState

    def getReceivingFormState(self):
        return self.mReceivingFormState

    def getRentApartmentState(self):
        return self.mRentApartmentState

    def getFullyRentedState(self):
        return self.mFullyRentedState

    def getCount(self):
        return self.mCount

    def setCount(self, count):
        self.mCount = count




# class IRentalRobot:
#     def setState(self, state):
#         self.state = state

#     def getReceivingFormState(self):
#         return self.receiving_form_state

#     def getWaitingState(self):
#         return self.waiting_state

#     def getRentApartmentState(self):
#         return self.rent_apartment_state

#     def getFullyRentedState(self):
#         return self.fully_rented_state

#     def getState(self):
#         return self.state

#     def getCount(self):
#         return self.count

#     def setCount(self, count):
#         self.count = count


from abc import ABC, abstractmethod
class IState(ABC):
    @abstractmethod
    def getForm(self):
        pass

    @abstractmethod
    def checkForm(self):
        pass

    @abstractmethod
    def rentApartment(self):
        pass

    @abstractmethod
    def dispenseKeys(self):
        pass


import random
class WaitingState(IState):
    def __init__(self, robot):
        super().__init__()
        
        self.robot = robot
        

    def getForm(self):
        self.robot.setState(self.robot.getReceivingFormState())
        print("Thanks for the form.")

    def checkForm(self):
        print("You have to submit an form.")

    def rentApartment(self):
        print("You have to submit an form.")

    def dispenseKeys(self):
        print("You have to submit an form.")

class ReceivingFormState(IState):
    def __init__(self, robot):
        super().__init__()
        
        self.robot = robot
        self.random_generator = random.SystemRandom()

    def getForm(self):
        print("We already got your application.")

    def checkForm(self):
        # simulate the form checking
        is_form_ok = self.random_generator.randint(0, 9) > 5

        if is_form_ok and self.robot.getCount() > 0:
            print("Congratulations, you were approved.")
            self.robot.setState(self.robot.getRentApartmentState())
            self.robot.getState().rentApartment()
        else:
            self.robot.setState(self.robot.getWaitingState())
            print("Sorry, you were not approved.")

    def rentApartment(self):
        print("You must have your application checked.")

    def dispenseKeys(self):
        print("You must have your application checked.")

class RentApartmentState(IState):
    def __init__(self, robot):
        super().__init__()
        
        self.robot = robot

    def getForm(self):
        print("Hang on, we're renting you an apartment.")

    def checkForm(self):
        print("Hang on, we're renting you an apartment.")

    def rentApartment(self):
        self.robot.setCount(self.robot.getCount() - 1)
        print("Renting you an apartment....")
        self.dispenseKeys()

    def dispenseKeys(self):
        if self.robot.getCount() > 0:
            self.robot.setState(self.robot.getWaitingState())
        else:
            self.robot.setState(self.robot.getFullyRentedState())
        print("Here are your keys!")

class FullyRentedState(IState):
    def __init__(self, robot):
        super(IState, self).__init__()
        
        self.robot = robot

    def getForm(self):
        print("Sorry, we're fully rented.")

    def checkForm(self):
        print("Sorry, we're fully rented.")

    def rentApartment(self):
        print("Sorry, we're fully rented.")

    def dispenseKeys(self):
        print("Sorry, we're fully rented.")




def main():
    robot = RentalRobot(10)
    robot.getForm()
    robot.checkForm()
    return 0

if __name__ == "__main__":
    main()

