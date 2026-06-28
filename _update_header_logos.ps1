# Update header logo img src from logo.png to logo-header.webp
# Only changes src= attributes for header logos, preserves all other attributes

$total = 0

Get-ChildItem -Path "." -Include "*.html" -Recurse | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content $file -Raw
    $original = $content

    # Replace full CDN URL for header logo
    $content = $content -creplace 'src="https://jeeprepguide\.netlify\.app/logo\.png"',
        'src="https://jeeprepguide.netlify.app/logo-header.webp"'

    if ($content -ne $original) {
        $total++
        Set-Content -Path $file -Value $content -NoNewline
        Write-Host "Updated: $file"
    }
}

Write-Host "`nTotal HTML files updated: $total"