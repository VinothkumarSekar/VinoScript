
<#PSScriptInfo

.VERSION 1.0.0

.AUTHOR Vinothkumar Sekar

.COMPANYNAME

.COPYRIGHT

#>

<#

.DESCRIPTION
 This script connects to vCenter and checks for vSAN CLOMD status.
 If the COMD status is not healthy , it will find out the affected host and restart the CLOMD services from ESXi SSH
 

 #>

#------------------------Error handling--------------------------------------------------------

$ErrorActionPreference = 'Stop'

$vcUser = $env:vc_user
$pwd = $env:vc_pwd
$ESXUser = $env:esx_user
$ESXpwd = $env:esx_pwd
$vCenter = $env:vCenter_name

$VCsecure = ConvertTo-SecureString -String $pwd -AsPlainText -Force
$VCcred = New-Object -typename System.Management.Automation.PSCredential -argumentlist ($vcUser, $VCsecure)

Connect-VIServer -Server $vCenter -Credential $VCcred


       
$Cluster = $env:Cluster_name
            $vsanhealthservice = Get-VSANView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
            $cluster_view = (Get-Cluster -Name $Cluster).ExtensionData.MoRef
            $results = $vsanhealthservice.VsanQueryVcClusterHealthSummary($cluster_view,$null,$null,$true,$null,$null,'defaultView')
            $healthCheckGroups = $results.Groups
            $ClomdLiveness = $results.ClomdLiveness

    $OverallclomdStatus = $ClomdLiveness.ClomdLivenessResult

    #Write-Host "`nOverall Cluster health:" $results.OverallHealth"("$results.OverallHealthDescription")"
    Write-Host CLOMD STATUS OF HOSTS -ForegroundColor DarkCyan
    Write-Host " "
    $OverallclomdStatus | Select-Object Hostname, ClomdStat | Format-Table -AutoSize


  

    $CLOMDHealth = $OverallclomdStatus | Where-Object { $_.ClomdStat -ne 'alive' }
    $affectedesxiS = $CLOMDHealth.Hostname
    
    if ($CLOMDHealth -ne $null ) {
        Write-Host Affected Host Details : -ForegroundColor DarkRed
        #$affectedesxiS = $CLOMDHealth.Hostname



        foreach ($affectedesxi in $CLOMDHealth.Hostname) {
    
    Write-Host " "
    $affectedHostState = Get-VMHost $affectedesxi
    Write-Host Affected host $affectedesxi is in $affectedHostState.ConnectionState State 
    Write-Host $affectedesxi CLOMD STATUS is not healthy
        }
    



##===============================ESXi SSH ============================================================================================================

Write-Host " "
Write-Host Restarting CLOMD Services from ESXiHost -ForegroundColor DarkYellow
Write-Host " "


    $esxiHosts = @($affectedHostState.Name )



    $ESXsecure = ConvertTo-SecureString -String $ESXpwd -AsPlainText -Force
    $ESXcred = New-Object -typename System.Management.Automation.PSCredential -argumentlist ($ESXUser, $ESXsecure)


foreach ($esxiHost in $esxiHosts) { 

Connect-VIServer -Server $esxiHost -Credential $ESXcred

$sshresult = Get-VMHost -Name $esxiHost | ForEach-Object -Process {

    if((Get-VMHostService -VMHost $_).where({$_.Key -eq 'TSM-SSH'}).Running){

        $ssh = New-SSHSession -ComputerName $_.Name -Credential $cred -AcceptKey -KeepAliveInterval 5 

        Invoke-SSHCommand -SessionId $ssh.SessionId -Command " /etc/init.d/clomd status; /etc/init.d/clomd start; /etc/init.d/clomd restart; /etc/init.d/clomd status " -TimeOut 60

        Remove-SSHSession -SessionId $ssh.SessionId

    }
    
}
Write-Host " "
Write-Host Results from ESXi $esxiHost -ForegroundColor DarkCyan
    $TotalResult = $sshresult.Output

    $TotalResult

    }

    $vsanhealthservice = Get-VSANView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
    $cluster_view = (Get-Cluster -Name $Cluster).ExtensionData.MoRef
    $results = $vsanhealthservice.VsanQueryVcClusterHealthSummary($cluster_view,$null,$null,$true,$null,$null,'defaultView')
    $healthCheckGroups = $results.Groups
    $ClomdLiveness = $results.ClomdLiveness

$OverallclomdStatus = $ClomdLiveness.ClomdLivenessResult

#Write-Host "`nOverall Cluster health:" $results.OverallHealth"("$results.OverallHealthDescription")"
Write-Host CLOMD STATUS OF HOSTS -ForegroundColor DarkCyan
Write-Host " "
$OverallclomdStatus | Select-Object Hostname, ClomdStat


}

Else {
    Write-Host " "
    Write-Host CLOMD Process is healthy on all the hosts -ForegroundColor DarkGreen
    Write-Host " "
}

                
        
    
Get-Module -Name vmware.PowerCLI | Select-Object -Property Name,Version

