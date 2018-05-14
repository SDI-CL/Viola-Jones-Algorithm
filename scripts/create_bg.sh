#!/bin/bash

i=1
while [ $i -le 32 ] 
do
	echo "negative/$i.jpg" >> "bg.txt"
	(( i++ ))
done
