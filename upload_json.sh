#!/bin/bash

API_TOKEN=$(cat "./api_token")
OUTPUT=$(cat "./output")

echo $API_TOKEN
echo $OUTPUT

curl --user :$API_TOKEN -X POST -H "Content-Type: application/json" -d "$OUTPUT" https://davar.icfpcontest.org/teams/169/solutions
