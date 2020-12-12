#!/bin/bash


source ./functions.sh

echo -e "\n***************New Comment***************\n"

read -p "Post id: " INPUT_PID
read -p "Post content file path: " INPUT_PCFP

POST_CONTENT=$(cat $INPUT_PCFP)

echo -e "\n***************Response***************\n"

TOKEN=$(cat tok.en)
new_comment $NEW_COMMENT_URL $TOKEN $INPUT_PID $POST_CONTENT