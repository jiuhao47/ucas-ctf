from pymongo import MongoClient, errors
from pymongo.collection import Collection
import urllib
import datetime
import os
import socketserver
import pathlib

SOCK_FILE_LOC = os.environ.get("SOCK_FILE_LOC", "/socket/chall.sock")


class DBManager:
    client: MongoClient = None

    def __init__(self):
        self.client = MongoClient(
            f'mongodb://{os.environ.get("DB_USER")}:{urllib.parse.quote(os.environ.get("DB_PW").encode())}@mongo:27017/admin?retryWrites=true&w=majority'
        )

    def add_session(self, session: dict):
        session["create_date"] = datetime.datetime.now(tz=datetime.timezone.utc)
        session["success_date"] = None
        session["flag"] = None
        
        db = self.client["sessions"]
        collection: Collection = db["sessions"]
        collection.insert_one(session)
    
    def check_session(self, session: dict):
        db = self.client["sessions"]
        collection: Collection = db["sessions"]
        result = collection.find_one({"session_id": session["session_id"], "password": session["password"]})
        if result is None:
            return "NOPE"
        
        with open("/flag", "rb") as f:
            flag = f.read()
        
        collection.update_one({"session_id": session["session_id"], "password": session["password"]}, 
                              {"$set": {"flag": flag.decode(), "success_date": datetime.datetime.now(tz=datetime.timezone.utc)}})
        return flag


class ServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        recv_raw_data = self.request.recv(1024).strip().decode()
        recv_data = recv_raw_data.split(",")
        send_data = b""
        try:
            print(recv_data)
            db = DBManager()
            session = {"password": recv_data[1].strip(), "session_id": recv_data[2].strip()}
            if recv_data[0] == "register":
                db.add_session(session)
                send_data = b"OK"
            elif recv_data[0] == "check":
                send_data = db.check_session(session)
        except Exception as e:
            send_data = b"Call Admin!"
            pass
        self.request.sendall(send_data)

class Server(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    pass


if __name__ == "__main__":
    pathlib.Path(SOCK_FILE_LOC).unlink(missing_ok=True)
    with Server(SOCK_FILE_LOC, ServerHandler) as server:
        server.allow_reuse_addess = True
        print("Start Server...")
        server.serve_forever()
    
