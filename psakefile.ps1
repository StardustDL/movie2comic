Task f -depends frontend

Task b -depends backend

Task bd -depends backend-dev

Task backend-dev {
    Exec { python -m backend }
}

Task backend {
    docker-compose -f .\docker-compose.dev.yml up backend
}

Task frontend {
    Set-Location ./frontend
    Exec { npm run serve }
    Set-Location ../
}

Task download-models {
    Set-Location ./backend/subtitles/deepspeech/models
    Exec { curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm }
    Exec { curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer }
    Exec { curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models-zh-CN.pbmm }
    Exec { curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models-zh-CN.scorer }
    Get-Location
    Get-ChildItem
    Set-Location ../../../..
}

Task build-frontend {
    Set-Location ./frontend
    Exec { npm ci }
    Exec { npm run build }
    Set-Location ../
}