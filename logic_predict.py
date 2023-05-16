import time as t
import sys
import argparse
import random
import app.parser as p


parser = argparse.ArgumentParser()
parser.add_argument('-uuid')
parser.add_argument('-model')


namespace = parser.parse_args(sys.argv[1:])
uuid = namespace.uuid
model = namespace.model
print(uuid, "model", model)
ks = []
ls = p.read_from_file(uuid, 11)
for i in ls:
    ks.append([i[0], i[1], random.randint(0, 1)])
t.sleep(30)
print("Таймер все")
p.write_to_file(ks, uuid, 11)
