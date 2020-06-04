package main

import "net/http"
import "os/exec"
import "strings"
import "os"
import "io/ioutil"
import "runtime"
import "github.com/fatih/color"




func main() {


	Repo := [6]string{"https://github.com/EgeBalci/ARCANUS/blob/master/SOURCE/ARCANUS.go", "https://github.com/EgeBalci/ARCANUS/raw/master/ARCANUS_x64", "https://github.com/EgeBalci/ARCANUS/raw/master/ARCANUS_x64.exe", "https://github.com/EgeBalci/ARCANUS/raw/master/ARCANUS_x86", "https://github.com/EgeBalci/ARCANUS/raw/master/ARCANUS_x86.exe", "https://github.com/EgeBalci/ARCANUS/raw/master/README.md"}

	if runtime.GOOS == "windows" {
		exec.Command("cmd", "/C", "msg ARCANUS Update Started...").Run()
		exec.Command("cmd", "/C", "del ARCANUS.go").Run()
		exec.Command("cmd", "/C", "del ARCANUS_x64.exe").Run()
		exec.Command("cmd", "/C", "del ARCANUS_x86.exe").Run()
		exec.Command("cmd", "/C", "del ARCANUS_x64").Run()
		exec.Command("cmd", "/C", "del ARCANUS_x86").Run()
		color.Blue("[*] Updating ARCANUS...\n\n")
		for i := 0; i < len(Repo); i++ {
			response, _ := http.Get(Repo[i])
			defer response.Body.Close();
    		body, _ := ioutil.ReadAll(response.Body);

    		Name := strings.Split(Repo[i], "/")
    		color.Green("#	"+string(Name[(len(Name)-1)])+"		[OK]")
    		file, _ := os.Create(string(Name[(len(Name)-1)]))

    		file.WriteString(string(body))
		}
		/*ARC, _ := exec.Command("cmd", "/C", "echo %PROCESSOR_ARCHITECTURE%").Output()
		if strings.Contains(string(ARC), "x86") || strings.Contains(string(ARC), "X86") {
			exec.Command("cmd", "/C", "ARCANUS_x86.exe").Start()
		}else if strings.Contains(string(ARC), "AMD64") {
			exec.Command("cmd", "/C", "ARCANUS_x64.exe").Start()
		}*/
		exec.Command("cmd", "/C", "msg * ARCANUS Updated Succesfuly !").Run()
	}else if runtime.GOOS == "linux" {
		exec.Command("sh", "-c", "zenity --info --text=\"ARCANUS Update Started... \"").Run()
		exec.Command("sh", "-c", "rm ARCANUS.go").Run()
		exec.Command("sh", "-c", "rm ARCANUS_x64.exe").Run()
		exec.Command("sh", "-c", "rm ARCANUS_x86.exe").Run()
		exec.Command("sh", "-c", "rm ARCANUS_x64").Run()
		exec.Command("sh", "-c", "rm ARCANUS_x86").Run()
		color.Blue("[*] Updating ARCANUS...\n\n")
		for i := 0; i < len(Repo); i++ {
			response, _ := http.Get(Repo[i])
			defer response.Body.Close();
    		body, _ := ioutil.ReadAll(response.Body);

    		Name := strings.Split(Repo[i], "/")
    		color.Green("#	"+string(Name[(len(Name)-1)])+"		[OK]")
    		file, _ := os.Create(string(Name[(len(Name)-1)]))

    		file.WriteString(string(body))
		}
		exec.Command("sh", "-c", "zenity --info --text=\"ARCANUS Updated Succesfuly !\"").Run()
		/*ARC, _ := exec.Command("sh", "-c", "uname -a").Output()
		if strings.Contains(string(ARC), "x86") || strings.Contains(string(ARC), "X86") {
			exec.Command("sh", "-c", "./ARCANUS_x86").Start()
		}else if strings.Contains(string(ARC), "amd64") {
			exec.Command("sh", "-c", "./ARCANUS_x64").Start()
		}*/

	}

}
