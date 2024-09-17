
$vcUser = 'administrator@vsphere.local'
$vcPwd = ''
$vCenter = 'xxx-vc29.xxx.com'
$Cluster = 'xxx-vc29c01'

$VCsecure = ConvertTo-SecureString -String $vcPwd -AsPlainText -Force
$VCcred = New-Object -typename System.Management.Automation.PSCredential -argumentlist ($vcUser, $VCsecure)




$Connect = Connect-VIServer -Server $vCenter -Credential $VCcred
Write-Host ""
Write-Host "Connected to vCenter $vCenter.. "

       

$vsanhealthservice = Get-VSANView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
$cluster_view = (Get-Cluster -Name $Cluster).ExtensionData.MoRef
$results = $vsanhealthservice.VsanQueryVcClusterHealthSummary($cluster_view,$null,$null,$true,$null,$null,'defaultView')
$healthCheckGroups = $results.Groups
$ClomdLiveness = $results.ClomdLiveness

$OverallclomdStatus = $ClomdLiveness.ClomdLivenessResult

Write-Host CLOMD STATUS OF HOSTS -ForegroundColor DarkCyan
Write-Host " "
$affectedesxi_list = @() 
$clomd_res = @()   
    
foreach ($entity in $OverallclomdStatus) {

    $hostN =  $entity.Hostname 
    $CLomdS = $entity.ClomdStat

    Write-Host $hostN CLOMD status: $CLomdS

    $clomd_res += $hostN + ' CLOMD status: ' + $CLomdS 




    $CLOMDHealth = $entity | Where-Object { $_.ClomdStat -eq 'alive' }
    
    $affectedesxiS = $CLOMDHealth.Hostname
    $affectedesxi_list += $affectedesxiS


}



if ($CLOMDHealth -ne $null ) {
    Write-Host Affected Host Details : -ForegroundColor DarkRed
    #$affectedesxiS = $CLOMDHealth.Hostname



    foreach ($affectedesxi in $affectedesxi_list) {

        Write-Host " "
        $affectedHostState = Get-VMHost $affectedesxi
        $affectedHostConState = $affectedHostState.ConnectionState
        Write-Host Affected host $affectedesxi is in $affectedHostConState State 

        Write-Host $affectedesxi CLOMD STATUS is not healthy
        Write-Host " "

    }
    return $affectedesxi_list , $clomd_res
}

Else {
Write-Host " "
Write-Host CLOMD Process is healthy on all the hosts -ForegroundColor DarkGreen
Write-Host " "
$out = "No_Affected_host"

return $out , $clomd_res
}



