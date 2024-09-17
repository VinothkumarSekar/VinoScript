Connect-CIServer -Server vcd01.xxx.com -User xxx -Password xxx



Get-OrgVdc -Name vcd01-xxx-t-ovdc1 | ft -autosize


Disconnect-CIServer * -Confirm:$false
