cd "C:\Users\niccoloq\OneDrive - Ars Srl\Desktop\Private\Easy-versioning-sphinx\Example\project/build"
start /b python -m http.server 8000 --bind 0.0.0.0
timeout /t 2 /nobreak
explorer "http://localhost:8000/V. 2.0/English/index.html"