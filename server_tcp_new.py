import socketserver
from time import gmtime, strftime
import time
import ClientInt
import json
#import pymysql
from ClientInt import querySession, deleteSession, UpdateNavigationTable, sync_loc_camera, UpdateAnchorPosTable
import threading
import struct
import socket as sk


ip_port = ('', 6666)

class MyTCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        print("{}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())), self.client_address," has connected! ")
        #ClientInt.listC.append(self.client_address)
        ClientInt.listC.append(self.request)

        while True:
            try:
                data = self.request.recv(81920)
                #print(b'test here' + data)
                socket = self.request
                addr = self.client_address
                if not data:
                    try:
                        ClientInt.listC.remove(self.request)
                        socket.shutdown(sk.SHUT_RDWR)
                        socket.close()  
                    except:
                        pass
                    print("{}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())), addr, "has disconnected")
                    break

                else:
                    try:
                        recv_str = data.decode('ascii')
                        ClientInt.temp_str += recv_str
                        #print(ClientInt.temp_str)
                        if ClientInt.temp_str[-5:] == "<EOF>":
                            obj_list = ClientInt.temp_str.strip("<EOF>").split("<EOF>")
                            ClientInt.temp_str = ""
                            for obj in obj_list:
                                data_want = json.loads(obj)
                                if data_want["header"] == "AnchorRequire":
                                    rf = open("wa_data", 'rb')
                                    content = rf.read(8196)
                                    print("try to send world anchor")
                                    times = 0
                                    while content:
                                        socket.send(content)
                                        content = rf.read(8196)
                                        times += len(content)
                                        #print("send :" + str(times))
                                    rf.close()
                                    print("all bytes has been sent")

                                elif data_want["header"] == "NaviData":
                                    UpdateNavigationTable(data_want, obj)

                                elif data_want["header"] == "AnchorInfo":
                                    UpdateAnchorPosTable(data_want)

                                elif data_want["header"] == "msg":
                                    print(data_want["msg"])
                                    if (data_want["msg"] == "SyncLocation"):
                                        navi_data_list = sync_loc_camera()
                                        sd = b''
                                        for navi_ins in navi_data_list:
                                            socket.send(navi_ins.p_data)
                                        print("send all the location data to client!")

                    except UnicodeDecodeError:
                        ClientInt.temp_byte += data
                        if ClientInt.temp_byte[-5:] == b'<EOF>':
                            print("World Anchor received")
                            print("the length of the anchor: " + str(len(ClientInt.temp_byte)))
                            f = open("wa_data", 'wb')
                            f.write(ClientInt.temp_byte)
                            f.close()
                        # print("World Anchor received")
                        # print("the length of the anchor: " + str(len(recv_str)))
                        # f = open("wa_data", 'wb')
                        # f.write(recv_str.encode('ascii') + b'<EOF>')
                        # f.close()



            except Exception as e:
                socket.close()
                print(e)
                break

            
if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(ip_port,MyTCPServer)
    print("Waiting for connection......")
    server.serve_forever()
