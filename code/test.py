x = [0, 1, 2, 3, 4, 5]

def index(y):
    y += 1
    y = y % (len(x) + 1)
    y = y - 1
    return y


for i in range(0, 10):
    print(index(i))
