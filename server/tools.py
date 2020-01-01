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
        for name in dir:
            os.removedirs(os.path.join(root, name))


clear()
