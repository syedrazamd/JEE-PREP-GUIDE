# Update HTML files to replace Tailwind CDN with compiled CSS
$htmlFiles = Get-ChildItem -Path "e:\jeeprepguide" -Recurse -Include "*.html"

$updatedCount = 0
$skippedCount = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Check if file has Tailwind CDN or inline config
    $hasTailwind = ($content -match 'cdn\.tailwindcss\.com') -or ($content -match 'tailwind\.config\s*=')
    
    if ($hasTailwind) {
        Write-Host "Updating: $($file.FullName)"
        
        # Remove the Tailwind CDN script tag
        $content = $content -replace '<script src="https://cdn\.tailwindcss\.com"></script>', ''
        
        # Remove the inline tailwind.config script block (multi-line) - more comprehensive pattern
        $content = $content -replace '<script>\s*tailwind\.config\s*=\s*\{[\s\S]*?\n\s*\}\s*</script>', ''
        
        # Remove preconnect to cdn.tailwindcss.com
        $content = $content -replace '<link rel="preconnect" href="https://cdn\.tailwindcss\.com" />', ''
        
        # Remove dns-prefetch for cdn.tailwindcss.com
        $content = $content -replace '<link rel="dns-prefetch" href="https://cdn\.tailwindcss\.com" />', ''
        
        # Remove preload for tailwind CDN
        $content = $content -replace '<link rel="preload"[^>]*cdn\.tailwindcss\.com[^>]*>', ''
        
        # Remove Tailwind CSS comment
        $content = $content -replace '<!-- Tailwind CSS -->', ''
        
        # Add compiled CSS link before subject stylesheet
        $tailwindCssLink = '<link rel="stylesheet" href="/css/tailwind.min.css">'
        
        # Check for subject stylesheet patterns (relative path)
        if ($content -match '<link rel="stylesheet" href="\.\./assets/css/notes-[^"]+\.css">') {
            $content = $content -replace '<link rel="stylesheet" href="\.\./assets/css/notes-([^"]+)\.css">', "$tailwindCssLink`n<link rel=""stylesheet"" href=""../assets/css/notes-`$1.css"">"
        } elseif ($content -match '<link rel="stylesheet" href="/jee/assets/css/notes-[^"]+\.css">') {
            $content = $content -replace '<link rel="stylesheet" href="/jee/assets/css/notes-([^"]+)\.css">', "$tailwindCssLink`n<link rel=""stylesheet"" href=""/jee/assets/css/notes-`$1.css"">"
        } elseif ($content -match '<link rel="stylesheet" href="/assets/css/notes-[^"]+\.css">') {
            $content = $content -replace '<link rel="stylesheet" href="/assets/css/notes-([^"]+)\.css">', "$tailwindCssLink`n<link rel=""stylesheet"" href=""/assets/css/notes-`$1.css"">"
        } else {
            # If no subject stylesheet found, add before </head>
            $content = $content -replace '</head>', "$tailwindCssLink`n</head>"
        }
        
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        $updatedCount++
    } else {
        $skippedCount++
    }
}

Write-Host "`n=== Summary ==="
Write-Host "Updated: $updatedCount files"
Write-Host "Skipped (no Tailwind): $skippedCount files"