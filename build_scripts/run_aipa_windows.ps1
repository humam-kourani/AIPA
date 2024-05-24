Write-Output "RUNNING BACKEND"
Set-Location ..
pip install -r requirements.txt

Start-Process powershell "build_scripts\run_aipa_frontend_windows.ps1"

python .\app.py -h localhost -p 4555
