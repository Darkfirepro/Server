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
                socket = self.request
                addr = self.client_address
                if not data:
                    try:
                        ClientInt.listC.remove(self.request)
                        #socket.shutdown(socket.SHUT_RD)
                        socket.close()
                    except:
                        pass
                    print("{}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())), addr, "has disconnected")
                    #break
                
                if len(data) < 40:
                    data_want = data.strip().decode("utf-8")
                    if data_want == "NeedToSyncPlantSet":
                        list_plant_set = sync_plant_set()
                        allbyte_send = b''
                        for ps in list_plant_set:
                            #socket.sendto(ps[0] + b'<EOF>', addr)
                            allbyte_send += ps[0] + b'<EOF>'
                            #time.sleep(0.1)
                        socket.sendto(allbyte_send, addr)
                        print(len(allbyte_send))

                    if data_want == "NeedToSyncPlantInfor":
                        list_plant_infor = sync_plant_infor()
                        allbyte_infor = b''
                        for pi in list_plant_infor:
                            pi_dict = {}
                            pi_dict["header"] = "pds_sync"
                            pi_dict["singNameId"] = pi.sp_name + "|" + str(pi.sp_id)
                            pi_dict["param1"] = pi.sp_param1
                            pi_dict["param2"] = pi.sp_param2
                            pi_dict["param3"] = pi.sp_param3
                            pi_dict_bytes = json.dumps(pi_dict).encode("utf-8")
                            #socket.sendto(pi_dict_bytes + b'<EOF>', addr)
                            allbyte_infor += pi_dict_bytes + b'<EOF>'
                            #time.sleep(0.1)
                        socket.sendto(allbyte_infor, addr)
                        print(len(allbyte_infor))


                
                elif len(data) > 40:
                    print(b'test here' + data)
                    data_want = json.loads(data.decode("utf-8"),)
                    if data_want["header"] == "ps":
                        del data_want["header"]
                        db_operation("ps")
                    elif data_want["header"] == "pds":
                        del data_want["header"]
                        db_operation("pds")
                    elif data_want["header"] == "wa":
                        print(data_want["data"])


            except Exception as e:
                socket.close()
                print(e)
                break

            
if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(ip_port,MyTCPServer)
    print("Waiting for connection......")
    server.serve_forever()
