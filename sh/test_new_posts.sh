#!/bin/bash

source ./functions.sh

echo -e "\n***************New Test Posts***************\n"

read -p "Enter number of random posts: " INPUT_NO

echo -e "\n***************Response***************\n"

TOKEN=$(cat tok.en)
for i in $(seq -w $INPUT_NO); do
POST_TITLE="Post $i title"
POST_CONTENT="This is post $i content for fun."
new_post $NEW_POST_URL $TOKEN $POST_TITLE $POST_CONTENT
done
