import subprocess
import os
import time
import sys
from pymongo import MongoClient


class Mongod(object):
    def __init__(self):
        self.connect = False

    def log(self, text):
        print((len(text) * "═") + "═╗", '\n' +
              text + ' ║\n' + (len(text) * "═") + "═╝\n")

    def start(self):
        self.process = subprocess.Popen('mongod')
        time.sleep(1)
        text = "mongod started"
        self.log(text)

    def stop(self):
        self.process.kill()
        time.sleep(1)
        text = "mongod stopped"
        self.log(text)

    def findData(self, _id, collaction=None, collactionName=None):
        neededToClose = self.startMongod()
        if not collaction:
            collaction = self.collaction
        data = collaction.find_one({"_id": _id})
        if neededToClose:
            self.stopMongod()
        if data and str(data["_id"]) == str(_id):
            return data
        return False

    def add_data(self, data, collactionName):
        neededToClose = self.startMongod()
        collaction = self.collaction
        if not self.findData(_id=data["_id"], collaction=collaction):
            collaction.insert_many([data])
            print("item added successfully")
        else:
            print("allready exists")
        if neededToClose:
            self.stopMongod()

    def passwordOf(self, _id, pk=False):
        neededToClose = self.startMongod()
        collaction = self.collaction
        data = self.findData(_id=_id, collaction=collaction)
        if neededToClose:
            self.stopMongod()
        if data:
            if pk:
                return data['pk']
            return data['password']

    def pkOf(self, _id):
        return self.passwordOf(_id, pk=True)

    def updatePassword(self, user_name, new_password):
        neededToClose = self.startMongod()
        collaction = self.collaction
        query = {"_id": user_name}
        new_user = {"$set": {"password": new_password}}
        collaction.update_one(query, new_user)
        self.client.close()
        if neededToClose:
            self.stopMongod()

    def updateUserName(self, user_name, new_user_name):
        neededToClose = self.startMongod()
        collaction = self.collaction
        if not self.findData(user_name, collaction=collaction):
            print("user don't exists")
            return
        if self.findData(new_user_name, collaction=collaction):
            print("user allready exists")
            return
        data = collaction.find_one({"_id": user_name})
        data["_id"] = new_user_name
        data["user_name"] = new_user_name
        collaction.delete_one({"_id": user_name})
        collaction.insert_one(data)
        if neededToClose:
            self.stopMongod()

    def startMongod(self):
        if not self.connect:
            self.start()
            self.connect = True
            client = self.client = MongoClient()
            self.db = db = client['InstaFollow']
            self.collaction = db['clients']
            return True

    def stopMongod(self):
        self.connect = False
        self.client.close()
        self.stop()

    def updateUsersToUnfollow(self, user_name, users, add=True):
        neededToClose = self.startMongod()
        collaction = self.collaction
        data = self.findData(user_name, collaction=collaction)
        if not data:
            print("user not found")
            return
        if "usersToUnfollow" in data and add:
            users += [tuple(i) for i in data["usersToUnfollow"]]
            users = list(set(users))
        users = [list(i) for i in users]
        print(users)
        query = {"_id": user_name}
        new_user = {"$set": {"usersToUnfollow": users}}
        collaction.update_one(query, new_user)
        time.sleep(1)
        if neededToClose:
            self.stopMongod()


# used exam

# m = Mongod()
# m.add_data({"_id" : "mor_bargig", "user_name": "mor_bargig" , "pk" : 873268 },"clients")
# print(m.updateUsersToUnfollow("mor_bargig", [("Aran", 12345678, False)]))
# m.add_data({"_id" : "mor_bargig", "user_name": "mor_bargig" , "pk" : 873268 },"clients")
# print(m.updateUsersToUnfollow("mor_bargig",[("Sarel",31338027,False)] ))
# m.add_data({"_id" : "mor_bargig", "user_name": "mor_bargig" , "pk" : 873268 },"clients")
