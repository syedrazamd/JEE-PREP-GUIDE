# update-notes-assets.ps1
# Replaces inline <style> and bottom <script> blocks in all notes HTML files
# with external CSS (per-subject) and JS (common) links.

$base = "e:\jeeprepguide\jee"

$subjects = @{
    "physics"   = "notes-physics.css"
    "chemistry" = "notes-chemistry.css"
    "maths"     = "notes-maths.css"
}

foreach ($subject in $subjects.Keys) {
    $cssFile = $subjects[$subject]
    $dir = Join-Path $base $subject
    $htmlFiles = Get-ChildItem -Path $dir -Filter "*.html" | Where-Object { $_.Name -ne "index.html" }

    foreach ($file in $htmlFiles) {
        Write-Host "Processing: $($file.FullName)"
        $content = [System.IO.File]::ReadAllText($file.FullName)

        # 1. Replace inline <style>...</style> with external CSS link
        #    The style block is the one right before </head>
        $stylePattern = '(?s)\s*<style>\s*body \{ font-family.*?</style>'
        $cssLink = "`r`n    <link rel=`"stylesheet`" href=`"../assets/css/$cssFile`">"
        
        if ($content -match $stylePattern) {
            $content = [regex]::Replace($content, $stylePattern, $cssLink)
            Write-Host "  [OK] Replaced inline <style> with $cssFile"
        } else {
            Write-Host "  [SKIP] No matching inline <style> found"
        }

        # 2. Replace inline bottom <script> (progress bar, nav highlighting, etc.)
        #    with external JS link. The bottom script starts after <!-- Scripts -->
        #    Pattern: <script> // Progress Bar ... </script> right before </body>
        $scriptPattern = '(?s)<script>\s*\r?\n\s*//\s*Progress Bar.*?</script>\s*(?=\r?\n\s*</body>)'
        $jsLink = "<script src=`"../assets/js/notes.js`"></script>"

        if ($content -match $scriptPattern) {
            $content = [regex]::Replace($content, $scriptPattern, $jsLink)
            Write-Host "  [OK] Replaced inline bottom <script> with notes.js"
        } else {
            Write-Host "  [SKIP] No matching bottom <script> found"
        }

        [System.IO.File]::WriteAllText($file.FullName, $content)
        Write-Host "  [SAVED] $($file.Name)"
        Write-Host ""
    }
}

Write-Host "`nDone! All notes pages updated."
