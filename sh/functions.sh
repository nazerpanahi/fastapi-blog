#!/bin/bash

source ./constants.sh

function register {
    URL=$1
    USERNAME=$2
    PASSWORD=$3
    DATA=$(echo '{'\"$USERNAME_KEY\"': '\"$USERNAME\"', '\"$PASSWORD_KEY\"': '\"$PASSWORD\"'}')
    curl -d "$DATA" "$URL" -s
}


function login {
    URL=$1
    USERNAME=$2
    PASSWORD=$3
    DATA=$(echo '{'\"$USERNAME_KEY\"': '\"$USERNAME\"', '\"$PASSWORD_KEY\"': '\"$PASSWORD\"'}')
    TOKEN=$(curl -s -H "Accept: application/json" -X POST -d "$DATA" "$URL")
    echo $TOKEN | tee tok.en
}


function logout {
    URL=$1
    TOKEN=$2
    curl -s -X POST -H "Authorization: Bearer $TOKEN" $URL
}

function delete_account {
    URL=$1
    TOKEN=$2
    curl -s -X POST -H "Authorization: Bearer $TOKEN" $URL
}

function new_post {
    URL=$1
    TOKEN=$2
    TITLE=$3
    CONTENT=$4
    DATA=$(echo '{'\"title\"': '\"$TITLE\"', '\"content\"': '\"$CONTENT\"'}')
    curl -s -X POST -H "Authorization: Bearer $TOKEN" -d "$DATA" $URL
}

function new_comment {
    URL=$1
    TOKEN=$2
    POST_ID=$3
    CONTENT=$4
    DATA=$(echo '{'\"post_id\"': '\"$POST_ID\"', '\"content\"': '\"$CONTENT\"'}')
    curl -s -X POST -H "Authorization: Bearer $TOKEN" -d "$DATA" $URL
}

function like_post {
    URL=$1
    TOKEN=$2
    POST_ID=$3
    curl -s -X GET -H "Authorization: Bearer $TOKEN" $URL?post_id=$POST_ID
}
