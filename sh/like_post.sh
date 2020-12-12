#!/bin/bash


source ./functions.sh

echo -e "\n***************Like Post***************\n"

read -p "Post id: " INPUT_PID

echo -e "\n***************Response***************\n"

TOKEN=$(cat tok.en)
like_post $LIKE_POST_URL $TOKEN $INPUT_PID