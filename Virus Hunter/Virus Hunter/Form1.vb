Public Class Form1

    Private Sub Button1_Click(sender As System.Object, e As System.EventArgs) Handles Button1.Click
        If My.Computer.FileSystem.FileExists("C:\virus.bat") Then ListBox1.Items.Add("virus.bat malware virus")
        If My.Computer.FileSystem.FileExists("C:\malware.bat") Then ListBox1.Items.Add("malware.bat malware")
        If My.Computer.FileSystem.FileExists("C:\Zhelatin.afg") Then ListBox1.Items.Add("Zhelatin.afg malware worms")
        If My.Computer.FileSystem.FileExists("C:\HELP_TO_DECRYPT_YOUR_FILES.txt") Then ListBox1.Items.Add("HELP_TO_DECRYPT_YOUR_FILES.txt ransomware")
        If My.Computer.FileSystem.FileExists("C:\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MRxCls.exe") Then ListBox1.Items.Add("MRxCls.exe trojan dropper")
        If My.Computer.FileSystem.FileExists("C:\abshdjakmz21.exe") Then ListBox1.Items.Add("abshdjakmz21.exe trojan dropper spyware")
        If My.Computer.FileSystem.FileExists("C:\smona1321265195858334061410e7871035f4e0f92b60a02ba7bd36de2155323akeygen.exe") Then ListBox1.Items.Add("smona1321265195858334061410e7871035f4e0f92b60a02ba7bd36de2155323akeygen.exe trojan worm backdoor")
        If My.Computer.FileSystem.FileExists("C:\d220c04a696b43849dfc245113142fdc.virus") Then ListBox1.Items.Add("d220c04a696b43849dfc245113142fdc.virus spyware trojan")
        If My.Computer.FileSystem.FileExists("C:\bocik.exe") Then ListBox1.Items.Add("bocik.exe spyware trojan")
        If My.Computer.FileSystem.FileExists("C:\usa.exe") Then ListBox1.Items.Add("usa.exe spyware trojan malware")
        If My.Computer.FileSystem.FileExists("C:\0_HELP_DECRYPT_FILES.html") Then ListBox1.Items.Add("0_HELP_DECRYPT_FILES.html ransomware")
        If My.Computer.FileSystem.FileExists("C:\vbbokccleiow.exe") Then ListBox1.Items.Add("vbbokccleiow.exe trojan malware ransomware")
        If My.Computer.FileSystem.FileExists("C:\annoncanon.exe") Then ListBox1.Items.Add("annoncanon.exe trojan")
        If My.Computer.FileSystem.FileExists("C:\phpkTLmyM") Then ListBox1.Items.Add("phpkTLmyM trojan malware riskware")
        If My.Computer.FileSystem.FileExists("C:\cbf1a3ce48f344bee6e47aa16ddd0424") Then ListBox1.Items.Add("cbf1a3ce48f344bee6e47aa16ddd0424 trojan malware riskware")
        If My.Computer.FileSystem.FileExists("C:\Crypted File.exe") Then ListBox1.Items.Add("Crypted File.exe trojan backdoor dropper worm")
    End Sub

    Private Sub ProgressBar1_Click(sender As System.Object, e As System.EventArgs) Handles ProgressBar1.Click

    End Sub

    Private Sub Button2_Click(sender As System.Object, e As System.EventArgs) Handles Button2.Click
        If ListBox1.SelectedItem = "BSOD.Activator" Then
            ListBox1.ClearSelected()

        End If
    End Sub

    Private Sub Button3_Click(sender As System.Object, e As System.EventArgs) Handles Button3.Click
        Dim targetfile As String
        Kill("C:\virus.bat")
        Kill("C:\malware.bat")
        Kill("C:\Zhelatin.afg")
        Kill("C:\HELP_TO_DECRYPT_YOUR_FILES.txt")
        Kill("C:\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MRxCls.exe")
        Kill("C:\abshdjakmz21.exe")
        Kill("C:\smona1321265195858334061410e7871035f4e0f892b60a02ba7bd36de2155323akeygen.exe")
        Kill("C:\d220c04a696b43849dfc245113142fdc.virus")
        Kill("C:\bocik.exe")
        Kill("C:\usa.exe")
        Kill("C:\0_HELP_DECRYPT_FILES.html")
        Kill("C:\vbbokccleiow.exe")
        Kill("C:\annoncanon.exe")
        Kill("C:\phpkTLmyM")
        Kill("C:\cbf1a3ce48f344bee6e47aa16ddd0424")
        Kill("C:\Crypted File.exe")
        targetfile = "c:\WINDOWS\system32\cmd.exe"
        Label1.Text = "Deleting selected files please wait"
        Timer1.Start()

    End Sub

    Private Sub Timer1_Tick(sender As System.Object, e As System.EventArgs) Handles Timer1.Tick
        Dim therandom As New Random
        Timer1.Interval = therandom.Next(100, 1000)
        On Error Resume Next
        If ProgressBar1.Value >= ProgressBar1.Maximum Then
            Label2.Text = "Deleted selected file(s)"
        Else
            ProgressBar1.Value += therandom.Next(1, 3)

        End If

    End Sub

    Private Sub Label3_Click(sender As System.Object, e As System.EventArgs) Handles Label3.Click

    End Sub
End Class
