unit = (14,4)
my_list = [1,2,3,4, unit]
print(my_list)
my_list.remove(unit)
print(my_list)
if 2 in my_list: my_list.remove(2)
print(my_list)

print(26//5)
print(26%5)


data = (0,1,2,3,4,5,6,7,8,9)
for x in range(1, len(data)):
    print("data:", data[x])