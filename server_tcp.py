import socketserver
from time import gmtime, strftime
import time
import ClientInt
import json
import pymysql
from ClientInt import addSession, querySession, updateSession, deleteSession, exist_or_not, query_getHash
import threading


ip_port = ('', 6666)

class MyTCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        print("{}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())), self.client_address," has connected! ")
        #ClientInt.listC.append(self.client_address)
        ClientInt.listC.append(self.request)

        def db_operation(_tables):
            result_query = exist_or_not(data_want, _tables)
            if result_query == False or result_query == None:
                addSession(data_want, _tables)
                for socket1 in ClientInt.listC:
                        print(socket1)
                        socket1.send(data) 
            else:
                old_data_orm = query_getHash(data_want, _tables)
                if str(hash(json.dumps(data_want).encode("utf-8"))) != old_data_orm:
                    for socket1 in ClientInt.listC:
                        print(socket1)
                        socket1.send(data)  
                    updateSession(data_want, _tables)  

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
                
                elif len(data) > 40:
                    data_want = json.loads(data.decode("utf-8"))
                    if data_want["header"] == "ps":
                        del data_want["header"]
                        db_operation("ps")
                    elif data_want["header"] == "pds":
                        del data_want["header"]
                        db_operation("pds")

            except Exception as e:
                print(e)
                break

            
if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(ip_port,MyTCPServer)
    print("Waiting for connection......")
    server.serve_forever()
