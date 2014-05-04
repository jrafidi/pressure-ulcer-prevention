#!/bin/bash

hciconfig hci0 down
hciconfig hci0 up
#timeout 10 hcitool lescan
