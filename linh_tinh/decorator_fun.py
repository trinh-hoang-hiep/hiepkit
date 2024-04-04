def decor_function(origin_function):
    def wrapper_function(*args, **kwargs):
        print("sua doi{}".format(origin_function.__name__))
        return origin_function(*args, **kwargs)
    return wrapper_function

def display(strA,strB):
    print (strA+strB)

print(display("strA","strB"))
a=decor_function(display)
a("hiep", "design pattern")







@decor_function
def decor_nowdisplay(strA,strB):
    print (strA+strB)
    
decor_nowdisplay("hiep", "design pattern")