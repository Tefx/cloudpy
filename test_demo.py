import sh
import yajl
import os
from time import sleep

print os.getcwd()
bytes = yajl.dumps(str(sh.pip.freeze()))
print yajl.loads(bytes)
