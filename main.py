import pickle
import package

object = package.file_reader('valid.txt')
data = object.get_data()
package.quick_sort(data)

with open('sample.pickle', 'wb') as f:
    pickle.dump(object, f)
f.close()

with open('sample.pickle', 'rb') as f:
    obj_2 = pickle.load(f)
f.close()

data_2 = obj_2.get_data()

f = open('sorted.txt', 'w', encoding='utf-8')
for i in data_2:
    f.write(str(i) + "\n")
f.close()
