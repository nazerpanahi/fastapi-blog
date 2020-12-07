#!/bin/bash

source ./constants.sh

function register {
    URL=$1
    USERNAME=$2
    PASSWORD=$3
    DATA=$(echo '{'\"$USERNAME_KEY\"': '\"$USERNAME\"', '\"$PASSWORD_KEY\"': '\"$PASSWORD\"'}')
    curl -d "$DATA" "$URL"
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
    TOKEN=$(cat tok.en)
    curl -s -X POST -H "Authorization: Bearer $TOKEN" $URL
}

function delete_account {
    URL=$1
    TOKEN=$2
    curl -s -X POST -H "Authorization: Bearer $TOKEN" $URL
}
