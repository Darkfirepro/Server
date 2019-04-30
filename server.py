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

        def db_operation(_tables):
            result_query = exist_or_not(data_want, _tables)
            if result_query == False or result_query == None:
                addSession(data_want, _tables)
            else:
                old_data_orm = query_getHash(data_want, _tables)
                if str(hash(json.dumps(data_want).encode("utf-8"))) != old_data_orm:
                    for client in ClientInt.listC:
                        socket.sendto(data, client)  
                    updateSession(data_want, _tables)  

        try:
            data = self.request[0]
            socket = self.request[1]
            if len(data) < 25:
                if data.strip().decode("utf-8") != "QUIT now":
                    ClientInt.listC.append(self.client_address)
                    
                    print("{} ({}) {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), self.client_address, " send:"))
                    print(data.strip().decode("utf-8")) 

                    for client in ClientInt.listC:
                        socket.sendto(data, client)

                else:
                    ClientInt.listC.remove(self.client_address)
                    print(self.client_address, "has disconnected!")

                    for new_client in ClientInt.listC:
                        socket.sendto("{} has disconnected from this system".format(self.client_address), new_client)

            elif len(data) > 50:
                print("get data now")
                data_want = json.loads(data.decode("utf-8"))
                if data_want["header"] == "ps":
                    del data_want["header"]
                    db_operation("ps")
                elif data_want["header"] == "pds":
                    del data_want["header"]
                    db_operation("pds")
            
        except:
            pass


if __name__ == "__main__":
    HOST, PORT = '', 6666
    server = socketserver.ThreadingUDPServer((HOST, PORT), MyUDPHandler)
    print("Waiting for connection......")
    server.serve_forever()



