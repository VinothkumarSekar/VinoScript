Connect-VIServer -Server xxx-vc13.xxxe.com -User xx -Password xxx

       
$Cluster = 'xxx-vc13c01'
            $vsanhealthservice = Get-VSANView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
            $cluster_view = (Get-Cluster -Name $Cluster).ExtensionData.MoRef
            $results = $vsanhealthservice.VsanQueryVcClusterHealthSummary($cluster_view,$null,$null,$true,$null,$null,'defaultView')
            #$results
            $healthCheckGroups = $results.Groups
            
            $PhysicalDisksHealth = $results.PhysicalDisksHealth
            #$PhysicalDisksHealth
if ($healthCheckGroups.GroupName -eq  "Physical disk") {
    if ($healthCheckGroups.GroupHealth -eq  "green"){
        Write-Host Overall operational status of Physical disk is healthy : -ForegroundColor Green

    }

    else {

        Write-Host Overall operational status of Physical disk is not healthy : -ForegroundColor DarkRed
    }


}



