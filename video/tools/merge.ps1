# 合并录屏 webm + 配音 mp3 -> 最终 mp4 (按 trim_offset 对齐音画)
# 用法:  pwsh video/tools/merge.ps1 video/408/os/deadlock
#       pwsh video/tools/merge.ps1 .                 (在主题目录里执行)

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$TopicDir
)

$ErrorActionPreference = "Stop"

$topic = (Resolve-Path $TopicDir).Path
$webm  = Join-Path $topic "out\demo.webm"
$mp3   = Join-Path $topic "narration.mp3"
$trimF = Join-Path $topic "out\trim_offset.txt"
$mp4   = Join-Path $topic "out\demo.mp4"

if (-not (Test-Path $webm)) { throw "missing $webm — 先运行 record.py" }
if (-not (Test-Path $mp3 )) { throw "missing $mp3"  }

$trim = if (Test-Path $trimF) { (Get-Content $trimF).Trim() } else { "0" }
Write-Host "topic: $topic" -ForegroundColor Cyan
Write-Host "trim : $trim s" -ForegroundColor Cyan

# 优先 PATH 中的 ffmpeg, 否则 imageio_ffmpeg
$ff = Get-Command ffmpeg -ErrorAction SilentlyContinue
$ffmpeg = if ($ff) { $ff.Source } else { python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" }
Write-Host "ffmpeg: $ffmpeg" -ForegroundColor Cyan

& $ffmpeg -y -ss $trim -i $webm -i $mp3 `
    -c:v libx264 -preset veryfast -crf 22 -pix_fmt yuv420p `
    -c:a aac -b:a 192k -shortest -movflags +faststart `
    $mp4

Write-Host "Done -> $mp4" -ForegroundColor Green
