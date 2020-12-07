#!/bin/bash


source ./functions.sh

echo -e "\n***************Login***************\n"

read -p "Username: " INPUT_USERNAME
read -sp "Password: " INPUT_PASSWORD 

echo -e "\n***************Response***************\n"

login $LOGIN_URL $INPUT_USERNAME $INPUT_PASSWORD
