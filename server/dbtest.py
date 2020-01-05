import pymongo
import bcrypt
SERVERIP='101.76.250.242'
SERVERPORT=27017
DBUSR="thinpad_plus_test"
myclient = pymongo.MongoClient(f'mongodb://{SERVERIP}:{SERVERPORT}/')
dblist = myclient.list_database_names()
mydb=myclient[DBUSR]
user=mydb["users"]
def login(username,passwd=''):
    x=user.find_one({"username":str(username)})
    if x is not None and bcrypt.checkpw(passwd.encode('utf-8'),x['password'].encode('utf-8')):
        return True

if __name__=="__main__":
    login('aaa','')
    # dblist = myclient.database_names()
    # for x in dblist:
    #     print(x)
    #
    # password = "admin"
    # print(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=5)).decode('utf-8'))
    # print(bcrypt.gensalt(rounds=5))
    # print(password.encode('utf-8'))
    # for x in user.find():
    #     pwd=x['password']
    #     if bcrypt.checkpw('admin'.encode('utf-8'),pwd.encode('utf-8')):
    #         print(pwd)