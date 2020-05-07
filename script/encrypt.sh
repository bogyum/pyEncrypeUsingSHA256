#!/bin/bash

if [ $# -ne 3 ]; then
	echo "Usage: $0 (encrypt source) (salt) (encrypt target)"
   exit -1
fi

encryptCode='pyEncryptUsingSHA256.py'

#ubuntu server path
#encryptHome='/home/jarvis/work/pyEncryptUsingSHA256' 

#MAC local path
#encryptHome='/Users/bogyum/work/pyEncryptUsingSHA256' 

#Windows local path
encryptHome='/c/work/pyEncryptUsingSHA256'

#Date=$(date '+%Y-%m-%d' -d '1 day ago')
if [ ! -d "${encryptHome}/log" ]; then
	mkdir ${encryptHome}/log
fi

Log="${encryptHome}/log/$Date.log"

python ${encryptHome}/src/${encryptCode} $1 $2 $3

