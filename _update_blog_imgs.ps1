# Update img src references from PNG to WebP in blog HTML files
# Only changes src= attributes, preserves all other attributes

$blogDir = "blog"

# Mapping of PNG filenames to WebP filenames
$replacements = @(
    "comedk-2026-registration.png",          "comedk-2026-registration.webp",
    "comedk-2026-important-dates.png",       "comedk-2026-important-dates.webp",
    "icai-results-2026.png",                 "icai-results-2026.webp",
    "ca-final-result.png",                    "ca-final-result.webp",
    "icai-official-website.png",              "icai-official-website.webp",
    "iiith-ugee-2026-registration-date-eligibility-and-application-process.png",
    "iiith-ugee-2026-registration-date-eligibility-and-application-process.webp",
    "ugee-2026-exam-and-important-dates.png", "ugee-2026-exam-and-important-dates.webp",
    "ugee-2026-courses-offered-iiit-hyderabad.png",
    "ugee-2026-courses-offered-iiit-hyderabad.webp",
    "wbjee-2026-registration-date-exam-date-application-form.png",
    "wbjee-2026-registration-date-exam-date-application-form.webp",
    "jee-main-2026-do-or-die-chapters-score-200.png",
    "jee-main-2026-do-or-die-chapters-score-200.webp",
    "jee-main-2026-physics-high-weightage-chapters-chart.png",
    "jee-main-2026-physics-high-weightage-chapters-chart.webp",
    "jee-main-2026-Chemistry-high-weightage-chapters-chart.png",
    "jee-main-2026-Chemistry-high-weightage-chapters-chart.webp",
    "jee-main-2026-Mathematics-high-weightage-chapters-chart.png",
    "jee-main-2026-Mathematics-high-weightage-chapters-chart.webp"
)

$total = 0
$changed = 0

Get-ChildItem -Path $blogDir -Filter "*.html" | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content $file -Raw
    $original = $content

    for ($i = 0; $i -lt $replacements.Length; $i += 2) {
        $png = $replacements[$i]
        $webp = $replacements[$i + 1]

        # Replace full CDN URLs (case-sensitive)
        $content = $content -creplace "src=""https://jeeprepguide\.netlify\.app/blog/$png""", "src=""https://jeeprepguide.netlify.app/blog/$webp"""
        # Replace relative URLs (case-sensitive)
        $content = $content -creplace "src=""$png""", "src=""$webp"""
    }

    if ($content -ne $original) {
        $changed++
        Set-Content -Path $file -Value $content -NoNewline
        Write-Host "Updated: $file"
    }
}

Write-Host "`nTotal blog HTML files updated: $changed"