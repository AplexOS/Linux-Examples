#!/bin/sh

if [ $1 = "start" ]; then
    touch /on-off.file
    sync
elif [ $1 = "end"  ];then
    rm /on-off.file -rf
    sync
else
    echo please input "start" or "end" ;
fi

