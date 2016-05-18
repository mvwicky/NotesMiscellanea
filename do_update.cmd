@echo off

SETLOCAL ENABLEEXTENSIONS
SET me=%~n0
SET parent=%~dp0

git pull
git submodule update --init --recursive
git submodule foreach git checkout master || 0
git submodule foreach git pull --rebase || 0