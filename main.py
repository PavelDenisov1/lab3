import pickle
from file_reader import file_reader
from sort import quick_sort

object = file_reader('valid.txt')
data = object.get_data()
quick_sort(data)

f = open('sorted.txt', 'w', encoding='utf-8')
for i in data:
    f.write(str(i) + "\n")
f.close()
