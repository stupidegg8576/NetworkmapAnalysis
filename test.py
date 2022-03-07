a = {
    'asd' : 3,
    'qweq' : 4,
    'zxczx' :1
}


t = sorted(a.items(),key= lambda item: item[1], reverse=True)
t = dict(t)
print(t)
print(type(t))
