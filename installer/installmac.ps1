Add-Type -AssemblyName System.Windows.Forms
$ACDLINS = New-Object system.Windows.Forms.Form
$ACDLINS.ClientSize = '400,200'

$InstBtn = New-Object System.Windows.Forms
$InstBtn.text = "Install ACDL"
$InstBtn.Font = "Microsoft Sans Serif,10"

$CancelBtn = New-Object System.Windows.Forms
$CancelBtn.text = "Cancel"

[void]$ACDLINS.ShowDialog()