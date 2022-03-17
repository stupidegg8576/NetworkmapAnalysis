import yaml

with open('test.yaml','r') as a:
    data = yaml.load(a, Loader=yaml.CLoader)

for i in data:
    i = i.lower()
    print(i)



