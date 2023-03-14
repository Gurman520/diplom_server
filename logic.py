import time as t
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-uuid')


namespace = parser.parse_args(sys.argv[1:])
uuid = namespace.uui
print(uuid)
t.sleep(30)
print("Таймер все")
my_file = open(uuid+".csv", "w+")
my_file.close()
