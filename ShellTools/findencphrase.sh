#!/bin/ksh

# search the dictionary for the specified encrypted phrase
dict.py -os mac -action search -searchtype encword -target $1
