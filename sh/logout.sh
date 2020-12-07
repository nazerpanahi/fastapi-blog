#!/bin/bash


source ./functions.sh

echo -e "\n***************Logout***************\n"

echo -e "\n***************Response***************\n"

TOKEN=$(cat tok.en)
logout $LOGOUT_URL $TOKEN
