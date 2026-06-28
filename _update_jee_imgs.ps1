# Update img src references from PNG to WebP in jee/physics and jee/chemistry HTML files
# Only changes src= attributes, preserves all other attributes

$dirs = @("jee\physics", "jee\chemistry")

# Physics PNG -> WebP mappings
$physics = @(
    "alternating-current.png",              "alternating-current.webp",
    "atoms-and-nuclei.png",                "atoms-and-nuclei.webp",
    "capacitance.png",                     "capacitance.webp",
    "centre-of-mass-and-collision.png",    "centre-of-mass-and-collision.webp",
    "current-electricity.png",              "current-electricity.webp",
    "dual-nature-of-radiation-and-matter.png", "dual-nature-of-radiation-and-matter.webp",
    "electromagnetic-induction.png",       "electromagnetic-induction.webp",
    "electromagnetic-waves.png",           "electromagnetic-waves.webp",
    "electrostatics.png",                  "electrostatics.webp",
    "fluid-mechanics.png",                 "fluid-mechanics.webp",
    "gravitation.png",                     "gravitation.webp",
    "kinematics.png",                      "kinematics.webp",
    "kinetic-theory-of-gases.png",         "kinetic-theory-of-gases.webp",
    "laws-of-motion.png",                  "laws-of-motion.webp",
    "magnetic-effects-of-current-and-magnetism.png", "magnetic-effects-of-current-and-magnetism.webp",
    "ray-optics.png",                      "ray-optics.webp",
    "rotational-motion.png",               "rotational-motion.webp",
    "semiconductors.png",                  "semiconductors.webp",
    "simple-harmonic-motion.png",          "simple-harmonic-motion.webp",
    "thermal-properties-of-matter.png",    "thermal-properties-of-matter.webp",
    "thermodynamics.png",                  "thermodynamics.webp",
    "units-and-dimensions.png",             "units-and-dimensions.webp",
    "wave-motion.png",                     "wave-motion.webp",
    "wave-optics.png",                     "wave-optics.webp",
    "work-energy-and-power.png",            "work-energy-and-power.webp"
)

# Chemistry PNG -> WebP mappings
$chemistry = @(
    "chemical-kinetics.png",               "chemical-kinetics.webp",
    "electrochemistry.png",                 "electrochemistry.webp",
    "surface-chemistry.png",               "surface-chemistry.webp"
)

$total = 0

foreach ($dir in $dirs) {
    $mappings = if ($dir -eq "jee\physics") { $physics } else { $chemistry }

    Get-ChildItem -Path $dir -Filter "*.html" | ForEach-Object {
        $file = $_.FullName
        $content = Get-Content $file -Raw
        $original = $content

        for ($i = 0; $i -lt $mappings.Length; $i += 2) {
            $png = $mappings[$i]
            $webp = $mappings[$i + 1]

            # Replace full CDN URLs for physics
            if ($dir -eq "jee\physics") {
                $content = $content -creplace "src=""https://jeeprepguide\.netlify\.app/jee/physics/$png""",
                    "src=""https://jeeprepguide.netlify.app/jee/physics/$webp"""
            }
            # Replace full CDN URLs for chemistry (handle the electrochemistry subdir mismatch)
            else {
                $content = $content -creplace "src=""https://jeeprepguide\.netlify\.app/jee/chemistry/$png""",
                    "src=""https://jeeprepguide.netlify.app/jee/chemistry/$webp"""
                $content = $content -creplace "src=""https://jeeprepguide\.netlify\.app/jee/chemistry/electrochemistry/$png""",
                    "src=""https://jeeprepguide.netlify.app/jee/chemistry/$webp"""
            }
        }

        if ($content -ne $original) {
            $total++
            Set-Content -Path $file -Value $content -NoNewline
            Write-Host "Updated: $file"
        }
    }
}

Write-Host "`nTotal HTML files updated: $total"