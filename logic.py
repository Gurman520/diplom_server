import time as t
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-uuid')


namespace = parser.parse_args(sys.argv[1:])
uuid = namespace.uuid
print(uuid)
t.sleep(30)
print("Таймер все")
my_file = open("./FinishPredict/" + uuid+".csv", "w+")
my_file.close()
