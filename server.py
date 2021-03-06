import socket
import json
from firebase import firebase

firebase = firebase.FirebaseApplication('https://senior-project-iot-7c771.firebaseio.com', None)


HOST = 'localhost'  # IP ของ server
PORT = 5432         # port ที่จะใช้ในการติดต่อ

# สร้าง socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# กำหนดข้อมูลพื้นฐานให้กับ socket object
s.bind((HOST, PORT))

# สั่งให้รอการเชื่อมต่อจาก client
s.listen()

 
while True:
    # รอการเชื่อมต่อจาก client
    print("waiting for connection")
 
    # จากข้อ 5 : รับการเชื่อมต่อจาก client
    connection, client_address = s.accept()

    try:
        print("connection from", client_address)
        connection.sendall(b'Enter PATH to access your DATA ->>')
 
        # รับข้อมูลจาก client
        while True:
            # กำหนดขนาดข้อมูลที่จะรับใน recv()//แปลง byte เป็น String เพื่อ print
            data = connection.recv(1024)
            print("received:", data.decode("utf-8"))

            # ถ้ามีข้อมูลส่งเข้ามาให้ส่งกลับไปหา client
            if data:
                data = firebase.get('/'+ str(data,"utf-8"),'')
                print("sending data back to the client")

                #แปลง json เป็น byte เพื่อส่งให้ client
                data = json.dumps(data,indent=2 ).encode("utf-8")
                connection.sendall(data)
                              
            # ถ้าไม่มีข้อมูลให้จบการรอรับข้อมูล
            else:
                print("no more data from", client_address)
                break
    
    # รับข้อมูลเสร็จแล้วทำการปิดการเชื่อมต่อ
    finally:
        connection.close()
        print("closed connection")