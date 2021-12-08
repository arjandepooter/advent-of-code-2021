#/usr/bin/env bash
if [ -z "$1" ] ; then
    echo "Please pass the day number, e.g.: "
    echo "./download.sh 6"
    exit 1
fi

if [ -z "$AOC_SESSION" ] ;  then
    echo "Make sure AOC_SESSION is set in your environment"
    exit 2
fi

curl "https://adventofcode.com/2021/day/$1/input" \
    --compressed \
    --header "Cookie: session=$AOC_SESSION" \
    > inputs/day$(printf "%02d" $1).txt