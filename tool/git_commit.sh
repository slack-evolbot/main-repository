#!/bin/sh
LOG=/home/pi/log/commit.log
PASS=`pwd`
cd /home/pi/git/main-repository >> $LOG
git add * >> $LOG
if [ $# -eq 1 ]; then
    git commit -a -m $1 >> $LOG
else
    git commit -a -m "シェルファイルによるコミット" >> $LOG
fi
git pull origin master >> $LOG
git push origin master:master >> $LOG
cd $PASS
