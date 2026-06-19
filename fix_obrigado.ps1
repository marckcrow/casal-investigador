$ob = "C:\Users\Administrador\.qclaw-oversea\workspace\casal-investigador\obrigado.html"
$c = [IO.File]::ReadAllText($ob)
$c = $c.Replace('100 Casos para Desvendar', '50 Casos para Desvendar')
$c = $c.Replace('href="#" id="downloadBtn"', 'href="https://pay.kiwify.com.br/eErvPaj" id="downloadBtn" target="_blank"')
$c = $c.Replace("'SEU_PRODUCT_ID_AQUI'", "'eErvPaj'")
$c = $c.Replace("' + KIWIFY_PRODUCT_ID", "'eErvPaj'")
[IO.File]::WriteAllText($ob, $c, (New-Object System.Text.UTF8Encoding $false))
Write-Host "Done - obrigado.html updated with Kiwify link"
