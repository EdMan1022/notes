import time

def timer(func):
    def f(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        print("{.__name__} took {} seconds".format(func, time.time() - start))
        return rv
    return f

@timer
def add(x, y):
    return x + y

@timer
def sub(x, y):
    return x - y

print(add(5, 6))
print(sub(8, 9))
