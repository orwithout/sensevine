# PowerShell script to open Registry Editor at a specific key

# Set the registry key path you want to open
$registryPath = "Computer\HKEY_CLASSES_ROOT\*\shell"

# Start Registry Editor
Start-Process regedit

# Wait for the Registry Editor to load
Start-Sleep -Seconds 2

# Send the key path to the Registry Editor
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait($registryPath)
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

# Note: The SendKeys method is not always reliable as it depends on the focus being on the Registry Editor window.