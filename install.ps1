Add-Type -AssemblyName System.Windows.Forms
$IGUI = New-Object system.Windows.Forms.Form
$IGUI.ClientSize = '500,400'
$IGUI.text = "INSTALLER GUI"
$IGUI.BackColor = "#ffffff"
$TTL = New-Object System.Windows.Forms.Label
$TTL.text = "ACDL Installer"
$TTL.Font = 'Microsoft Sans Serif,13'
$IGUI.controls.AddRange(@($TTL))
[void]$IGUI.ShowDialog()
$pythonUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
$installerPath = "$env:TEMP\python-3.11.0-amd64.exe"

# Download Python installer
Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

# Install Python
Start-Process -Wait -FilePath $installerPath -ArgumentList "/quiet", "PrependPath=1"

# Clean up the installer
Remove-Item -Path $installerPath
Write-Output "Python Installed"