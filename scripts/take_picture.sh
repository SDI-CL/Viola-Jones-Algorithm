#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

raspistill -md 7 -o /home/pi/camera/$DATE.jpg

