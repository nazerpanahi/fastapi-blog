#!/bin/bash

source ./functions.sh

echo -e "\n***************Test All***************\n"

read -p "Enter number of random users: " INPUT_UNO
read -p "Enter number of random posts: " INPUT_PNO
read -p "Enter number of comments for each post: " INPUT_CNO
read -p "Enter number of likes for each post: " INPUT_LNO

echo -e "\n***************Response***************\n"

LOGFILE="$(basename $0).log"
BASE_USERNAME="Test"
BASE_PASSWORD="P@ssw0rd"
USER_ID_LOG_FILE="user_ids.log"
POST_ID_LOG_FILE="post_ids.log"

# register new users
> $USER_ID_LOG_FILE
for i in $(seq -w $INPUT_UNO); do
    echo 
    INPUT_USERNAME="${BASE_USERNAME}${i}"
    INPUT_PASSWORD="${BASE_PASSWORD}${i}"
    OUTPUT=$(register $REG_URL $INPUT_USERNAME $INPUT_PASSWORD)
    echo $OUTPUT
    USER_ID=$(echo $OUTPUT | jq '.data.user_id')
    echo $USER_ID >> $USER_ID_LOG_FILE
    # echo -ne "\n"
    echo "User with username '$INPUT_USERNAME' and password '$INPUT_PASSWORD' registered."
    echo 
done

# post new post
> $POST_ID_LOG_FILE
for i in $(seq -w $INPUT_UNO); do
    echo 
    login $LOGIN_URL "${BASE_USERNAME}${i}" "${BASE_PASSWORD}${i}"
    for j in $(seq -w $INPUT_PNO); do
        POST_TITLE="Post $j title"
        POST_CONTENT="This is post $j content for fun by user $i."
        OUTPUT=$(new_post $NEW_POST_URL $TOKEN $POST_TITLE $POST_CONTENT)
        echo $OUTPUT
        POST_ID=$(echo $OUTPUT | jq '.data.post_id')
        echo $POST_ID >> $POST_ID_LOG_FILE
        echo "User $i posted new post with title '$POST_TITLE'."
    done
    logout $LOGOUT_URL $TOKEN
    rm -rf ./tok.en
    echo 
done

# new comment
for i in $(seq -w $INPUT_UNO); do
    echo 
    login $LOGIN_URL "${BASE_USERNAME}${i}" "${BASE_PASSWORD}${i}"
    for j in $(seq -w $INPUT_CNO); do
        COMMENT_CONTENT="This is comment $j content for fun by user $i."
        RANDOM_LINE=$(shuf -i 1-$(wc -l $POST_ID_LOG_FILE | cut -d " " -f 1) -n 1)
        POST_ID=$(sed -n "${RANDOM_LINE}p" $POST_ID_LOG_FILE)
        new_comment $NEW_COMMENT_URL $TOKEN $POST_ID $COMMENT_CONTENT
        echo "User $i commented post '$POST_ID'."
    done
    logout $LOGOUT_URL $TOKEN
    rm -rf ./tok.en
    echo 
done

# new like
for i in $(seq -w $INPUT_UNO); do
    echo 
    login $LOGIN_URL "${BASE_USERNAME}${i}" "${BASE_PASSWORD}${i}"
    for j in $(seq -w $INPUT_LNO); do
        RANDOM_LINE=$(shuf -i 1-$(wc -l $POST_ID_LOG_FILE | cut -d " " -f 1) -n 1)
        POST_ID=$(sed -n "${RANDOM_LINE}p" $POST_ID_LOG_FILE)
        like_post $LIKE_POST_URL $TOKEN $POST_ID
        echo "User $i liked post '$POST_ID'."
    done
    logout $LOGOUT_URL $TOKEN
    rm -rf ./tok.en
    echo
done
