import serial.tools.list_ports
import serial
import time
import signal
import threading

line = [] #라인 단위로 데이터 가져올 리스트 변수

port = 'COM51'
baud = 115200
list=[]
meaBool =False
exitThread = False   # 쓰레드 종료용 변수

file_path=""
file_name ="test.txt"

start_time=None
end_time=None

#연결 가능한 port list 출력
def printPort():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)

    print("Connected COM Ports : " + str(connected))

#thread 종료용 signal function
def handler(signum, frame):
     exitThread = True

#데이터 처리 함수
def parsing_data(data):
    tmp = ''.join(data)  # list로 들어 온 것을 스트링으로 합침
    print(tmp)
    return tmp

#측정된 데이터 센서 값 출력 하고 list에 저장하기
def sensor_parsing_data(data):
    global list
    tmp = ''.join(data)
    print(tmp)
    list.append(tmp)
    return tmp

#본 thread
def readThread(ser):
    global line, exitThread,meaBool,list,start_time,end_time

    # thread가 종료될때까지
    # Serial interfacce :  data를 stream으로 바꿔서 (직렬화,serialization) 한 번에 1 bit 씩 전송

    f = open("test.txt", 'w')

    while not exitThread:
        #데이터가 있있다면
        for c in ser.read():
            line.append(chr(c))  #(integer, 0 ~ 255)를 ASCII character로 변환하고 line에 추가한다.

            if c == 10: #ASCII의 개행문자 10
                readystr = parsing_data(line)


                if(readystr =='xbee is ready?\r\n'):
                    ser.write(b'x')

                if (readystr.find('TXS_') >= 0):
                    start_time = time.time()
                    ser.write(b'R')
                    meaBool =True

                if (readystr.find('Send confirm message(A, F)') >= 0):
                    ser.write(b'F')
                    print(meaBool)
                    meaBool =False

                if (not meaBool and readystr.find('Ready') >= 0):
                    f.close()
                    end_time = time.time()
                    print("working time: {} sec".format(end_time - start_time))
                    print('text close')
                    meaBool = False

                if(meaBool):
                    readystr = sensor_parsing_data(line)
                    if(readystr =='\n'):
                        continue;
                    else:
                        readystr =readystr.strip('\n')
                        f.write(readystr)


                del line[:] #line list 원소를 다 지워버린다.


if __name__ == "__main__":
    #종료 signal 등록
    signal.signal(signal.SIGINT, handler)
    printPort()
    #시리얼 열기
    ser = serial.Serial(port, baud, timeout=0)
    print(ser.port)
    #serial 읽을 thread 생성
    thread = threading.Thread(target=readThread, args=(ser,))
    thread.start()


