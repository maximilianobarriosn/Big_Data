#!/bin/bash
echo "Cantidad de veces que aparece asd en my_linux_search_file.txt (case sensitive): $(grep -c "asd" $(pwd)/../files/my_linux_search_file.txt)"
echo "Cantidad de veces que aparece asd en my_linux_search_file.txt (case insensitive):$(grep -c -i "asd" $(pwd)/../files/my_linux_search_file.txt)"
