#! /bin/bash

cp -r ../../../templates/p4_psa_ebpf_template/* ./test.p4app

python3 codegen.py

p4c-ebpf --arch psa -o main.c ./test.p4app/main.p4
clang -O2 -g -c -DBTF -emit-llvm -o main.bc main.c
llc -march=bpf -mcpu=generic -filetype=obj -o main.o main.bc