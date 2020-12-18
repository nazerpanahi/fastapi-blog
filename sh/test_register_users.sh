#!/bin/bash


source ./functions.sh

echo -e "\n***************New Test Users***************\n"

read -p "Enter number of random users: " INPUT_NO

echo -e "\n***************Response***************\n"

LOGFILE="$(basename "$0").log"

for i in $(seq -w "$INPUT_NO"); do
INPUT_USERNAME="test$i"
INPUT_PASSWORD="P@ssw0rd"
register "$REG_URL" "$INPUT_USERNAME" "$INPUT_PASSWORD" >> "$LOGFILE"
echo -ne "\n" >> "$LOGFILE"
done