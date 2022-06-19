#!/bin/bash

set -eu

readonly API_TENANT_ID="2c8c52cfd3204a8699a9d804231038c1" # テナントID
readonly API_USERNAME="gncu58124125" # APIユーザー名
readonly API_PASSWORD="Smashsmash12" # APIパスワード
readonly SERVER_UUID="a4f47b4c-a934-4415-9344-0dc50970512a" # サーバーのUUID
readonly URL_END_POINT_IDENTITY="https://identity.tyo2.conoha.io/v2.0" # エンドポイント: Identity Service
readonly URL_END_POINT_COMPUTE="https://compute.tyo2.conoha.io/v2/2c8c52cfd3204a8699a9d804231038c1" # エンドポイント: Compute Service
#-------------------------------------------
echo "(1) トークン発行 - Identity API v2.0"
# ref. https://www.conoha.jp/docs/identity-post_tokens.html
#-------------------------------------------
REQUEST_TOKEN_BODY="{\"auth\":{\"passwordCredentials\":{\"username\":\"${API_USERNAME}\",\"password\":\"${API_PASSWORD}\"},\"tenantId\":\"${API_TENANT_ID}\"}}" \

RESPONSE_TOKEN=$( curl -s -X POST \
     -H "Accept: application/json" \
     -d "${REQUEST_TOKEN_BODY}" \
     ${URL_END_POINT_IDENTITY}/tokens )

API_TOKEN=""
API_EXPIRES=""

#echo "${RESPONSE_TOKEN}" | jq '.'

API_TOKEN=$(echo "${RESPONSE_TOKEN}" | jq -r '.access.token.id')
API_EXPIRES=$(echo "${RESPONSE_TOKEN}" | jq -r '.access.token.expires')

echo "API_TOKEN   = $API_TOKEN"
echo "API_EXPIRES = $API_EXPIRES"

if [ "${API_TOKEN}" = "null" ]; then
    echo "トークンの取得に失敗しました。"
    exit 1
fi


#----------------------------------------
echo -e "\n(2) VM起動 - Compute API v2"
# ref. https://www.conoha.jp/docs/compute-reboot_vm.html
#----------------------------------------
RESPONSE_REBOOT=$( curl -i -s -X POST \
  -H "Accept: application/json" \
  -H "X-Auth-Token: ${API_TOKEN}" \
  -d '{"os-start": null}' \
  ${URL_END_POINT_COMPUTE}/servers/${SERVER_UUID}/action )

HTTP_STATUS=$(echo "$RESPONSE_REBOOT" | head -n1 | cut -d ' ' -f2- | tr -d "\r\n")

if [ "${HTTP_STATUS}" = "202 Accepted" ]; then
    echo "起動に成功しました！"
    exit 0
else
    echo "起動に失敗しました。"
    echo "HTTP_STATUS = ${HTTP_STATUS}"
    exit 1
fi