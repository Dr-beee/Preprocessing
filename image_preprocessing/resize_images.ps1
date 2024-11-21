# resize_images.ps1

$inputFolder = "."

$outputFolder = "./bee_resized"

if(!(Test-Path -Path $outputFolder)){
    New-Item -ItemType Directory -Path $outputFolder
}

$folders = Get-ChildItem -Directory $inputFolder
foreach($folder in $folders){
    $jpgFile = Get-ChildItem -Path $folder.FullName -Filter "*.jpg" | Select-Object -First 1

    if ($jpgFile){
        $outputFileName = "$($folder.Name).jpg"
        $outputPath = Join-Path $outputFolder $outputFileName
        magick $jpgFile.FullName -resize 608x432 -background black -gravity center -extent 608x608 $outputPath
        Write-Output "Processed $jpgFile.FUllname to $outputPath"
    }else{
        Write-Output "Image not found in $folder"
    }
}