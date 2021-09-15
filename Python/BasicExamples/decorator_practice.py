import functools

def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        #aux = '<b/>'+ str(*args)+ '</b>'
        func(*args, **kwargs)
        #func(aux,**kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def say_hello(name):
    print("Hello %s" %name)

say_hello("Bob")
help(say_hello)
help(do_twice)
