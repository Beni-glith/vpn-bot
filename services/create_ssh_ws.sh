#!/bin/bash
USER_ID=$1
USERNAME="trial${USER_ID: -4}"
PASSWORD="vpn123"
EXPIRE=1

useradd -e $(date -d "$EXPIRE days" +"%Y-%m-%d") -s /bin/false -M $USERNAME
echo -e "$PASSWORD\n$PASSWORD" | passwd $USERNAME

IP=$(curl -s ifconfig.me)
echo -e "Host: $IP\nPort: 22, 80, 443\nUsername: $USERNAME\nPassword: $PASSWORD\nExpired: $EXPIRE day(s)"
