#!/bin/sh

# Compile Python code to C
cython -a --embed python_serial_data_processing.pyx

# Compile C code to executable
gcc python_serial_data_processing.c -Wall -fPIC -I/usr/include/python2.7  -lpython2.7 -o pyprocessing