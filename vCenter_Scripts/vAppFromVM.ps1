Connect-VIServer vc09.xx.com -User xxxx.com" -Password "xxxx"
$Results = @()
Import-Csv "/Users/vinoths/Desktop/SDDC Automation/vCenter_Scripts/VM.csv" | ForEach-Object {
    $vMDetails = Get-VM -Name $_.Name
    $folder =  $vMDetails.Folder.Name
    $powerstate = $vMDetails.PowerState
    $resourcepool = $vMDetails.ResourcePool
    #$respool = $resourcepool.split( "( )")[0]
    
  
#    if ($powerstate = "PoweredOn"){

        $Report = "" | Select-Object VMName,VMState,vAppName,OvDCName
        $Report.VMName = $_.Name
        $Report.VMState = $vMDetails.PowerState
        $Report.vAppName = $vMDetails.Folder.Name
        $Report.OvDCName = $vMDetails.ResourcePool
        Write-Host "$powerstate VM  "$($_.Name)" is part of vApp "$folder" on OvDC $resourcepool."
        $Results += $Report
        

        #$Report.Reading = $Sensor.CurrentReading/100
        
    #}
    
    #$Results
  }
  
  $Results | Format-Table VMName,VMState,vAppName,OvDCName
  $Results| Export-Csv -Path '/Users/vinoths/Desktop/SDDC Automation/vCenter_Scripts/VMFOLDER.csv'
