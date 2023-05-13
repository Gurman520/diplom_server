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
ls = p.read_from_file(uuid, 0)
print(ls)
