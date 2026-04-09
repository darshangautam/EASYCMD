import customtkinter as ctk
import os
import subprocess
import sys
import ctypes
import threading
from tkinter import messagebox

# ====================== AUTO REQUEST ADMINISTRATOR RIGHTS ======================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        try:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join(sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}" {params}', None, 1
            )
            sys.exit(0)
        except Exception:
            pass

run_as_admin()

# ====================== MODERN UI CONFIGURATION ======================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class EasyCMDPro(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("EasyCMD Pro - Ultimate Master Edition")
        self.geometry("1400x950")
        
        self.current_dir = os.getcwd()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Top Navigation ---
        self.nav_frame = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="transparent")
        self.nav_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        self.tab_navigator = ctk.CTkSegmentedButton(
            self.nav_frame, 
            values=["General", "WiFi", "Administrator", "Advanced"],
            command=self.switch_tab,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.tab_navigator.set("General")
        self.tab_navigator.pack(side="left", fill="x", expand=True)

        # --- Sidebar ---
        self.sidebar = ctk.CTkScrollableFrame(self, width=450, label_text="System Toolbox")
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))
        
        # --- Output Area ---
        self.output_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.output_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        self.output_text = ctk.CTkTextbox(
            self.output_frame, wrap="word", font=("Consolas", 13),
            fg_color="transparent", text_color="#e0e0e0"
        )
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.output_text.configure(state="disabled")

        self.progress_bar = ctk.CTkProgressBar(self.output_frame, orientation="horizontal", height=4)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 5))
        self.progress_bar.set(0)
        self.progress_bar.configure(mode="indeterminate")

        # --- Bottom Input Area ---
        self.input_frame = ctk.CTkFrame(self, height=70, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))
        
        self.prompt_label = ctk.CTkLabel(self.input_frame, text=">", font=("Consolas", 16, "bold"))
        self.prompt_label.pack(side="left", padx=(5, 10))

        self.input_entry = ctk.CTkEntry(
            self.input_frame, placeholder_text="Command ready...",
            font=("Consolas", 14), height=45
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.process_command)
        
        self.run_btn = ctk.CTkButton(
            self.input_frame, text="Execute", width=100, height=45, 
            command=self.process_command, font=ctk.CTkFont(weight="bold")
        )
        self.run_btn.pack(side="right")

        self.update_sidebar("General")
        self.print_welcome()

    def print_welcome(self):
        status = "ADMIN" if is_admin() else "USER"
        self.print_output(f"EasyCMD Pro | Mode: {status}\n", "#1f6aa5")
        self.print_output(f"Path: {self.current_dir}\n", "gray")

    def switch_tab(self, tab_name):
        self.after(10, lambda: self.update_sidebar(tab_name))

    def add_section_header(self, text):
        header = ctk.CTkLabel(self.sidebar, text=f"--- {text} ---", 
                            text_color="#5a5a5a", font=ctk.CTkFont(size=12, weight="bold"))
        header.pack(fill="x", pady=(15, 5), padx=5)

    def build_buttons(self, items):
        for text, cmd in items:
            btn = ctk.CTkButton(
                self.sidebar, text=text, anchor="w", fg_color="transparent",
                text_color="#d1d1d1", hover_color="#2b2b2b", height=32,
                command=lambda c=cmd, t=text: self.run_button_command(c, t)
            )
            btn.pack(fill="x", pady=1, padx=5)

    def update_sidebar(self, tab_name):
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        if tab_name == "General":
            self.add_section_header("CORE NAVIGATION")
            self.build_buttons([
                ("🧹 Clear Screen", "clear"), ("📁 List Files", "ls"),
                ("⬆️ Go Up One Level", "cd .."), ("📍 Current Path", "pwd"),
                ("⚡ Task List", "tasklist"), ("🔎 Active Connections", "netstat -an"),
            ])
            self.add_section_header("HARDWARE SPECS")
            self.build_buttons([
                ("🖥️ System Info", "systeminfo"),
                ("🏗️ OS Architecture", "powershell -Command \"(Get-CimInstance Win32_OperatingSystem).OSArchitecture\""),
                ("📋 Motherboard Info", "powershell -Command \"Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product\""),
                ("⚡ CPU Details", "powershell -Command \"Get-CimInstance Win32_Processor | Select-Object Name, MaxClockSpeed, NumberOfCores\""),
                ("💾 BIOS Version", "powershell -Command \"(Get-CimInstance Win32_BIOS).SMBIOSBIOSVersion\""),
                ("🎮 GPU Model", "powershell -Command \"Get-CimInstance Win32_VideoController | Select-Object Name\""),
                ("📺 Monitor Resolution", "powershell -Command \"Get-CimInstance Win32_VideoController | Select-Object CurrentHorizontalResolution, CurrentVerticalResolution\""),
                ("🚦 Storage Status", "powershell -Command \"Get-PhysicalDisk | Select-Object FriendlyName, HealthStatus\""),
            ])
            self.add_section_header("FILE & DISK TOOLS")
            self.build_buttons([
                ("🌲 Tree View (Folders)", "tree"), ("🌲 Tree View (Files)", "tree /f"),
                ("🔎 Find a File", "where /r C:\\ filename.txt"),
                ("⚖️ Compare Two Files", "fc file1.txt file2.txt"),
                ("📂 Folder Size (Current)", "powershell -Command \"gci . -recurse | measure-object -property length -sum | select @{Name='Size(MB)';Expression={$_.sum / 1MB}}\""),
                ("🗄️ Disk Management UI", "diskmgmt.msc"), ("🧹 Defragment C:", "defrag C: /O"),
                ("🗑️ Temp Cleanup (Silent)", "del /q/f/s %TEMP%\\* 2>nul"), ("🔒 File Attributes", "attrib"),
                ("🗜️ Compress Item", "compact /c /s"),
            ])
            self.add_section_header("WINDOWS UTILITIES")
            self.build_buttons([
                ("🎛️ Control Panel", "control"), ("➕ Programs & Features", "appwiz.cpl"),
                ("⌨️ Screen Keyboard", "osk"), ("✂️ Snipping Tool", "snippingtool"),
                ("🔣 Character Map", "charmap"), ("🧮 Calculator", "calc"),
                ("📝 Sticky Notes", "stikynot"), ("🔋 Battery Report", "powercfg /batteryreport"),
                ("💾 Disk Space (Table)", "powershell -Command \"Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{Name='Size(GB)';Expression={[math]::round($_.Used/1GB,2)}}, @{Name='Free(GB)';Expression={[math]::round($_.Free/1GB,2)}} | Format-Table\""),
                ("⚙️ Open Task Manager", "taskmgr"), ("📝 Detailed Specs", "dxdiag"),
                ("🛠️ Device Manager", "devmgmt.msc"), ("📦 List Installed Apps", "powershell -Command \"Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName\""),
            ])

        elif tab_name == "WiFi":
            show_pass_cmd = 'powershell -Command "netsh wlan show profiles | Select-String \':\\s(.+)\' | ForEach-Object { $n=$_.Matches.Groups[1].Value.Trim(); $out=(netsh wlan show profile name=\\\"$n\\\" key=clear); $res=($out | Select-String \'Key Content\\W+\\:(.+)\'); if ($res) { $p=$res.Matches.Groups[1].Value.Trim(); Write-Host \\\"$n : $p\\\" } else { Write-Host \\\"$n : (Open Network)\\\" } }"'
            self.add_section_header("SCANNING")
            self.build_buttons([
                ("📡 Nearby Networks", "netsh wlan show networks"),
                ("📡 Nearby (BSSID)", "netsh wlan show networks mode=bssid"),
                ("📋 List Saved Profiles", "netsh wlan show profiles"),
                ("🔑 SHOW ALL PASSWORDS", show_pass_cmd),
                ("📶 WiFi Interface Info", "netsh wlan show interface"),
            ])
            self.add_section_header("NETWORK CONFIG")
            self.build_buttons([
                ("🔌 Disconnect WiFi", "netsh wlan disconnect"),
                ("🌐 Connect to SSID", "netsh wlan connect name=\"SSID_HERE\""),
                ("🧹 Flush DNS Cache", "ipconfig /flushdns"),
                ("🔵 Set Cloudflare DNS", "powershell -Command \"Set-DnsClientServerAddress -InterfaceAlias 'Wi-Fi' -ServerAddresses ('1.1.1.1','1.0.0.1')\""),
                ("🟢 Set Google DNS", "powershell -Command \"Set-DnsClientServerAddress -InterfaceAlias 'Wi-Fi' -ServerAddresses ('8.8.8.8','8.8.4.4')\""),
                ("⚪ Reset DNS (DHCP)", "powershell -Command \"Set-DnsClientServerAddress -InterfaceAlias 'Wi-Fi' -ResetServerAddresses\""),
                ("🔍 Ping Google", "ping google.com"), ("🔍 Ping Cloudflare", "ping 1.1.1.1"),
                ("🆔 IP Config", "ipconfig"), ("🆔 IP Config (Full)", "ipconfig /all"),
            ])

        elif tab_name == "Administrator":
            self.add_section_header("USER CONTROLS")
            self.build_buttons([
                ("🔑 Change Password", "net user USERNAME NEWPASSWORD"),
                ("➕ Add New User", "net user NEWUSER PASSWORD /add"),
                ("❌ Delete User", "net user USERNAME /delete"),
                ("👥 List All Users", "net user"),
                ("🔓 Activate Hidden Admin", "net user administrator /active:yes"),
            ])
            self.add_section_header("SYSTEM MAINTENANCE")
            self.build_buttons([
                ("🛠️ System File Checker", "sfc /scannow"),
                ("🔍 DISM Health Scan", "DISM /Online /Cleanup-Image /ScanHealth"),
                ("💉 DISM Restore Health", "DISM /Online /Cleanup-Image /RestoreHealth"),
                ("💾 CHKDSK Fix Disk", "chkdsk C: /f /r"),
                ("🧹 Deep Cleanup", "Dism.exe /online /Cleanup-Image /StartComponentCleanup"),
            ])
            self.add_section_header("SECURITY & POWER")
            self.build_buttons([
                ("🛡️ Disable Firewall", "netsh advfirewall set allprofiles state off"),
                ("🛡️ Enable Firewall", "netsh advfirewall set allprofiles state on"),
                ("🔄 Reset Network", "netsh winsock reset"),
                ("🔌 Shutdown PC", "shutdown /s /f /t 0"),
                ("🔄 Restart PC", "shutdown /r /f /t 0"),
                ("🔋 Power Study report", "powercfg /sleepstudy"),
            ])

        elif tab_name == "Advanced":
            self.add_section_header("ACTIVATION")
            self.build_buttons([
                ("🪟 Windows/Office Activation (MAS)", "powershell -Command \"irm https://get.activated.win | iex\""),
                ("⏳ IDM Trial Reset/Freeze", "echo [Add IDM Command Here]"),
            ])
            self.add_section_header("RECOVERY")
            self.build_buttons([
                ("☣️ RUN TRON (Manual Only)", "powershell -Command \"Start-Process cmd -ArgumentList '/c cd /d %USERPROFILE%\\Desktop\\tron && tron.bat -a -p' -Verb RunAs\""),
                ("📥 Download Tron", "powershell -Command \"Invoke-WebRequest -Uri 'https://bmrf.org/repos/tron/Tron%20v12.0.8%20(2025-01-09).exe' -OutFile '%USERPROFILE%\\Desktop\\tron_setup.exe'\""),
            ])
            self.add_section_header("SYSTEM TWEAKS")
            self.build_buttons([
                ("🌡️ Check CPU Temp", "powershell -Command \"get-wmiobject msacpi_thermalzonetemperature -namespace root/wmi | Select-Object @{n='Temp';e={($_.CurrentTemperature - 2732)/10}}\""),
                ("📦 Uninstall Built-in App", "powershell -Command \"Get-AppxPackage *APPNAME* | Remove-AppxPackage\""),
                ("🚀 Ultimate Perf Mode", "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"),
                ("🔄 Restart Explorer", "taskkill /f /im explorer.exe && start explorer.exe"),
                ("🕒 System Boot Time", "systeminfo | find \"System Boot Time\""),
                ("📊 Resource Monitor", "resmon"),
                ("🛡️ Defender Quick Scan", "\"%ProgramFiles%\\Windows Defender\\MpCmdRun.exe\" -Scan -ScanType 1"),
                ("⚙️ System Config", "msconfig"),
            ])

    def run_button_command(self, command: str, title: str):
        # List of critical functions that trigger a confirmation popup
        sensitive = ["Uninstall", "Temp", "Activation", "Reset", "Firewall", "Shutdown", "Restart", "Delete User", "Tron", "Explorer"]
        if any(keyword in title for keyword in sensitive):
            if not messagebox.askyesno("Sensitive Operation", f"Are you sure you want to run: {title}?"):
                return

        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, command)
        
        # Auto-run if no user variables are needed
        placeholders = ["USERNAME", "NEWPASSWORD", "NEWUSER", "SSID_HERE", "filename.txt", "APPNAME", "file1.txt"]
        if not any(x in command for x in placeholders):
            self.process_command()

    def print_output(self, text: str, color: str = "white"):
        self.output_text.configure(state="normal")
        tag = f"tag_{color}"
        self.output_text.tag_config(tag, foreground=color)
        self.output_text.insert("end", text, tag)
        self.output_text.see("end")
        self.output_text.configure(state="disabled")

    def process_command(self, event=None):
        user_input = self.input_entry.get().strip()
        if not user_input: return
        self.print_output(f"\n(easycmd) {os.path.basename(self.current_dir)}> {user_input}\n", "#55FF55")
        
        parts = user_input.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        self.input_entry.delete(0, "end")

        if cmd in ["ls", "dir"]: self.do_ls(args)
        elif cmd == "cd": self.do_cd(args)
        elif cmd == "pwd": self.do_pwd()
        elif cmd in ["clear", "cls"]: self.clear_screen()
        elif cmd in ["exit", "quit"]: self.quit_app()
        else:
            thread = threading.Thread(target=self.run_system_command, args=(user_input,))
            thread.daemon = True
            thread.start()

    def do_ls(self, args=""):
        target = os.path.join(self.current_dir, args) if args else self.current_dir
        try:
            items = os.listdir(target)
            for item in sorted(items):
                color = "#3b8ed0" if os.path.isdir(os.path.join(target, item)) else "white"
                self.print_output(f"{item}{'/' if color == '#3b8ed0' else ''}\n", color)
        except Exception as e:
            self.print_output(f"Error: {e}\n", "#FF5555")

    def do_cd(self, args):
        if not args: return
        try:
            new_path = os.path.abspath(os.path.join(self.current_dir, args))
            if os.path.isdir(new_path):
                os.chdir(new_path)
                self.current_dir = os.getcwd()
                self.print_output(f"→ {self.current_dir}\n", "#3b8ed0")
            else:
                self.print_output(f"Folder not found: {args}\n", "#FF5555")
        except Exception as e:
            self.print_output(f"Error: {e}\n", "#FF5555")

    def do_pwd(self):
        self.print_output(f"Current directory: {self.current_dir}\n", "#3b8ed0")

    def run_system_command(self, command):
        self.run_btn.configure(state="disabled")
        self.progress_bar.start()
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True,
                                    cwd=self.current_dir)
            if result.stdout: self.print_output(result.stdout + "\n", "white")
            if result.stderr: self.print_output(result.stderr + "\n", "#FF5555")
        except Exception as e:
            self.print_output(f"Failed to execute: {e}\n", "#FF5555")
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.run_btn.configure(state="normal")

    def clear_screen(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")

    def quit_app(self):
        self.after(500, self.destroy)

if __name__ == "__main__":
    app = EasyCMDPro()
    app.mainloop()