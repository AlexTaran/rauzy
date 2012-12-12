#!/bin/sh

maindir=$(cat $1 |./grepmaindir)
#echo $maindir
cat $1 | ./projector $maindir
