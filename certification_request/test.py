#!/usr/local/bin/python3

import sys

for i in range(0,len(sys.argv),1):
    print ('Argument #{num}: {value}'.format(num = i, value= sys.argv[i]))
    