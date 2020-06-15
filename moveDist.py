import shutil
try:
    shutil.rmtree("./server/dist")
except:
    pass
shutil.copytree("./dist","./server/dist")