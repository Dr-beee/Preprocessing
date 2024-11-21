# resize_images.ps1

# Imagemagick 오픈 소스 프로그램 다운로드

# powershell에 ./resize_images.ps1 입력하여 실행

# 쉘 스크립트가 안될경우 아래 입력
### Set-ExecutionPolicy Bypass -Scope Process ###

# ex
# 성충 응애
# |-bee_resized
# |-resize_images.ps1
# |-027 |-(난수).jpg
# |-039 |-(난수).jpg
# |- ...

$inputFolder = "."

$outputFolder = "./bee_resized"

if(!(Test-Path -Path $outputFolder)){
    New-Item -ItemType Directory -Path $outputFolder
}

$folders = Get-ChildItem -Directory $inputFolder
foreach($folder in $folders){
    $jpgFile = Get-ChildItem -Path $folder.FullName -Filter "*.jpg" | Select-Object -First 1

    if ($jpgFile){
        $outputFileName = $jpgFile.Name
        $outputPath = Join-Path $outputFolder $outputFileName
        magick $jpgFile.FullName -resize 640x360 -background black -gravity center -extent 640x640 $outputPath
        Write-Output "Processed $jpgFile.FUllname to $outputPath"
    }else{
        Write-Output "Image not found in $folder"
    }
}
