import socketserver
from time import gmtime, strftime
import time
import ClientInt
import json
import pymysql
from ClientInt import addSession, querySession, updateSession, deleteSession, exist_or_not, query_getHash
import threading

class MyUDPHandler (socketserver.BaseRequestHandler):

    def handle(self):

        try:
            data = self.request[0]
            socket = self.request[1]

            recv_str = data.decode("utf-8")
            ClientInt.temp_str += recv_str
            #print(len(recv_str))
            if ClientInt.temp_str[-5:] == "<EOF>":
                print("test here get eof")
                obj_list = ClientInt.temp_str.strip("<EOF>").split("<EOF>")
                ClientInt.temp_str = ""

                for obj in obj_list:
                    print(obj)
                    data_want = json.loads(obj)

                    if data_want["header"] == "msg":
                        if data_want["msg"] == "desktop connect":
                            ClientInt.listC.append(self.client_address)
                            print("{}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())), self.client_address, " has connected! ")

                            feedback_msg = json.dumps({"header" : "connection", "msg" : "server received!"}).encode("utf-8")

                            socket.sendto(feedback_msg, self.client_address)

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

                    elif data_want["header"] == "wa":
                        print("World Anchor received")
                        print("the length of the anchor: " + str(len(data_want["data"])))
                        # del data_want["header"]
                        # Add_World_Anchor("wa")
                        contentSend = obj.encode("utf-8") + b'<EOF>'
                        f = open(data_want["spaceName"], 'wb')
                        f.write(contentSend)
                        f.close()

                    elif data_want["header"] == "AnchorRequire":
                        rf = open(data_want["id"], 'rb')
                        content = rf.read(8192)
                        print("try to send world anchor")
                        times = 0
                        while content:
                            print(times)
                            socket.sendto(content, self.client_address)
                            content = rf.read(8192)
                            time.sleep(0.001)
                            times += len(content)
                            # print("send :" + str(times))
                        rf.close()

            
        except:
            pass


if __name__ == "__main__":
    HOST, PORT = '', 6666
    server = socketserver.ThreadingUDPServer((HOST, PORT), MyUDPHandler)
    print("Waiting for connection......")
    server.serve_forever()



