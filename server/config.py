import json5
with open("config.json",'r')as f:
    js=json5.load(f)
import os
env=os.getenv("autovnc")
config=js.get(env) or js.get("dev")
print(f"env={env} config={config}")