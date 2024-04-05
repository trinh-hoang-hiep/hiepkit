# nhóm 2
def decor_function(origin_function):
    def wrapper_function(*args, **kwargs):
        print("sua doi{}".format(origin_function.__name__))
        return origin_function(*args, **kwargs)#####converted datetime to str 
    return wrapper_function

def display(strA,strB):
    print (strA+strB)

print(display("strA","strB"))
a=decor_function(display)
a("hiep", "design pattern")


#####display=AgeCalculator
#####wrapper_function= DateAgeAdapter