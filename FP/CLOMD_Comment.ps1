Connect-VIServer -Server xxx-vc17.xxx.com -User xxx.com -Password xxx

       
$Cluster = 'xxx-vc17c01'
            $vsanhealthservice = Get-VSANView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
            $cluster_view = (Get-Cluster -Name $Cluster).ExtensionData.MoRef
            $results = $vsanhealthservice.VsanQueryVcClusterHealthSummary($cluster_view,$null,$null,$true,$null,$null,'defaultView')
            $healthCheckGroups = $results.Groups
            $ClomdLiveness = $results.ClomdLiveness

    $OverallclomdStatus = $ClomdLiveness.ClomdLivenessResult

    #Write-Host "`nOverall Cluster health:" $results.OverallHealth"("$results.OverallHealthDescription")"
    Write-Host CLOMD STATUS OF HOSTS -ForegroundColor DarkCyan
    Write-Host " "
    #$OverallclomdStatus | Select-Object Hostname, ClomdStat | Format-Table -AutoSize
    $prints =@()
    foreach ($entity in $OverallclomdStatus) {
        #$formatt =   "On Host $entity.Hostname CLOMD service is in $entity.ClomdStat state"

        $hostN =  $entity.Hostname 
        $CLomdS = $entity.ClomdStat
        
        $print = "CLOMD status on Host $hostN is $CLomdS "

        $prints += $print
    }
         
    

  

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
$user = "root"
$password = "xxx"


$pswdSec = ConvertTo-SecureString -String $password -AsPlainText -Force

$cred = New-Object System.Management.Automation.PSCredential($user,$pswdSec)


foreach ($esxiHost in $esxiHosts) { 

Connect-VIServer -Server $esxiHost -Credential $cred 

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
$test =  $OverallclomdStatus | Select-Object Hostname, ClomdStat | Format-Table -AutoSize


}

Else {
    Write-Host " "
    Write-Host CLOMD Process is healthy on all the hosts -ForegroundColor DarkGreen
    Write-Host " "
}

                
$prints     
    
<# Backup testing
            $obj = new-object psobject
    $obj | Add-Member -MemberType NoteProperty -Name VM_Name -Value $healthCheckGroup.GroupTests.TestName | 
    $obj | Add-Member -MemberType NoteProperty -Name CPUSocket -Value $healthCheckGroup.GroupTests.TestHealth
   
    $result += $obj


$result | Format-Table -Autosize
#>


<# Current testing 

$healthCheckGroup | Select @{Name=”vSAN Service Name”;Expression={$healthCheckGroup.GroupTests.TestName}} | Where { $_.Name -like '*Performance*' } ,@{Name=”Status”;Expression={$healthCheckGroup.GroupTests.TestHealth}}

#>
