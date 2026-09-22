# read mafs script

import os, copy, shutil, sys
if len(sys.argv) == 1:
    f = open("fs.mafs", "r")
    fb = open("fs.mafs", "rb")
else:
    f = open(sys.argv[1], "r")
    fb = open(sys.argv[1], "rb")
c = f.read()
cb = fb.read()
f.close()
fb.close()

drivename = None
files, directories = {}, {}

if c[:4] != "MAFS":
    raise Exception("bro you're mafs is not mafs")
c, cb = c[4:], cb[4:]
drivename = c[:32].strip("\x00")
c, cb = c[33:], cb[33:]
print(f"Name : {drivename}")
while True:
    if c.startswith("\xff"):
        c, cb = c[1:], cb[1:]
        break
    dpid = cb[0]*(64**2) + cb[1]*(64) + cb[2]
    diid = cb[3]*(64**2) + cb[4]*(64) + cb[5]
    dnam = c[6:6+32].strip("\x00")
    directories.update({diid: [dpid, dnam]})
    #print(dnam)
    c, cb = c[6+32:], cb[6+32:]
while True:
    if c.startswith("\xff"):
        c, cb = c[1:], cb[1:]
        break
    if c.startswith("\xef"):
        c, cb = c[1:], cb[1:]
        continue
    fpid = cb[0]*(64**2) + cb[1]*64 + cb[2]
    fnam = c[3:3+32].strip("\x00")
    files.update({fnam: fpid})
    #print(fnam)
    c, cb = c[3+32:], cb[3+32:]
try:
    shutil.rmtree(os.path.join(".", drivename))
except:
    pass
dd = {}
index = 0
os.mkdir(drivename)
directoriess = copy.deepcopy(directories)
directorie = copy.deepcopy(directories)
while directories != {}:
    for k, v in directories.items():
        if v[0] == 0:
            os.mkdir(os.path.join(".", drivename, v[1]))
            dd.update({k: v+[os.path.join(".", drivename, v[1])]})
            directorie.pop(k)
        elif v[0] in list(dd.keys()):
            os.mkdir(os.path.join(dd[v[0]][2], v[1]))
            dd.update({k: v+[os.path.join(dd[v[0]][2], v[1])]})
            directorie.pop(k)
    directories = copy.deepcopy(directorie)
for k, v in files.items():
    if v != 0:
        open(os.path.join(dd[v][2], k), "w").close()
    else:
        open(os.path.join(".", drivename, k), "w").close()
print(f"Directories extracted : {", ".join([i[1] for i in list(directoriess.values())])}")
print(f"Files extracted : {", ".join(list(files.keys()))}")