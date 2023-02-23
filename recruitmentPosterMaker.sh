#/bin/env
ls -1 ~/11ty-sesosite/assets/img/raw_media/* |  shuf | head -1 | convert "@-" -resize 1920 ~/bot/Kakapo/RecruitmentPosterOverlay.png -gravity South -composite ~/bot/Kakapo/result.jpg
