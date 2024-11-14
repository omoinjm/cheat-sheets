# Storage Account

Script to access storage account

```powershell
$connectTestResult = Test-NetConnection -ComputerName stoptixewbot.file.core.windows.net -Port 445

if ($connectTestResult.TcpTestSucceeded) {
    # Save the password so the drive will persist on reboot
    cmd.exe /C "cmdkey /add:`"stoptixewbot.file.core.windows.net`" /user:`"localhost\stoptixewbot`" /pass:`"FxnnA/XCgHxsYVNnX6jUQxpHoI6Qnm0XuzK4irwIpM3IKp9vlPZwqAeB12aOE1wn0SBc/Nylm8mD+ASt16vipQ==`""
    # Mount the drive
    New-PSDrive -Name L -PSProvider FileSystem -Root "\\stoptixewbot.file.core.windows.net\share1" -Persist
} else {
    Write-Error -Message "Unable to reach the Azure storage account via port 445. Check to make sure your organization or ISP is not blocking port 445, or use Azure P2S VPN, Azure S2S VPN, or Express Route to tunnel SMB traffic over a different port."
}
```
