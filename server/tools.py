import os
import yaml
import json


def clear():
    with open("dockerUse.json", 'w')as f:
        f.write("{\n}")
    for root, dir, file in os.walk("./"):
        for name in file:
            print(name)
            if name.endswith(".yml") and "model" not in name:
                os.system(f"docker-compose -f {os.path.join(root, name)} rm -s -f")
                os.remove(os.path.join(root, name))

    for root, dir, file in os.walk("./"):
        try:
            for name in dir:
                os.removedirs(os.path.join(root, name))
        except:
            pass


def delete(username):
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

if __name__=="__main__":
    with open("dockerUse.json", 'r')as f:
        js=json.load(f)
    for dockername in js:
        delete(dockername)
    with open("dockerUse.json", 'w')as f:
        f.write("{\n}")