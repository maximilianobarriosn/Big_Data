#!/bin/bash
echo "Ultimas 100 lineas del archivo my_linux_search_file que contienen ERROR: "
grep "ERROR" $(pwd)/../files/my_linux_search_file.txt | tail -100