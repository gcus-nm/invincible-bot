#!/bin/bash

API_TENANT_ID="2c8c52cfd3204a8699a9d804231038c1" # テナントID
API_USERNAME="gncu58124125" # APIユーザー名
API_PASSWORD="Smashsmash_12" # APIパスワード
SERVER_UUID="a4f47b4c-a934-4415-9344-0dc50970512a" # サーバーのUUID
URL_END_POINT_IDENTITY="https://identity.tyo2.conoha.io/v2.0" # エンドポイント: Identity Service
URL_END_POINT_COMPUTE="https://compute.tyo2.conoha.io/v2/2c8c52cfd3204a8699a9d804231038c1" # エンドポイント: Compute Service

REQ_TOKEN_JSON="{ "auth": { "passwordCredentials": { "username": "gncu58124125", "password": "Smashsmash_12"}, "tenantId": "2c8c52cfd3204a8699a9d804231038c1" } }"

TOKEN=$(curl -i -X POST -H "Accept: application/json" -d ' { "auth": { "passwordCredentials": { "username": "gncu58124125", "password": "Smashsmash_12"}, "tenantId": "2c8c52cfd3204a8699a9d804231038c1" } }' ${URL_END_POINT_IDENTITY}/tokens | jq -r -R 'fromjson? | .access.token.id')

curl -i -X GET -H "Accept: application/json" -H "X-Auth-Token: ${TOKEN}" https://compute.tyo2.conoha.io/v2/2c8c52cfd3204a8699a9d804231038c1/servers

