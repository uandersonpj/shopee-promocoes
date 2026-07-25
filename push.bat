@echo off
cd /d "C:\Users\UANDERSON\shopee-site"

REM Regenera o sitemap com as categorias presentes no JSON atual
python gerar_sitemap.py

git add produtos.json sitemap.xml
git diff --cached --quiet && (
  echo [push.bat] Nenhuma alteracao.
  exit /b 0
)
git commit -m "update: produtos %date% %time%"
git push origin master
