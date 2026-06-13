Add-Type -AssemblyName System.IO.Compression.FileSystem

$reportDir = "E:\FYP-main\report_extracted\report"
$files = Get-ChildItem -Path $reportDir -Filter "*.docx" | Sort-Object Name

foreach ($file in $files) {
    Write-Host "=========================================="
    Write-Host "FILE: $($file.Name)"
    Write-Host "=========================================="
    
    $zip = [System.IO.Compression.ZipFile]::OpenRead($file.FullName)
    $entry = $zip.Entries | Where-Object { $_.FullName -eq "word/document.xml" }
    
    if ($entry) {
        $stream = $entry.Open()
        $reader = New-Object System.IO.StreamReader($stream)
        $content = $reader.ReadToEnd()
        $reader.Close()
        $stream.Close()
        
        $xmlDoc = New-Object System.Xml.XmlDocument
        $xmlDoc.LoadXml($content)
        
        $nsMgr = New-Object System.Xml.XmlNamespaceManager($xmlDoc.NameTable)
        $nsMgr.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
        
        $paragraphs = $xmlDoc.SelectNodes("//w:p", $nsMgr)
        
        foreach ($para in $paragraphs) {
            $texts = $para.SelectNodes(".//w:t", $nsMgr)
            $lineText = ""
            foreach ($t in $texts) {
                $lineText += $t.InnerText
            }
            if ($lineText.Trim() -ne "") {
                Write-Host $lineText
            }
        }
    }
    
    $zip.Dispose()
    Write-Host ""
    Write-Host ""
}
