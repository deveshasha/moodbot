import sys

# print("from test_3 py")

import fileinput

print("from test_3py")
sys.stdout.flush()
for line in fileinput.input():
    print (line)
    sys.stdout.flush()