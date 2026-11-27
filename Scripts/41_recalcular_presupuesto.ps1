<#
CX-1 helper for Scripts/40_llenar_plantilla_presupuesto.py
Entrada: -Workbook <presupuesto .xlsm>
Salida: JSON de celdas calculadas por Excel COM en stdout; libro guardado.
Dependencias: Microsoft Excel de escritorio.
Fecha: 26-11-2026
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$Workbook
)

$excel = $null
$book = $null
$previousSecurity = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AskToUpdateLinks = $false
    $excel.EnableEvents = $false
    $excel.ScreenUpdating = $false
    $previousSecurity = $excel.AutomationSecurity
    $excel.AutomationSecurity = 3 # msoAutomationSecurityForceDisable
    $book = $excel.Workbooks.Open((Resolve-Path -LiteralPath $Workbook).Path, 0, $false)
    foreach ($sheet in $book.Worksheets) {
        $sheet.PageSetup.PaperSize = 1 # xlPaperLetter
        if ($sheet.Name -eq 'D25-00_Sobrecosto') {
            $sheet.PageSetup.Orientation = 2 # xlLandscape
        }
        else {
            $sheet.PageSetup.Orientation = 1 # xlPortrait
        }
        $sheet.PageSetup.Zoom = $false
        $sheet.PageSetup.FitToPagesWide = 1
        $sheet.PageSetup.FitToPagesTall = $false # 0 = unlimited height / fit-to-width only
        $sheet.PageSetup.LeftMargin = 36
        $sheet.PageSetup.RightMargin = 36
        $sheet.PageSetup.TopMargin = 54
        $sheet.PageSetup.BottomMargin = 54
    }
    $excel.CalculateFullRebuild()
    $excel.CalculateUntilAsyncQueriesDone()

    $over = $book.Worksheets.Item('D25-00_Sobrecosto')
    $budget = $book.Worksheets.Item('D25-00_Presupuesto')
    $subtotalRow = 0
    $ivaRow = 0
    $totalRow = 0
    for ($row = 17; $row -le 1000; $row++) {
        $label = [string]$budget.Cells.Item($row, 2).Value2
        if ($label -eq 'SUBTOTAL') { $subtotalRow = $row }
        elseif ($label -eq 'IVA') { $ivaRow = $row }
        elseif ($label -eq 'TOTAL') { $totalRow = $row }
        if ($subtotalRow -gt 0 -and $ivaRow -gt 0 -and $totalRow -gt 0) { break }
    }
    if ($subtotalRow -eq 0 -or $ivaRow -eq 0 -or $totalRow -eq 0) {
        throw 'No se encontraron los renglones SUBTOTAL, IVA y TOTAL.'
    }

    $result = [ordered]@{
        AD200 = $over.Range('AD200').Value2
        AD209 = $over.Range('AD209').Value2
        AD210 = $over.Range('AD210').Value2
        AD211 = $over.Range('AD211').Value2
        AW5 = $over.Range('AW5').Value2
        AW215 = $over.Range('AW215').Value2
        BE209 = $over.Range('BE209').Value2
        BE210 = $over.Range('BE210').Value2
        BE211 = $over.Range('BE211').Value2
        IVA = $budget.Cells.Item($ivaRow, 7).Value2
        IVA_celda = "G$ivaRow"
        TOTAL = $budget.Cells.Item($totalRow, 7).Value2
        SUBTOTAL = $budget.Cells.Item($subtotalRow, 7).Value2
    }
    $book.Save()
    ConvertTo-Json -InputObject $result -Compress -Depth 4
}
finally {
    if ($book -ne $null) {
        $book.Close($true)
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($book)
        $book = $null
    }
    if ($excel -ne $null) {
        if ($previousSecurity -ne $null) { $excel.AutomationSecurity = $previousSecurity }
        $excel.Quit()
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel)
        $excel = $null
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
