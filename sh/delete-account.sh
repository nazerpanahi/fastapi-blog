#!/bin/bash


source ./functions.sh

echo -e "\n***************Delete account***************\n"

echo -e "\n***************Response***************\n"

TOKEN=$(cat tok.en)
logout $DELETE_ACCOUNT_URL $TOKEN
