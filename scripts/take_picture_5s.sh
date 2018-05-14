#!/bin/bash

i=1

while [ 1 ]
do
  raspistill --mode 7 -o /home/pi/camera/$i.jpg
  ((i++))
  echo "picture $i taken"
  sleep 5s
done

