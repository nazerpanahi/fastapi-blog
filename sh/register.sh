#!/bin/bash


source ./functions.sh

echo -e "\n***************Register***************\n"

read -p "Username: " INPUT_USERNAME
read -sp "Password: " INPUT_PASSWORD 

echo -e "\n***************Response***************\n"

register $REG_URL $INPUT_USERNAME $INPUT_PASSWORD
