function Handler($inputs) {
    $inputsString = $inputs | ConvertTo-Json -Compress

$vcUser = $inputs.vcUser
$vcPwd = $inputs.vcPwd
$vCenter = $inputs.vCenter

$VCsecure = ConvertTo-SecureString -String $vcPwd -AsPlainText -Force
$VCcred = New-Object -typename System.Management.Automation.PSCredential -argumentlist ($vcUser, $VCsecure)

$ConfigurationDetails = Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -ParticipateInCeip:$false -Scope Session -Confirm:$false 


$Connect = Connect-VIServer -Server $vCenter -Credential $VCcred
Write-Host ""
Write-Host "Connected to vCenter $vCenter.. "

       
$Cluster = $inputs.Cluster
            $vsanhealthservice = Get-VSANView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
            $cluster_view = (Get-Cluster -Name $Cluster).ExtensionData.MoRef
            $results = $vsanhealthservice.VsanQueryVcClusterHealthSummary($cluster_view,$null,$null,$true,$null,$null,'defaultView')
            $healthCheckGroups = $results.Groups
            $ClomdLiveness = $results.ClomdLiveness

    $OverallclomdStatus = $ClomdLiveness.ClomdLivenessResult

    Write-Host CLOMD STATUS OF HOSTS -ForegroundColor DarkCyan
    Write-Host " "
    
    
    foreach ($entity in $OverallclomdStatus) {

        $hostN =  $entity.Hostname 
        $CLomdS = $entity.ClomdStat

        Write-Host $hostN CLOMD status: $CLomdS

    }
  

    $CLOMDHealth = $OverallclomdStatus | Where-Object { $_.ClomdStat -ne 'alive' }
    $affectedesxiS = $CLOMDHealth.Hostname
    
    if ($CLOMDHealth -ne $null ) {
        Write-Host Affected Host Details : -ForegroundColor DarkRed
        #$affectedesxiS = $CLOMDHealth.Hostname



        foreach ($affectedesxi in $CLOMDHealth.Hostname) {
    
    Write-Host " "
    $affectedHostState = Get-VMHost $affectedesxi
    $affectedHostConState = $affectedHostState.ConnectionState
    Write-Host Affected host $affectedesxi is in $affectedHostConState State 

    Write-Host $affectedesxi CLOMD STATUS is not healthy
    Write-Host " "
  
    $ESX = "Affected host $affectedesxi is in $affectedHostConState State"
    $ESXCLOMD = "CLOMD STATUS is not healthy on host $affectedesxi" 
    $nextact = "Restarting CLOMD Services from ESXiHost"

    $res = "<p>$ESX&nbsp;</p>" + "<p>$ESXCLOMD&nbsp;</p>" + "<p>$nextact&nbsp;</p>"
    $out = $outpre + $res

    return $out , $affectedesxi
        }
}

Else {
    Write-Host " "
    Write-Host CLOMD Process is healthy on all the hosts -ForegroundColor DarkGreen
    Write-Host " "
    $out = "No_Affected_host"
    
    return $out
}
 #$prints
 #return $OverallclomdStatus.Hostname , $OverallclomdStatus.ClomdStat
 

}  