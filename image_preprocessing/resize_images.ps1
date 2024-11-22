# resize_images.ps1

# Imagemagick 오픈 소스 프로그램 다운로드

# powershell에 ./resize_images.ps1 입력하여 실행

# 쉘 스크립트가 안될경우 아래 입력
### Set-ExecutionPolicy Bypass -Scope Process ###

# 파일 경로 예시
# 성충
# |-성충_날개불구바이러스_감염증
#   |- 002 |- B_001_001_20230821082418_001_003_001_002.jpg
#   |- ...
# |-성충_응애
#   |- ...
# |-성충_정상
#   |- ...
# |-resize_images.ps1 (현재 파일)
# |-resized_images (생성될 폴더)
#   |- B_001_001_20230821082418_001_003_001_002.jpg
#   |- ...

$inputFolder = "."

$outputFolder = "./images"

if(!(Test-Path -Path $outputFolder)){
    New-Item -ItemType Directory -Path $outputFolder
}

# Get all class folders (e.g. 성충_날개불구바이러스_감염증, 성충_응애, 성충_정상)
$class_folders = Get-ChildItem -Directory $inputFolder
foreach($class_folder in $class_folders){
    # Get all folders in the class folder (e.g. 001, 002, 003)
    foreach($folder in Get-ChildItem -Directory $class_folder.FullName){
        $jpgFile = Get-ChildItem -Path $folder.FullName -Filter "*.jpg" | Select-Object -First 1

        if ($jpgFile){
            $outputFileName = $jpgFile.Name
            $outputPath = Join-Path $outputFolder $outputFileName
            magick $jpgFile.FullName -resize 640x360 -background black -gravity center -extent 640x640 $outputPath
            Write-Output "Processed $jpgFile to $outputPath"
        }else{
            Write-Output "Image not found in $folder.FullName"
        }
    }
}
