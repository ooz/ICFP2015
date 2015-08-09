#!/bin/bash

for i in {0..24}
do
    ./play_icfp2015 -f problems/problem_"$i".json > output
    #sleep 1
    ./upload_json.sh
done
