<#PSScriptInfo

.VERSION 1.0.0

.AUTHOR Vinothkumar Sekar <vinoxxx.com>

.COMPANYNAME xxx

.COPYRIGHT

#>

<#

.DESCRIPTION
 This script connects to vCenter and checks for vSAN Cluster usage.
 If the disk balance health status is more then 85%, it sends mail to top users of sandbox OVDC and checks for ESXi health status
 If the cluster doesn't have sandbox ovdc , it will pop up message "The cluster dosen't have sandbox ovdc, Send the ticket to cloudops to check for the possibilities to reduce the usage "".

 #>

#Get-Credential | Export-Clixml -Path C:\Users\vinoths\Desktop\Automation\vCenterADM.xml


#Write-Host "Received vCenter creds form local for authentication... " -ForegroundColor Cyan

#$vCenterCred = Import-Clixml -Path C:\Users\vinoths\Desktop\Automation\vCenterADM.xml

#------------------------Error handling--------------------------------------------------------

$ErrorActionPreference = 'Stop'

#-------------------------Details from jenkins---------------------------------------------------

Write-Host "Getting details from Jenkins..." -ForegroundColor Green




$server = "vcenter-xxxx.com"

$Cluster = "xxx-VSAN-Cluster"

#$server = $env:VC_Name
#$Cluster = $env:Cluster_Name



#$vcUser = $env:vc_user
#$pwd = $env:vc_pwd

$vcUser = "xxx"
$pwrd = “xxx”

$secure = ConvertTo-SecureString -String $pwrd -AsPlainText -Force
$VCcred = New-Object -typename System.Management.Automation.PSCredential -argumentlist ($vcUser, $secure)






#Write-Host "Connecting to Server $server... " -ForegroundColor Cyan
Write-Host "Gathering Cluster Information from Jenkins..."




#-------------------------Getting details from vRops---------------------------------------------------



Write-Host " "
Write-Host "======Searching for Cluster '$Cluster' on vCenter Server=$server======"

# Adding certificate exception to prevent API errors


$vcConnect = Connect-VIServer -server $server -Credential $VCcred -Force

Write-Host "Connection established to Server $server... " -ForegroundColor Cyan








#--------------------------Calulating vSAN Datastore-----------------------------------------


Write-Host "Getting details of vSanDatastore from $server... " -ForegroundColor Cyan

#Below is to get all the vSAN DS
#$vSANDatastore = Get-Cluster  | Get-Datastore -Server $server | Where-Object { $_.Name -like '*vsan*' } 

$vSANDatastore = Get-cluster $Cluster | Get-Datastore | Where-Object { $_.Name -like '*vsan*' }

$Capacity = $vSANDatastore.CapacityGB
$CapacityRound = [math]::round($Capacity, 1)
$Free = $vSANDatastore.FreeSpaceGB
$FreeRound = [math]::round($Free, 1)
$Used = $Capacity - $Free
$UsedRound = [math]::round($Used, 1)
#$usedPercent = $Used *100 / (($Capacity),0)

$UsedPercent = (($Used)*100/$Capacity)
$usedPercentRound = [math]::round($UsedPercent, 1)

#$Results = @()
$Result = Get-cluster $Cluster | Get-Datastore | 
          Where-Object { $_.Name -like '*vsan*' } | 
          Select @{N="DataStoreName";E={$_.Name}},
                 @{N="FreeSpace(%)";E={[math]::Round(($_.FreeSpaceGB)/($_.CapacityGB)*100,0)}}, #| Where {$_."Percentage(<20%)" -le 20}
                 @{N="FreeSpaceGB";E={$_.FreeSpaceGB}},
                 @{N="TotalCapacityGB";E={$_.CapacityGB}}

#$Result | Export-Csv -Path $ENV:WORKSPACE\DatastoreDetails.csv -NoTypeInformation
$Result






