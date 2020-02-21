#!/usr/bin/env sh

# touch the env file
/bin/touch .env

# read the passed in env var and put it in the .env file

if [ -z $GITHUB_PERSONAL_ACCESS_TOKEN ]
then
	echo "We need a GITHUB_PERSONAL_ACCESS_TOKEN defined!"
	exit 1
fi

echo GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_PERSONAL_ACCESS_TOKEN >> .env
echo "RR_SECRET_KEY=$(openssl rand -base64 32)" >> .env

flask run -h 0.0.0.0 -p 5002
