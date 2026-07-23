@echo off
cd /d "C:\Users\UANDERSON\shopee-site"
git add produtos.json
git commit -m "update: produtos %date% %time%"
git push origin master
