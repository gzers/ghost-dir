# Ghost-Dir 发布脚本
# 用法: .\scripts\release.ps1 -Version "1.0.0"

param(
    [Parameter(Mandatory=$true)]
    [string]$Version,
    
    [Parameter(Mandatory=$false)]
    [string]$Codename = ""
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Ghost-Dir 发布脚本 v$Version" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 更新版本号
Write-Host "[1/6] 更新版本号..." -ForegroundColor Yellow
$initFile = "src\__init__.py"
$content = Get-Content $initFile -Raw
$content = $content -replace '__version__ = ".*"', "__version__ = `"$Version`""
Set-Content $initFile $content -NoNewline
Write-Host "  ✓ 已更新 $initFile" -ForegroundColor Green

# 2. 更新 README 徽章
Write-Host "[2/6] 更新 README..." -ForegroundColor Yellow
$readmeFile = "README.md"
$content = Get-Content $readmeFile -Raw
$content = $content -replace 'version-[\d\.]+-.*\.svg', "version-$Version-blue.svg"
Set-Content $readmeFile $content -NoNewline
Write-Host "  ✓ 已更新 $readmeFile" -ForegroundColor Green

# 3. 检查 CHANGELOG
Write-Host "[3/6] 检查 CHANGELOG..." -ForegroundColor Yellow
$changelogFile = "docs\release\CHANGELOG.md"
if (Test-Path $changelogFile) {
    $changelog = Get-Content $changelogFile -Raw
    if ($changelog -match "\[$Version\]") {
        Write-Host "  ✓ CHANGELOG 已包含 $Version" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ 警告: CHANGELOG 未包含 $Version，请手动更新" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠ 警告: CHANGELOG 不存在" -ForegroundColor Yellow
}

# 4. 构建可执行文件
Write-Host "[4/6] 构建可执行文件..." -ForegroundColor Yellow
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}
pyinstaller Ghost-Dir.spec --clean
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ 构建失败" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ 构建完成" -ForegroundColor Green

# 5. 打包发布文件
Write-Host "[5/6] 打包发布文件..." -ForegroundColor Yellow
$zipName = "Ghost-Dir-$Version-win64.zip"
$zipPath = "dist\$zipName"
if (Test-Path $zipPath) {
    Remove-Item $zipPath
}
Compress-Archive -Path "dist\Ghost-Dir" -DestinationPath $zipPath
$hash = (Get-FileHash $zipPath -Algorithm SHA256).Hash
Write-Host "  ✓ 已创建 $zipName" -ForegroundColor Green
Write-Host "  SHA256: $hash" -ForegroundColor Cyan

# 6. Git 操作
Write-Host "[6/6] Git 操作..." -ForegroundColor Yellow
git add .
git commit -m "release: 发布 $Version 版本"
git tag -a "v$Version" -m "Release version $Version"
Write-Host "  ✓ 已创建 Git 标签 v$Version" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  发布准备完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步操作：" -ForegroundColor Yellow
Write-Host "1. 推送到远程仓库：" -ForegroundColor White
Write-Host "   git push origin main" -ForegroundColor Gray
Write-Host "   git push origin v$Version" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 创建 GitHub Release：" -ForegroundColor White
Write-Host "   - 前往 https://github.com/gzers/ghost-dir/releases/new" -ForegroundColor Gray
Write-Host "   - 选择标签 v$Version" -ForegroundColor Gray
Write-Host "   - 使用 docs/release/copy.md 中的文案" -ForegroundColor Gray
Write-Host "   - 上传 dist\$zipName" -ForegroundColor Gray
Write-Host "   - SHA256: $hash" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 发布文案位置：docs\release\templates.md" -ForegroundColor White
Write-Host ""
