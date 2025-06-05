#!/bin/sh
D=`date +%-d`
case $D in
  1|21|31) echo ${D}st;;
  2|22)    echo ${D}nd;;
  3|23)    echo ${D}rd;;
  *)       echo ${D}th;;
esac
