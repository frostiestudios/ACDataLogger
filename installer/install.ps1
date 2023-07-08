$pythonUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
$installerPath = "$env:TEMP\python-3.11.0-amd64.exe"

# Download Python installer
Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

# Install Python
Start-Process -Wait -FilePath $installerPath -ArgumentList "/quiet", "PrependPath=1"

# Clean up the installer
Remove-Item -Path $installerPath
Write-Output "Python Installed"
Write-Progress 