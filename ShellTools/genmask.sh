#!/bin/ksh

# call the dictionary tool to generate a mask for the specified phrase
dict.py -os mac -action genmask -target $1

