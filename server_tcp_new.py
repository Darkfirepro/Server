import socketserver
from time import gmtime, strftime
import time
import ClientInt
import json
#import pymysql
from ClientInt import addSession, querySession, updateSession, deleteSession, exist_or_not, query_getHash, sync_plant_set, sync_plant_infor, UpdateLatencyTime
import threading
import struct
import socket as sk


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
                        socket1.send(data) 
            else:
                old_data_orm = query_getHash(data_want, _tables)
                if str(hash(data)) != old_data_orm:
                    for socket1 in ClientInt.listC:
                        #if socket1 != socket:
                        print(socket1)
                        socket1.send(data)  
                    updateSession(data_want, _tables, data)

        def Add_World_Anchor(_tables):
            result_query = exist_or_not(data_want, _tables)
            path_world_anchor = "world_anchor/{}".format(data_want["spaceName"])
            if result_query == False or result_query == None:
                addSession(data_want, _tables, path_world_anchor)
            else:
                updateSession(data_want, _tables, path_world_anchor)
            f = open(path_world_anchor, "w")
            f.write(data_want["data"])
            f.close

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
                    recv_str = data.decode("utf-8")
                    ClientInt.temp_str += recv_str
                    #print(ClientInt.temp_str)
                    if ClientInt.temp_str[-5:] == "<EOF>":
                        obj_list = ClientInt.temp_str.strip("<EOF>").split("<EOF>")
                        ClientInt.temp_str = ""

                        for obj in obj_list:
                            data_want = json.loads(obj)
                            if data_want["header"] == "ps":
                                #del data_want["header"]
                                #db_operation("ps")

                                ###new system upload position:
                                print("recieved plant set")
                                plant_pos_file = open(data_want["Name"], 'wb')
                                plant_pos_file.write(obj.encode("utf-8") + b'<EOF>')
                                plant_pos_file.close()

                            elif data_want["header"] == "TimeCost":
                                if data_want["type"] == "OFALL":
                                    print(data_want["content"])
                                    file_time_ofall = open("OFALL.txt", "a+")
                                    file_time_ofall.write(data_want["content"] + "\r\n")
                                    file_time_ofall.close()
                                if data_want["type"] == "ASA":
                                    print(data_want["content"])
                                    file_time_asa = open("ASA.txt", "a+")
                                    file_time_asa.write(data_want["content"] + "\r\n")
                                    file_time_asa.close()

                            elif data_want["header"] == "pds":
                                del data_want["header"]
                                db_operation("pds")

                            elif data_want["header"] == "wa":
                                print("World Anchor received")
                                print("the length of the anchor: " + str(len(data_want["data"])))
                                #del data_want["header"]
                                #Add_World_Anchor("wa")
                                contentSend = obj.encode("utf-8") + b'<EOF>'
                                f = open(data_want["spaceName"], 'wb')
                                f.write(contentSend)
                                f.close()

                            elif data_want["header"] == "AnchorRequire":
                                rf = open(data_want["id"], 'rb')
                                content = rf.read(1024)
                                print("try to send world anchor")
                                times = 0
                                while content:
                                    socket.send(content)
                                    content = rf.read(1024)
                                    times += len(content)
                                    #print("send :" + str(times))
                                rf.close()
                            
                            ##### test on latency time:
                            elif data_want["header"] == "LatencyTest":
                                UpdateLatencyTime(data_want)
                            ####################################

                            elif data_want["header"] == "msg":
                                
                                if data_want["msg"] == "NeedToSyncPlantSet":
                                    # list_plant_set = sync_plant_set()
                                    # socket.sendto(json.dumps({"header" : "PN", "PlantNumber" : len(list_plant_set)}).encode("utf-8") + b'<EOF>', addr)
                                    # all_bytes_ps = b''
                                    # for ps in list_plant_set:
                                    #     all_bytes_ps += ps[0]
                                    # socket.sendto(all_bytes_ps, addr)
                                    # print("send plant set:" + str(len(all_bytes_ps)))

                                    ###new system upload:
                                    plantset_location_file = open("4_GC35L", 'rb')
                                    content = plantset_location_file.read(1024)
                                    print("try to send plant set location")
                                    times = 0
                                    while content:
                                        socket.send(content)
                                        content = plantset_location_file.read(1024)
                                        times += len(content)
                                        #print("send :" + str(times))
                                    plantset_location_file.close()

                                elif data_want["msg"] == "NeedToSyncPlantInfor":
                                    list_plant_infor = sync_plant_infor()
                                    list_pi_all = b''
                                    for pi in list_plant_infor:
                                        pi_dict = {}
                                        pi_dict["header"] = "pds_sync"
                                        pi_dict["singId"] = pi.sp_id
                                        pi_dict["singName"] = pi.sp_name
                                        pi_dict["param1"] = pi.sp_param1
                                        pi_dict["param2"] = pi.sp_param2
                                        pi_dict["param3"] = pi.sp_param3
                                        pi_dict["showPlant"] = pi.sp_show_plant
                                        pi_dict_bytes = json.dumps(pi_dict).encode("utf-8") + b'<EOF>'
                                        list_pi_all += pi_dict_bytes
                                    socket.sendto(list_pi_all, addr)
                                    print("send plant details:" + str(len(list_pi_all)))

                                ##############test for latency here:
                                elif data_want["msg"][0 : 12] == "SyncPlantNum":
                                    plant_num_sync_string = data_want["msg"].split(':')[1]
                                    plant_num_int = int(plant_num_sync_string)
                                    list_plant_set = sync_plant_set()
                                    all_bytes_ps_latency_test = b''
                                    for count in range(0, plant_num_int):
                                        plant_data = list_plant_set[count]
                                        all_bytes_ps_latency_test += plant_data[0]
                                    socket.sendto(all_bytes_ps_latency_test + b'<EOF>', addr)
                                    print("send plant set locations on number of: " + plant_num_sync_string)
                                ###############################

            except Exception as e:
                socket.close()
                print(e)
                break

            
if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(ip_port,MyTCPServer)
    print("Waiting for connection......")
    server.serve_forever()
