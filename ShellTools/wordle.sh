#!/bin/ksh

# Run wordle action with specified parameters 
# expect arguments -include ... -require ... -omit ... -mask ... (last 3 are optional)
./dict.py -os mac -action wordle $@
