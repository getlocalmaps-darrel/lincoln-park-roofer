$dir = 'D:\html websites\Lincoln Park Roofing'

$replacements = @(
    # Meta description pattern: "5,600 jobs, 30+ years"
    @('5,600 jobs, 30+ years', 'over 6,000 jobs, 35+ years'),

    # Blog author bio and body - specific "over 20 years" patterns
    @('over 20 years of hands-on experience', 'over 35 years of hands-on experience'),
    @('for over 20 years', 'for over 35 years'),
    @('over 20 years of experience', 'over 35 years of experience'),
    @('over 20 years serving', 'over 35 years serving'),

    # ai.txt inline "5,600 roofs/jobs" patterns not caught
    @('5,600 roofs and 30+ years', 'over 6,000 roofs and 35+ years'),
    @('5,600 roofs, 30+ years', 'over 6,000 roofs, 35+ years'),
    @('5,600 roofs', 'over 6,000 roofs'),
    @('5,600 jobs', 'over 6,000 jobs')
)

$files = Get-ChildItem -Path $dir -Recurse -Include '*.html','*.txt' | Where-Object { $_.FullName -notlike '*\.git*' -and $_.Name -notlike 'update_claims*' }
$totalChanges = 0

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $originalContent = $content

    foreach ($pair in $replacements) {
        $content = $content.Replace($pair[0], $pair[1])
    }

    if ($content -ne $originalContent) {
        Set-Content $file.FullName -Value $content -Encoding UTF8 -NoNewline
        $totalChanges++
        Write-Host "Updated: $($file.Name)"
    }
}

Write-Host "`nTotal files updated: $totalChanges"
