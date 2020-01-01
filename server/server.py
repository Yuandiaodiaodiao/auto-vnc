import tornado.ioloop
import tornado.web
import os
import yaml
import json
vncport="6080"
datajs = dict()
with open("dockerUse.json", 'r')as f:
    datajs = json.load(f)

usedPort = set()
for i in datajs:
    usedPort.add(datajs[i]["port"])

def adddocker(username,port):
    global vncport
    pathYml = "docker-compose-model.yml"
    with open(pathYml, 'r')as f:
        yml = yaml.load(f)
    yml["services"]["novnc"]["container_name"] = f"novnc-{username}"
    yml["services"]["novnc"]["ports"] = [f'{port}:{vncport}']
    filename = f"docker-{username}.yml"
    os.makedirs(f"./{username}")
    filepath=f"./{username}/{filename}"
    with open(filepath, 'w')as f:
        yaml.dump(yml, f)
    os.system(f"docker-compose -f {filepath} up -d ")
    saveUse(username,port)
    print("finish")

def getCanUse(username):
    if ifopen(username):
        return ifopen(username)
    else:
        for i in range(9007, 9010):
            if i not in usedPort:
                adddocker(username,i)
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
    with open("dockerUse.json", 'w')as f:
        json.dump(datajs, f, indent=4)


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
        port = getCanUse(username)
        retJs = {
            "link": f"http://ip.oops-sdu.cn:{port}/#/",
            "dockerStatus":datajs,
        }
        self.write(json.dumps(retJs))


settings = {
    "static_path": "./dist/static",
}

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/add", addDesktop),
    ], **settings)
    application.listen(9006)
    print(f"open at http://ip.oops-sdu.cn:9006")
    tornado.ioloop.IOLoop.current().start()
