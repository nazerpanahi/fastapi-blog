#!/bin/bash

BASE_URL="127.0.0.1:8000"

USERNAME_KEY="username"
PASSWORD_KEY="password"

REG_URL="$BASE_URL/register"
LOGIN_URL="$BASE_URL/login"
LOGOUT_URL="$BASE_URL/logout"
DELETE_ACCOUNT_URL="$BASE_URL/delete-account"

NEW_POST_URL="$BASE_URL/post/new"
LIKE_POST_URL="$BASE_URL/post/like"

NEW_COMMENT_URL="$BASE_URL/comment/new"
