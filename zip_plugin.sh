#!/bin/bash

set -u
set -e

echo "Prepare plugin"

PWD=`pwd`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLUGIN=BivariateRenderer
SRC=$DIR/$PLUGIN
DEST="$DIR/build"
DEST_BUILD=$DEST/$PLUGIN

if [ ! -d "$SRC" ]; then
  echo "Missing directory $SRC"
  exit 1
fi

rm -rf $DEST_BUILD
mkdir -p $DEST_BUILD

cp -R $SRC/* $DEST_BUILD/
find $DEST_BUILD -type l -exec unlink {} \;

find $DEST_BUILD -name \*.pyc -delete
find $DEST_BUILD -name \*.pyo -delete
find $DEST_BUILD -name __pycache__ -delete

cd $DEST_BUILD/..

if [ -f "$DEST/$PLUGIN.zip" ]; then
    rm $DEST/$PLUGIN.zip
fi

zip -r $DEST/$PLUGIN.zip $PLUGIN --exclude *.coverage*

echo "$DEST/$PLUGIN.zip created"

cd $PWD
