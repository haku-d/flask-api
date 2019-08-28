#!/bin/sh

IMAGE=<REPLACE WITH YOUR GITLAB CONTAINER PACKAGE>
VERSION=$1

echo "version: $VERSION"
echo $VERSION > VERSION

docker build -t $IMAGE:latest .

docker tag $IMAGE:latest $IMAGE:$VERSION

docker push $IMAGE:latest
docker push $IMAGE:$VERSION