# Scarica i primi episodi numerati di Welcome to Night Vale dal feed ufficiale
# e crea un file .mp3z per episodio (MP3 dentro uno ZIP, estensione rinominata),
# pronto da copiare sul Kobo col cavo.
#
# Uso: tasto destro sul file -> "Esegui con PowerShell".
# I file finiscono nella cartella NightVale_mp3z sul Desktop.

param(
    [int]$Quanti = 30
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"   # download molto più veloci

$feedUrl = "https://feeds.nightvalepresents.com/welcometonightvalepodcast"
$dest = Join-Path ([Environment]::GetFolderPath("Desktop")) "NightVale_mp3z"
$tmp = Join-Path $env:TEMP "nightvale_tmp"
New-Item -ItemType Directory -Force -Path $dest, $tmp | Out-Null

Write-Host "Leggo il feed..."
[xml]$feed = (Invoke-WebRequest -Uri $feedUrl -UseBasicParsing).Content

# Solo episodi numerati ("1 - Pilot", "19A - The Sandstorm"), in ordine di numero
$episodi = foreach ($item in $feed.rss.channel.item) {
    # SelectSingleNode evita di confondere <title> con <itunes:title>
    $titolo = $item.SelectSingleNode("title").InnerText
    $enc = $item.SelectSingleNode("enclosure")
    if ($titolo -match '^(\d+)([A-Z]?)\s*-\s*(.+)$' -and $enc) {
        [pscustomobject]@{
            Numero = [int]$Matches[1]
            Lettera = $Matches[2]
            Titolo = $Matches[3].Trim()
            Url = $enc.GetAttribute("url")
        }
    }
}
$episodi = $episodi | Sort-Object Numero, Lettera | Select-Object -First $Quanti

$i = 0
foreach ($ep in $episodi) {
    $i++
    $pulito = ($ep.Titolo -replace '[\\/:*?"<>|]', '').Trim()
    $nome = "Night Vale {0:D3}{1} - {2}" -f $ep.Numero, $ep.Lettera, $pulito
    $mp3z = Join-Path $dest "$nome.mp3z"
    if (Test-Path $mp3z) {
        Write-Host "[$i/$($episodi.Count)] gia' presente: $nome"
        continue
    }
    Write-Host "[$i/$($episodi.Count)] scarico: $nome"
    $mp3 = Join-Path $tmp "$nome.mp3"
    Invoke-WebRequest -Uri $ep.Url -OutFile $mp3 -UseBasicParsing
    $zip = Join-Path $tmp "$nome.zip"
    Compress-Archive -Path $mp3 -DestinationPath $zip -CompressionLevel NoCompression -Force
    Move-Item $zip $mp3z -Force
    Remove-Item $mp3
}

Remove-Item $tmp -Recurse -Force
Write-Host ""
Write-Host "Fatto. I file sono in: $dest"
Write-Host "Collega il Kobo, copia i file .mp3z nella sua memoria ed espellilo."
Read-Host "Premi Invio per chiudere"
