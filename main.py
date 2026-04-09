import customtkinter as ctk
import os
import subprocess
import sys
import ctypes

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
            pass  # User denied UAC

run_as_admin()
# ============================================================================

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class EasyCMDGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("EasyCMD - Simpler & Friendlier Command Prompt (Admin)")
        self.geometry("1180x740")
        self.minsize(980, 580)
        
        self.current_dir = os.getcwd()
        self.current_tab = "General"
        
        # Layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        # Top Tabs
        self.tab_frame = ctk.CTkFrame(self, height=55)
        self.tab_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))
        self.create_tabs()
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=270, corner_radius=0)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        self.sidebar.grid_propagate(False)
        
        # Output Area
        self.output_text = ctk.CTkTextbox(self, wrap="word", font=("Consolas", 13))
        self.output_text.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="nsew")
        self.output_text.configure(state="disabled")
        
        # Input Area
        self.input_frame = ctk.CTkFrame(self, height=52)
        self.input_frame.grid(row=2, column=1, padx=(5, 10), pady=(0,10), sticky="ew")
        self.input_frame.grid_propagate(False)
        
        self.prompt_label = ctk.CTkLabel(self.input_frame, text="(easycmd)", font=("Consolas", 14, "bold"))
        self.prompt_label.pack(side="left", padx=(15, 5))
        
        self.input_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type any command here...", font=("Consolas", 14))
        self.input_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.input_entry.bind("<Return>", self.process_command)
        
        self.send_button = ctk.CTkButton(self.input_frame, text="Run", width=85, command=self.process_command)
        self.send_button.pack(side="right", padx=10)
        
        # Welcome Message
        if is_admin():
            self.print_output("🚀 Welcome to EasyCMD (Running as Administrator)\n", "green")
            self.print_output("All features including WiFi passwords are now available!\n", "cyan")
        else:
            self.print_output("🚀 Welcome to EasyCMD\n", "cyan")
            self.print_output("⚠️ Some features require Administrator rights.\n", "yellow")
        
        self.print_output(f"Current directory: {self.current_dir}\n\n", "blue")
        
        self.update_sidebar()
        self.input_entry.focus()

    def create_tabs(self):
        tabs = ["General", "WiFi", "Administrator", "Advanced"]
        self.tab_buttons = {}
        
        for tab in tabs:
            btn = ctk.CTkButton(
                self.tab_frame,
                text=tab,
                width=150,
                height=42,
                corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda t=tab: self.switch_tab(t)
            )
            btn.pack(side="left", padx=10, pady=8)
            self.tab_buttons[tab] = btn
        
        self.tab_buttons["General"].configure(fg_color="#1f6aa5")

    def switch_tab(self, tab_name: str):
        self.current_tab = tab_name
        for btn in self.tab_buttons.values():
            btn.configure(fg_color="transparent")
        self.tab_buttons[tab_name].configure(fg_color="#1f6aa5")
        self.update_sidebar()

    def update_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()
        
        title = ctk.CTkLabel(self.sidebar, text=f"{self.current_tab} Commands", 
                            font=ctk.CTkFont(size=17, weight="bold"))
        title.pack(pady=(25, 18), padx=20)
        
        if self.current_tab == "General":
            button_list = [
                ("🧹 Clear Screen", "clear"),
                ("📁 List Files", "ls"),
                ("⬆️ Go Up One Level", "cd .."),
                ("📍 Show Current Path", "pwd"),
                ("🖥️ System Information", "systeminfo"),
                ("⚡ Show Running Tasks", "tasklist"),
                ("📅 Date & Time", "echo %date% %time%"),
                ("💾 Disk Usage", "wmic logicaldisk get caption,size,freespace"),
                ("🔋 Battery Status", "powercfg /batteryreport"),
                ("📦 List Installed Programs", "wmic product get name,version"),
                ("🖥️ Computer Name", "hostname"),
                ("⏰ System Boot Time", "systeminfo | find \"System Boot Time\""),
                ("🔍 Check Windows Activation", "slmgr /xpr"),
                ("📊 High Memory Usage", "tasklist /fi \"memusage gt 10000\""),
            ]
        elif self.current_tab == "WiFi":
            button_list = [
                ("📡 Show Nearby WiFi Networks", "netsh wlan show networks"),
                ("📋 List All Saved WiFi Networks", "netsh wlan show profiles"),
                ("🔑 Show All Saved WiFi + Passwords", "netsh wlan show profiles key=clear"),
                ("📶 Show Current WiFi Info", "netsh wlan show interface"),
                ("🔌 Disconnect from WiFi", "netsh wlan disconnect"),
            ]
        else:
            button_list = []   # Administrator & Advanced still empty

        for text, cmd in button_list:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                width=230,
                height=48,
                corner_radius=12,
                font=ctk.CTkFont(size=14),
                command=lambda c=cmd: self.run_button_command(c)
            )
            btn.pack(pady=7, padx=20)

    def run_button_command(self, command: str):
        self.print_output(f"\n▶ Executing: {command}\n", "green")
        
        if command == "ls":
            self.do_ls()
        elif command.startswith("cd "):
            self.do_cd(command[3:].strip())
        elif command == "pwd":
            self.do_pwd()
        elif command == "clear":
            self.clear_screen()
        else:
            self.run_system_command(command)
        
        self.update_title()

    def print_output(self, text: str, color: str = "white"):
        self.output_text.configure(state="normal")
        tag = f"tag_{color}"
        self.output_text.tag_config(tag, foreground=color)
        self.output_text.insert("end", text, tag)
        self.output_text.see("end")
        self.output_text.configure(state="disabled")

    def process_command(self, event=None):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        
        self.print_output(f"\n(easycmd) {os.path.basename(self.current_dir)}> {user_input}\n", "green")
        
        parts = user_input.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in ["ls", "dir"]:
            self.do_ls(args)
        elif cmd == "cd":
            self.do_cd(args)
        elif cmd == "pwd":
            self.do_pwd()
        elif cmd in ["clear", "cls"]:
            self.clear_screen()
        elif cmd in ["exit", "quit"]:
            self.quit_app()
            return
        else:
            self.run_system_command(user_input)
        
        self.input_entry.delete(0, "end")
        self.update_title()

    # ====================== Core Command Functions ======================
    def do_ls(self, args=""):
        target = os.path.join(self.current_dir, args) if args else self.current_dir
        try:
            items = os.listdir(target)
            for item in sorted(items):
                color = "blue" if os.path.isdir(os.path.join(target, item)) else "white"
                self.print_output(f"{item}{'/' if color == 'blue' else ''}\n", color)
        except Exception as e:
            self.print_output(f"Error: {e}\n", "red")

    def do_cd(self, args):
        if not args:
            self.print_output("Usage: cd <folder or ..>\n", "yellow")
            return
        try:
            new_path = os.path.join(self.current_dir, args)
            if os.path.isdir(new_path):
                os.chdir(new_path)
                self.current_dir = os.getcwd()
                self.print_output(f"→ {self.current_dir}\n", "blue")
            else:
                self.print_output(f"Folder not found: {args}\n", "red")
        except Exception as e:
            self.print_output(f"Error: {e}\n", "red")

    def do_pwd(self):
        self.print_output(f"Current directory: {self.current_dir}\n", "blue")

    def clear_screen(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        self.print_output("✅ Screen cleared.\n\n", "yellow")

    def run_system_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True,
                                  cwd=self.current_dir, timeout=45)
            if result.stdout.strip():
                self.print_output(result.stdout + "\n", "white")
            if result.stderr.strip():
                self.print_output(result.stderr + "\n", "red")
        except subprocess.TimeoutExpired:
            self.print_output("⏰ Command timed out.\n", "red")
        except Exception as e:
            self.print_output(f"Failed: {e}\n", "red")

    def quit_app(self):
        self.print_output("\nGoodbye! 👋\n", "red")
        self.after(800, self.destroy)

    def update_title(self):
        self.title(f"EasyCMD - {os.path.basename(self.current_dir)}")


if __name__ == "__main__":
    app = EasyCMDGUI()
    app.mainloop()