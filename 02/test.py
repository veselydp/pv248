from scorelib import load
import sys

data = load(sys.argv[1])
for item in data:
    print(item.format())
    print("")
