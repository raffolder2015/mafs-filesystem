# write mafs script

import os, sys

directories, files = {}, {}
w = b"MAFS" + bytes(sys.argv[1], "ascii") + b"\x00"*(32-len(sys.argv[1])) + b"\xff"

for dp, dn, fn in os.walk(os.path.join(".", sys.argv[1])):
    #print(dp, dn, fn)
    for i in dn:
        if dp == f".\\{sys.argv[1]}":
            directories.update({max(list(directories.keys()), default=0)+1: [0, i, os.path.join(dp, i)]})
        else:
            directories.update({max(list(directories.keys()), default=0)+1: [list(directories.keys())[[i[1] for i in directories.values()].index(dp)], i, os.path.join(dp, i)]})
    #print(directories)
    for i in fn:
        if dp == f".\\{sys.argv[1]}":
            files.update({i: [0, os.path.join(dp, i)]})
        else:
            files.update({i: [list(directories.keys())[[i[2] for i in directories.values()].index(dp)], os.path.join(dp, i)]})
#print(files, directories)

def convert3(n, b=256):
    return [n%b, (n//b)%b, (n//(b**2))%b][::-1]

def convert8(n, b=256):
    return [n%b, (n//b)%b, (n//(b**2))%b, (n//b**3)%b, (n//(b**4))%b, (n//b**5)%b, (n//(b**6))%b, (n//b**7)%b][::-1]

for k, v in directories.items():
    w += bytes(convert3(v[0])) + bytes(convert3(k)) + bytes(v[1], "ascii")+b"\x00"*(32-len(bytes(v[1], "ascii")))
w += b"\xff"
for k, v in files.items():
    w += bytes(convert3(v[0])) + bytes(k, "ascii")+b"\x00"*(32-len(bytes(k, "ascii"))) + bytes(convert8(os.path.getsize(v[1]))) + open(v[1], "rb").read() + b"\xef\xff"
if len(sys.argv) == 3:
    with open(sys.argv[2], "wb") as f:
        f.write(w)
else:
    with open("fs.mafs", "wb") as f:
        f.write(w)
print(f"Directories inserted : {", ".join([i[1] for i in directories.values()])}")
print(f"Files inserted : {", ".join(list(files.keys()))}")