<#  Takes a file with pairs of an email adress and an integer, a text file 
    with a message, and a file with newline separated voucher codes and
    emails the specified number of codes to each email adress paired with the
    message.

    The text file should have the email subject on the first line, followed by 
    exactly two blank lines, and then the email body.

    The list of email adresses can have one or several emails per row. Each row 
    corresponds to one email. Multiple emails on a row should be 
    semicolon-separated.
#>

param([string]$to, [string]$text, [string]$vouchers)

function FullPath([string]$path) {
    [System.IO.Path]::GetFullPath((Join-Path (pwd) $path))
}

function SendMail([string]$subject, [System.Array]$text, [string]$to) {
    $outlook = New-Object -com Outlook.Application

    # Sends a single email using the provided outlook session
    
    $mail = $outlook.CreateItem(0)
    $mail.Subject = $subject
    $mail.Body = $text[3..($text.Length-1)]
    $mail.To = $to
    $mail.Send()
    #>
}

#Start-Process Outlook

# This is a hack, global variables and all

$voucherlines = New-Object System.Collections.ArrayList
(Get-Content (FullPath $vouchers)) | ForEach-Object {
    $voucherlines.Add($_)
}

$textrows = (Get-Content (FullPath $text))
$subject = $textrows[0]
(Get-Content (FullPath($to))) | ForEach-Object {
    $body = $textrows[3..($textrows.Length-1)] -join "`n"
    $toline = $_.Split(",")
    for($i=1; $i -le $toline[0]; $i++) {
        $body = $body + "`r`n" + $voucherlines.Item(0)
        $voucherlines.RemoveAt(0)
    }
    sendmail $subject $body $toline[1]
    Start-Sleep -m 250 
}
