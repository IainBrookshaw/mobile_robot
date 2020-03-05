#! /bin/bash
#
# Ningauble of the Seven Eyes
# Iain Brookshaw
# Copyright (c) 2020, All Rights Reserved
# MIT License


# Colors & Logging

r="\e[31m"
g="\e[32m"
b="\e[34m"
y="\e[33m"
rs="\e[0m"

function logerr() {
    echo -e "${r}[err]:${rs} $1"
}
function loginf() {
    echo -e "${b}[inf]:${rs} $1"
}
function logwrn() {
    echo -e "${y}[wrn]:${rs} $1"
}
function logok() {
    echo -e "${g}[ok]:${rs}  $1"
}
