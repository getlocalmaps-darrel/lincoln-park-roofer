$dir = 'D:\html websites\Lincoln Park Roofing'

$replacements = @(
    @('**Years in Business:** 30+', '**Years in Business:** 35+'),
    @('- **Years in Business:** 30+', '- **Years in Business:** 35+'),
    @('5,000+ roofs completed across Downriver Michigan', 'over 6,000 roofs completed across Downriver Michigan'),
    @('5,000+ completed roofs', 'over 6,000 completed roofs'),
    @('with 5,000+ roofs completed', 'with over 6,000 roofs completed'),
    @('Over 30 years and 5,000+ completed roofs', 'Over 35 years and over 6,000 completed roofs'),
    @('5,000+ roofs completed.', 'over 6,000 roofs completed.'),
    @('5,600 roofs completed across Downriver Michigan', 'over 6,000 roofs completed across Downriver Michigan'),
    @('5,600 roofing jobs across Downriver Michigan', 'over 6,000 roofing jobs across Downriver Michigan'),
    @('5,600 roofing jobs across Monroe County', 'over 6,000 roofing jobs across Monroe County'),
    @('5,600 completed roofs', 'over 6,000 completed roofs'),
    @('5,600 residential jobs', 'over 6,000 residential jobs'),
    @('5,600 shingle roofs installed', 'over 6,000 shingle roofs installed'),
    @('Owens Corning Preferred Contractor with 5,600 roofs completed', 'Owens Corning Preferred Contractor with over 6,000 roofs completed'),
    @('5,600 roofs completed, 30+ years', 'over 6,000 roofs completed, 35+ years'),
    @('5,600 jobs completed, 30+', 'over 6,000 jobs completed, 35+'),
    @('5,600 Jobs, 30+ Years', 'Over 6,000 Jobs, 35+ Years'),
    @('5,600 Jobs Done', 'Over 6,000 Jobs Done'),
    @('**Jobs Completed:** 5,600 roofs', '**Jobs Completed:** over 6,000 roofs'),
    @('**Jobs Completed:** 5,000+ roofs', '**Jobs Completed:** over 6,000 roofs'),
    @('**Jobs Completed:** 5,600 roofing jobs', '**Jobs Completed:** over 6,000 roofing jobs'),
    @('5,600 Roofing Jobs Completed', 'Over 6,000 Roofing Jobs Completed'),
    @('5,600 Roofing Jobs', 'Over 6,000 Roofing Jobs'),
    @('5,600 Jobs', 'Over 6,000 Jobs'),
    @('5,600 roofs completed across Downriver Michigan in 30 years of business', 'over 6,000 roofs completed across Downriver Michigan in 35+ years of business'),
    @('5,000+ roofs completed across Downriver Michigan in 30 years of business', 'over 6,000 roofs completed across Downriver Michigan in 35+ years of business'),
    @('30 years of Downriver experience', '35+ years of Downriver experience'),
    @('30+ years in business', '35+ years in business'),
    @('30+ in business', '35+ in business'),
    @('with 30 years of experience', 'with over 35 years of experience'),
    @('30 years of experience', 'over 35 years of experience'),
    @('30 years local experience', 'over 35 years local experience'),
    @('30+ Years Experience', '35+ Years Experience'),
    @('30+ Years &bull;', '35+ Years &bull;'),
    @('30+ Years of Experience', '35+ Years of Experience'),
    @('20+ Years Experience', '35+ Years Experience'),
    @('in-house licensed crew used on 5,600 residential jobs', 'in-house licensed crew used on over 6,000 residential jobs')
)

$files = Get-ChildItem -Path $dir -Recurse -Include '*.html','*.txt' | Where-Object { $_.FullName -notlike '*\.git*' }
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
