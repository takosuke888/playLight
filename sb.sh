#!/bin/bash

token="9146d1f3d34378630b848c190edd3e610b0c7976413acf656f390b1f48c747e4884325024ff01c91d4569c218c70ed62"
secret="bf37e6a6175ca427551c21100e61ee29"
t=$(date +%s%3N)
nonce=$(uuidgen -r)
sign=$(echo -n ${token}${t}${nonce} | openssl dgst -sha256 -hmac ${secret} -binary | base64)

result=$(
    curl -s "https://api.switch-bot.com/v1.1/devices" \
      --header "Authorization: ${token}" \
      --header "sign: ${sign}" \
      --header "t: ${t}" \
      --header "nonce: ${nonce}" \
      --header "Content-Type: application/json; charset=utf8")

echo $result