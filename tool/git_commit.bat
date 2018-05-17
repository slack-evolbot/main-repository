@echo off
set GIT="C:\Program Files\Git\cmd\git.exe"
set LOG="C:\Users\k-evolva\Desktop\commit.log"
cd C:\Users\k-evolva\Desktop\git\main-repository >> %LOG%
%GIT% add * >> %LOG%
if not "%1" == "" (
    %GIT% commit -a -m %1 >> %LOG%
) else (
    %GIT% commit -a -m "バッチファイルによるコミット" >> %LOG%
)
%GIT% pull origin master >> %LOG%
%GIT% push origin master:master >> %LOG%
cd /d %~dp0