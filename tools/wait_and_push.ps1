$logPath = "C:\Users\kamil\ProxyGram_Project\Source\proxygram_local_build.txt"
$repoPath = "C:\Users\kamil\ProxyGram"

while ($true) {
    if (Test-Path $logPath) {
        $content = Get-Content -Path $logPath -Tail 20 | Out-String
        if ($content -match "BUILD SUCCESSFUL") {
            $apkFile = Get-ChildItem -Path "C:\Users\kamil\ProxyGram_Project\Source\TMessagesProj_App\build\outputs\apk\afat\debug" -Filter "*.apk" -Recurse | Select-Object -First 1
            if ($apkFile) {
                Copy-Item -Path $apkFile.FullName -Destination "C:\Users\kamil\ProxyGram_Project\Infrastructure\dist\ProxyGram.apk" -Force
                Set-Location "C:\Users\kamil\ProxyGram_Project\Infrastructure"
                git add dist/ProxyGram.apk
                git commit -m "Release working ProxyGram APK"
                git push origin main --force
            }
            break
        } elseif ($content -match "BUILD FAILED") {
            break
        }
    }
    Start-Sleep -Seconds 20
}
