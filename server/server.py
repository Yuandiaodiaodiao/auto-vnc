import tornado.ioloop
import tornado.web
import os
import yaml
import json
import dbtest
import time

SERVERIP = 'ip.oops-sdu.cn'
SERVERPORT = 9006
vncport = "80"
# datajs = dict()


with open("dockerUse.json", 'r')as f:
    datajs = json.load(f)

usedPort = set()
for i in datajs:
    usedPort.add(datajs[i]["port"])


def loaddata():
    global datajs
    with open("dockerUse.json", 'r')as f:
        datajs = json.load(f)
    global usedPort
    usedPort = set()
    for i in datajs:
        usedPort.add(datajs[i]["port"])


def savedata():
    with open("dockerUse.json", 'w')as f:
        json.dump(datajs, f, indent=4)


def keepAlive(username):
    if username in datajs:
        datajs[username]['ttl'] = int(time.time())


def adddocker(username, port):
    global vncport
    pathYml = "docker-compose-model.yml"
    with open(pathYml, 'r')as f:
        yml = yaml.load(f)
    yml["services"]["novnc"]["container_name"] = f"autovnc-{username}"
    yml["services"]["novnc"]["ports"] = [f'{port}:{vncport}']
    filename = f"docker-{username}.yml"
    try:
        os.makedirs(f"./{username}")
    except:
        pass
    filepath = f"./{username}/{filename}"
    with open(filepath, 'w')as f:
        yaml.dump(yml, f)
    os.system(f"docker-compose -f {filepath} up -d ")
    saveUse(username, port)
    print("finish")



def deletedocker(username):
    if username not in datajs.keys():
        return True
    port = datajs[username]['port']
    usedPort.remove(port)
    datajs.pop(username)
    for root, dir, file in os.walk(top='./'):
        if root == './' + username:
            for name in file:
                if name.endswith(".yml") and "model" not in name:
                    print('find')
                    os.system(f"docker-compose -f {os.path.join(root, name)} rm -s -f")
                    break
                    # os.remove(os.path.join(root, name))
        else:
            continue


def getCanUse(username):
    if ifopen(username):
        return ifopen(username)
    else:
        for i in range(9007, 10000):
            if i not in usedPort:
                adddocker(username, i)
                return i


def ifopen(username):
    if username in datajs.keys():
        return datajs[username]['port']
    return False


def saveUse(username, port):
    usedPort.add(port)
    datajs[username] = {
        "port": port
    }


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('./dist/index.html')


class addDesktop(tornado.web.RequestHandler):
    def set_default_header(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    def post(self):
        self.set_default_header()
        js = json.loads(self.request.body)
        username = js['username']
        if len(username) < 1:
            self.write(json.dumps({'isok': False}))
        loaddata()
        port = getCanUse(username)
        retJs = {
            "link": f"http://{SERVERIP}:{port}/#/",
            "dockerStatus": datajs,
        }
        savedata()
        self.write(json.dumps(retJs))


class login(tornado.web.RequestHandler):
    def set_default_header(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    def post(self):
        self.set_default_header()
        js = json.loads(self.request.body)
        username = js['username']
        pwd = js['password']

        retJs = {
            'isok': dbtest.login(username, pwd)
        }
        self.write(json.dumps(retJs))


class status(tornado.web.RequestHandler):
    def set_default_header(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    def get(self):
        self.set_default_header()
        # js = json.loads(self.request.body)
        loaddata()
        retJs = {
            "dockerStatus": datajs,
        }
        self.write(json.dumps(retJs))


class delete(tornado.web.RequestHandler):
    def set_default_header(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    def post(self):
        self.set_default_header()
        js = json.loads(self.request.body)
        loaddata()
        deletedocker(js['username'])
        savedata()
        retJs = {
            "isok": True,
        }
        self.write(json.dumps(retJs))


class live(tornado.web.RequestHandler):
    def set_default_header(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    def post(self):
        self.set_default_header()
        js = json.loads(self.request.body)
        loaddata()
        print('alive'+str(js))
        keepAlive(js['username'])
        savedata()
        retJs = {
            "isok": True,
        }
        self.write(json.dumps(retJs))


settings = {
    "static_path": "./dist/static",
}

def clearworker():
    def deldocker(username):
        for root, dir, file in os.walk(top='./'):
            if root == './' + username:
                for name in file:
                    if name.endswith(".yml") and "model" not in name:
                        os.system(f"docker-compose -f {os.path.join(root, name)} rm -s -f")
                        return
    while True:
        with open("dockerUse.json", 'r')as f:
            datajs = json.load(f)
        # print(datajs)
        # print(int(time.time()))
        for username in datajs:
            if 'ttl' in datajs[username]:
                if time.time()-datajs[username]['ttl']>100:
                    datajs.pop(username)
                    deldocker(username)
                    break
        with open("dockerUse.json", 'w')as f:
            json.dump(datajs, f, indent=4)
        time.sleep(10)


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.Process(target=clearworker).start()

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/add", addDesktop),
        (r"/api/login", login),
        (r"/api/status", status),
        (r"/api/delete", delete),
        (r"/api/live", live),
    ], **settings)
    application.listen(SERVERPORT)
    print(f"open at http://{SERVERIP}:{SERVERPORT}")
    tornado.ioloop.IOLoop.current().start()
