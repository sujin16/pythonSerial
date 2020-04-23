import numpy as np

num = 0
z_min = 0
z_max = 40
num_frame = 100
min_value =0
max_value =80
def read_temp():
    global num
    if (num < num_frame):
        num = num + 1
        temp= []
        for i in range(0,7):
            temp.append(np.random.randint(max_value) +min_value)

        #print('num : '+str(num)+ '  '.join(str(e) for e in temp))

    if (num >= num_frame):
        temp = None

    return temp
