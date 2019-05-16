import socketserver
from time import gmtime, strftime
import time
import ClientInt
import json
import pymysql
from ClientInt import addSession, querySession, updateSession, deleteSession, exist_or_not, query_getHash, sync_plant_set, sync_plant_infor
import threading
import struct


ip_port = ('', 6666)

class MyTCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        print("{}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())), self.client_address," has connected! ")
        #ClientInt.listC.append(self.client_address)
        ClientInt.listC.append(self.request)

        def db_operation(_tables):
            result_query = exist_or_not(data_want, _tables)
            if result_query == False or result_query == None:
                addSession(data_want, _tables, data)
                for socket1 in ClientInt.listC:
                        print(socket1)
                        socket1.send(data + b'<EOF>') 
            else:
                if _tables != "wa":
                    old_data_orm = query_getHash(data_want, _tables)
                    if str(hash(data)) != old_data_orm:
                        for socket1 in ClientInt.listC:
                            if socket1 != socket:
                                print(socket1)
                                socket1.send(data + b'<EOF>')  
                        updateSession(data_want, _tables, data)
                else:
                    updateSession(data_want, _tables, data)

        while True:
            try:
                data = self.request.recv(1024)
                print(b'test here' + data)
                socket = self.request
                addr = self.client_address
                if not data:
                    try:
                        ClientInt.listC.remove(self.request)
                        socket.close()
                    except:
                        pass
                    print("{}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())), addr, "has disconnected")

                else:
                    recv_str = data.decode("utf-8")
                    ClientInt.temp_str += recv_str
                    if ClientInt.temp_str[-5:] == "<EOF>":
                        obj_list = ClientInt.temp_str.strip("<EOF>").split("<EOF>")
                        ClientInt.temp_str = ""

                        for obj in obj_list:
                            data_want = json.loads(obj)
                            if data_want["header"] == "ps":
                                del data_want["header"]
                                db_operation("ps")

                            elif data_want["header"] == "pds":
                                del data_want["header"]
                                db_operation("pds")

                            elif data_want["header"] == "wa":
                                print(data_want["data"])

                            elif data_want["header"] == "msg":
                                
                                if data_want["msg"] == "NeedToSyncPlantSet":
                                    list_plant_set = sync_plant_set()
                                    for ps in list_plant_set:
                                        socket.sendto(ps[0] + b'<EOF>', addr)
                                        print("send plant set:" + str(len(ps[0] + b'<EOF>')))

                                elif data_want["msg"] == "NeedToSyncPlantInfor":
                                    list_plant_infor = sync_plant_infor()
                                    for pi in list_plant_infor:
                                        pi_dict = {}
                                        pi_dict["header"] = "pds_sync"
                                        pi_dict["singNameId"] = pi.sp_name + "|" + str(pi.sp_id)
                                        pi_dict["param1"] = pi.sp_param1
                                        pi_dict["param2"] = pi.sp_param2
                                        pi_dict["param3"] = pi.sp_param3
                                        pi_dict_bytes = json.dumps(pi_dict).encode("utf-8")
                                        socket.sendto(pi_dict_bytes + b'<EOF>', addr)
                                        print("send plant details:" + str(len(pi_dict_bytes + b'<EOF>')))

                                elif data_want["msg"] == "ClientShutDown":
                                    socket.shutdown(socket.SHUT_RD)

            except Exception as e:
                socket.close()
                print(e)
                break

            
if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(ip_port,MyTCPServer)
    print("Waiting for connection......")
    server.serve_forever()
