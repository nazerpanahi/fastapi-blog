#!/bin/bash


source ./functions.sh

echo -e "\n***************New Post***************\n"

read -p "Post title file path: " INPUT_PTFP
read -p "Post content file path: " INPUT_PCFP

POST_TITLE=$(cat "$INPUT_PTFP")
POST_CONTENT=$(cat "$INPUT_PCFP")

echo -e "\n***************Response***************\n"

TOKEN=$(cat tok.en)
new_post "$NEW_POST_URL" "$TOKEN" "$POST_TITLE" "$POST_CONTENT"