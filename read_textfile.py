import pprint

line_number =None
total_array =[]
sensor_dict={}

time_dict= {}
cal_dict ={} #sum , count , mpa,
numPlot =7

for i in range(0,numPlot):
    sensor_dict['S'+str(i+1)] =[]
time = None
machine_number= 0

with open('test.txt','r' ,encoding='utf-8') as file:
    line =None
    while line !='':
        line =file.readline()
        if(line =='\n'):
            continue;
        else:
            if (line.find('TXS_')>=0):
                line_number =int(line[4:].replace(",",""))
                continue
            if (line.find('Ready')>=0):
                continue
            if (line.find('Measure')>=0):
                continue
            if (line.find('Result')>=0):
                continue
            if(line ==''):
                continue

            line = line.strip("\n")
            total_array.append(line)


print(total_array)
print("\n\n\n\n\n\n\n\n")
num = 1
for items in total_array:
    if(num <=line_number-3):
        item = items.split(",")[2:] #time이랑 machine number는 제외하고 출력
        for i in range(0, numPlot):
            sensor_dict['S' + str(i+1)].append(item[i].split(":")[1])
    else:
        item = items.split(",")
    print(item, "  line number", num)
    num = num + 1
num =0
print(sensor_dict)

# T:9694,0,S1:20850,S2:0,S3:0,S4:0,S5:0,S6:0,S7:0',

for items in total_array:
    item = items.split(",")
    print(len(item))
    if (num < line_number - 3):
        time = item[0]
        machine = item[1]
        sensor_data = item[2:]
        time_dict[time] ={}
        for i in range(0, numPlot):
            time_dict[time]['S' + str(i + 1)] ={}
            time_dict[time]['S' + str(i+1)] = sensor_data[i].split(":")[1]

    else:
        print(item)
    num = num + 1

print(time_dict)