#!/usr/bin/env python3
"""
DOORS - Advanced Graphical Operating System
A fully-featured retro-futuristic desktop with file system, terminal, and more
"""

import tkinter as tk
from tkinter import font, messagebox, filedialog, scrolledtext
import random
import os
import json
from datetime import datetime
from pathlib import Path
import subprocess
import sys


class DoorsOS:
    """Main operating system class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DoorsOS V4.0")
        self.root.state('zoomed')  # Fullscreen on Windows
        self.root.configure(bg="#0a0e27")
        
       
        # File system management
        self.home_dir = Path("E:/DoorsOS")
        self.home_dir.mkdir(exist_ok=True)
        self.current_dir = self.home_dir
        
        # Initialize sample files
        self.init_sample_files()
        
        # Configure styles
        self.setup_fonts()
        self.setup_colors()
        
        # Windows management
        self.windows = []
        self.z_order = 0
        
        # Create UI
        self.create_desktop()
        self.create_taskbar()
        self.create_applications_menu()
        
    def init_sample_files(self):
        """Initialize sample files in home directory"""
        # Create sample directories
        (self.home_dir / "Documents").mkdir(exist_ok=True)
        (self.home_dir / "Pictures").mkdir(exist_ok=True)
        (self.home_dir / "Music").mkdir(exist_ok=True)
        (self.home_dir / "User").mkdir(exist_ok=True)

        # Create sample files if they don't exist
        readme_file = self.home_dir / "README.txt"
        if not readme_file.exists():
            readme_file.write_text(
                "DoorsOS V4.0\n"
                "====================================\n\n"
                "Welcome to DoorsOS!\n\n"
                "Features:\n"
                "- File Manager with real file operations\n"
                "- Advanced Text Editor with save/load\n"
                "- System Terminal/CMD\n"
                "- Matrix Animation\n"
                "- Paint Application\n"
                "- System Monitor\n\n"
                "Location: " + str(self.home_dir)
            )
        
    def setup_fonts(self):
        """Setup custom fonts for retro-futuristic look"""
        self.title_font = font.Font(family="Times New Roman", size=30, weight="bold")
        self.header_font = font.Font(family="Times New Roman", size=20, weight="bold")
        self.body_font = font.Font(family="Times New Roman", size=16)
        self.small_font = font.Font(family="Times New Roman", size=11)
        self.mono_font = font.Font(family="Times New Roman", size=11)
        
    def setup_colors(self):
        """Setup color palette"""
        self.colors = {
            "bg_dark": "#0a0e27",
            "bg_darker": "#05080f",
            "accent_cyan": "#244bc1",
            "accent_purple": "#b000ff",
            "accent_green": "#00ae42",
            "accent_orange": "#ff9900",
            "accent_red": "#f12c18",
            "text_light": "#e8e8e8",
            "text_dim": "#888888",
            "window_bg": "#1a1f3a",
        }
        
    def create_desktop(self):
        """Create the desktop background"""
        self.desktop = tk.Frame(self.root, bg=self.colors["bg_dark"])
        self.desktop.pack(fill=tk.BOTH, expand=True, pady=(0, 60))
        
        # Add animated title text
        title_frame = tk.Frame(self.desktop, bg=self.colors["bg_dark"])
        title_frame.pack(pady=30)
        
        title = tk.Label(
            title_frame,
            text="⬚ DoorsOS V4.0 ⬚",
            font=font.Font(family="Times New Roman", size=65, weight="bold"),
            fg=self.colors["accent_cyan"],
            bg=self.colors["bg_dark"]
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="DoorsOS V4.0",
            font=self.body_font,
            fg=self.colors["accent_purple"],
            bg=self.colors["bg_dark"]
        )
        subtitle.pack(pady=5)
        
        version = tk.Label(
            title_frame,
            text="v4.0",
            font=self.small_font,
            fg=self.colors["accent_green"],
            bg=self.colors["bg_dark"]
        )
        version.pack()
        
    def create_taskbar(self):
        """Create the taskbar at the bottom"""
        self.taskbar = tk.Frame(self.root, bg=self.colors["window_bg"], height=60)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.taskbar.pack_propagate(False)
        
        # Taskbar border
        border = tk.Frame(self.taskbar, bg=self.colors["accent_cyan"], height=3)
        border.pack(side=tk.TOP, fill=tk.X)
        
        # Left side - logo
        logo = tk.Label(
            self.taskbar,
            text="[D]",
            font=self.header_font,
            fg=self.colors["accent_cyan"],
            bg=self.colors["window_bg"]
        )
        logo.pack(side=tk.LEFT, padx=15)
        
        # Center - taskbar items
        self.taskbar_items = tk.Frame(self.taskbar, bg=self.colors["window_bg"])
        self.taskbar_items.pack(side=tk.LEFT, padx=10, expand=True)
        
        # Right side - system info
        self.system_info = tk.Label(
            self.taskbar,
            text="",
            font=self.small_font,
            fg=self.colors["accent_green"],
            bg=self.colors["window_bg"]
        )
        self.system_info.pack(side=tk.RIGHT, padx=15)
        
        self.update_system_info()
        
    def create_applications_menu(self):
        """Create application launcher buttons"""
        menu_frame = tk.Frame(self.taskbar, bg=self.colors["window_bg"])
        menu_frame.pack(side=tk.LEFT, padx=5)
        
        apps = [
            ("📝 Editor", self.open_advanced_editor),
            ("📂 Files", self.open_file_manager),
            ("💻 Terminal", self.open_terminal),
            ("📊 Matrix", self.open_matrix),
            ("🎨 Paint", self.open_paint),
            ("⚙️  System", self.open_system_monitor),
            ("🔧 Settings", self.open_settings),
        ]
        
        for label, command in apps:
            btn = tk.Button(
                menu_frame,
                text=label,
                command=command,
                font=self.small_font,
                bg=self.colors["accent_purple"],
                fg=self.colors["text_light"],
                activebackground=self.colors["accent_cyan"],
                activeforeground=self.colors["bg_dark"],
                relief=tk.RAISED,
                bd=2,
                padx=6,
                pady=3
            )
            btn.pack(side=tk.LEFT, padx=1)
            
    def update_system_info(self):
        """Update system info display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.system_info.config(text=f"[{current_time}] Windows Open: {len(self.windows)}")
        self.root.after(1000, self.update_system_info)
        
    def create_window(self, title, width, height, content_func):
        """Create a new draggable window"""
        window = DoorsWindow(
            self.root,
            title,
            width,
            height,
            content_func,
            self.colors,
            self.fonts,
            self.windows
        )
        self.windows.append(window)
        self.z_order += 1
        window.set_z_order(self.z_order)
        return window
        
    @property
    def fonts(self):
        return {
            "title": self.title_font,
            "header": self.header_font,
            "body": self.body_font,
            "small": self.small_font,
            "mono": self.mono_font,
        }
        
    # Application launchers
    def open_advanced_editor(self):
        """Open advanced text editor with save/load"""
        def content(frame):
            # Menu bar
            menu_frame = tk.Frame(frame, bg=self.colors["window_bg"])
            menu_frame.pack(fill=tk.X, padx=5, pady=5)
            
            file_data = {"current_file": None}
            
            def new_file():
                text.delete("1.0", tk.END)
                file_data["current_file"] = None
                
            def open_file():
                file_path = filedialog.askopenfilename(
                    initialdir=self.home_dir,
                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
                )
                if file_path:
                    with open(file_path, 'r') as f:
                        text.delete("1.0", tk.END)
                        text.insert("1.0", f.read())
                    file_data["current_file"] = file_path
                    
            def save_file():
                if file_data["current_file"]:
                    with open(file_data["current_file"], 'w') as f:
                        f.write(text.get("1.0", tk.END))
                    messagebox.showinfo("Save", f"File saved: {file_data['current_file']}")
                else:
                    save_as()
                    
            def save_as():
                file_path = filedialog.asksaveasfilename(
                    initialdir=self.home_dir,
                    defaultextension=".txt",
                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
                )
                if file_path:
                    with open(file_path, 'w') as f:
                        f.write(text.get("1.0", tk.END))
                    file_data["current_file"] = file_path
                    messagebox.showinfo("Save", f"File saved: {file_path}")
            
            buttons = [
                ("New", new_file),
                ("Open", open_file),
                ("Save", save_file),
                ("Save As", save_as),
            ]
            
            for label, cmd in buttons:
                btn = tk.Button(
                    menu_frame,
                    text=label,
                    command=cmd,
                    font=self.fonts["small"],
                    bg=self.colors["accent_green"],
                    fg=self.colors["bg_dark"],
                    relief=tk.RAISED,
                    bd=1,
                    padx=8
                )
                btn.pack(side=tk.LEFT, padx=2)
            
            # File info
            info_label = tk.Label(
                menu_frame,
                text="No file loaded",
                font=self.fonts["small"],
                fg=self.colors["accent_cyan"],
                bg=self.colors["window_bg"]
            )
            info_label.pack(side=tk.LEFT, padx=20)
            
            # Text editor
            text = scrolledtext.ScrolledText(
                frame,
                bg=self.colors["bg_darker"],
                fg=self.colors["accent_green"],
                font=self.fonts["body"],
                insertbackground=self.colors["accent_cyan"],
                relief=tk.FLAT,
                wrap=tk.WORD
            )
            text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            text.insert("1.0", "# Advanced Text Editor\n\nStart typing or open an existing file...")
            
            def update_info(*args):
                file_name = Path(file_data["current_file"]).name if file_data["current_file"] else "No file"
                info_label.config(text=f"File: {file_name}")
            
            text.bind("<<Change>>", update_info)
            
        self.create_window("Advanced Text Editor", 700, 500, content)
        
    def open_file_manager(self):
        """Open advanced file manager"""
        def content(frame):
            # Path bar
            path_frame = tk.Frame(frame, bg=self.colors["window_bg"])
            path_frame.pack(fill=tk.X, padx=5, pady=5)
            
            path_label = tk.Label(
                path_frame,
                text=f"Location: {self.current_dir}",
                font=self.fonts["small"],
                fg=self.colors["accent_cyan"],
                bg=self.colors["window_bg"]
            )
            path_label.pack(side=tk.LEFT)
            
            # Buttons frame
            btn_frame = tk.Frame(frame, bg=self.colors["window_bg"])
            btn_frame.pack(fill=tk.X, padx=5, pady=5)
            
            def refresh():
                listbox.delete(0, tk.END)
                try:
                    items = sorted(os.listdir(self.current_dir))
                    for item in items:
                        full_path = os.path.join(self.current_dir, item)
                        if os.path.isdir(full_path):
                            listbox.insert(tk.END, f"📁 {item}/")
                        else:
                            size = os.path.getsize(full_path)
                            listbox.insert(tk.END, f"📄 {item} ({size} bytes)")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            
            def go_back():
                parent = self.current_dir.parent
                if parent != self.current_dir:
                    self.current_dir = parent
                    path_label.config(text=f"Location: {self.current_dir}")
                    refresh()
            
            def new_folder():
                import tkinter.simpledialog as simpledialog
                name = simpledialog.askstring("New Folder", "Folder name:")
                if name:
                    try:
                        os.makedirs(os.path.join(self.current_dir, name), exist_ok=True)
                        refresh()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
            
            def delete_item():
                sel = listbox.curselection()
                if sel:
                    item = listbox.get(sel[0])
                    item_name = item.replace("📁 ", "").replace("📄 ", "").split(" (")[0].replace("/", "")
                    if messagebox.askyesno("Delete", f"Delete '{item_name}'?"):
                        try:
                            full_path = os.path.join(self.current_dir, item_name)
                            if os.path.isdir(full_path):
                                import shutil
                                shutil.rmtree(full_path)
                            else:
                                os.remove(full_path)
                            refresh()
                        except Exception as e:
                            messagebox.showerror("Error", str(e))
            
            def rename_item():
                import tkinter.simpledialog as simpledialog
                sel = listbox.curselection()
                if sel:
                    old_item = listbox.get(sel[0])
                    old_name = old_item.replace("📁 ", "").replace("📄 ", "").split(" (")[0].replace("/", "")
                    new_name = simpledialog.askstring("Rename", f"New name for '{old_name}':")
                    if new_name:
                        try:
                            old_path = os.path.join(self.current_dir, old_name)
                            new_path = os.path.join(self.current_dir, new_name)
                            os.rename(old_path, new_path)
                            refresh()
                        except Exception as e:
                            messagebox.showerror("Error", str(e))
            
            buttons = [
                ("⬅ Back", go_back),
                ("🔄 Refresh", refresh),
                ("➕ New Folder", new_folder),
                ("✏️ Rename", rename_item),
                ("🗑️ Delete", delete_item),
            ]
            
            for label, cmd in buttons:
                btn = tk.Button(
                    btn_frame,
                    text=label,
                    command=cmd,
                    font=self.fonts["small"],
                    bg=self.colors["accent_orange"],
                    fg=self.colors["bg_dark"],
                    relief=tk.RAISED,
                    bd=1,
                    padx=6
                )
                btn.pack(side=tk.LEFT, padx=2)
            
            # File listbox
            listbox = tk.Listbox(
                frame,
                bg=self.colors["bg_darker"],
                fg=self.colors["accent_green"],
                font=self.fonts["body"],
                relief=tk.FLAT,
                selectmode=tk.SINGLE
            )
            listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            def on_double_click(event):
                sel = listbox.curselection()
                if sel:
                    item = listbox.get(sel[0])
                    if "📁" in item:
                        item_name = item.replace("📁 ", "").replace("/", "")
                        self.current_dir = Path(self.current_dir) / item_name
                        path_label.config(text=f"Location: {self.current_dir}")
                        refresh()
            
            listbox.bind("<Double-Button-1>", on_double_click)
            
            refresh()
            
        self.create_window("File Manager", 700, 500, content)
        
    def open_terminal(self):
        """Open system terminal/command prompt"""
        def content(frame):
            # Input frame
            input_frame = tk.Frame(frame, bg=self.colors["window_bg"])
            input_frame.pack(fill=tk.X, padx=5, pady=5)
            
            prompt_label = tk.Label(
                input_frame,
                text="C:\\> ",
                font=self.fonts["mono"],
                fg=self.colors["accent_green"],
                bg=self.colors["window_bg"]
            )
            prompt_label.pack(side=tk.LEFT)
            
            # Output display
            output = tk.Text(
                frame,
                bg=self.colors["bg_darker"],
                fg=self.colors["accent_green"],
                font=self.fonts["mono"],
                insertbackground=self.colors["accent_cyan"],
                relief=tk.FLAT,
                wrap=tk.WORD
            )
            output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            output.config(state=tk.DISABLED)
            
            def append_output(text):
                output.config(state=tk.NORMAL)
                output.insert(tk.END, text + "\n")
                output.see(tk.END)
                output.config(state=tk.DISABLED)
            
            def execute_command(event=None):
                cmd = input_entry.get()
                input_entry.delete(0, tk.END)
                
                append_output(f"C:\\> {cmd}")
                
                if cmd.lower() == "clear":
                    output.config(state=tk.NORMAL)
                    output.delete("1.0", tk.END)
                    output.config(state=tk.DISABLED)
                elif cmd.lower() == "help":
                    append_output("DOORS Terminal Commands:")
                    append_output("  help      - Show this help")
                    append_output("  clear     - Clear screen")
                    append_output("  dir       - List directory")
                    append_output("  cd <path> - Change directory")
                    append_output("  mkdir <name> - Make directory")
                    append_output("  echo <text> - Print text")
                    append_output("  date      - Show current date/time")
                    append_output("  whoami    - Current user")
                    append_output("  systeminfo - System info")
                elif cmd.lower() == "date":
                    append_output(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                elif cmd.lower() == "whoami":
                    append_output(os.getenv("USERNAME", "DOORS_User"))
                elif cmd.lower() == "dir":
                    try:
                        items = os.listdir(self.current_dir)
                        for item in items:
                            append_output(f"  {item}")
                    except:
                        append_output("Error reading directory")
                elif cmd.lower() == "systeminfo":
                    append_output(f"OS: DOORS v2.0")
                    append_output(f"Python: {sys.version.split()[0]}")
                    append_output(f"Platform: {sys.platform}")
                    append_output(f"Home: {self.home_dir}")
                elif cmd.lower().startswith("echo "):
                    append_output(cmd[5:])
                elif cmd.lower().startswith("cd "):
                    path = cmd[3:].strip()
                    try:
                        new_path = Path(self.current_dir) / path
                        if new_path.exists() and new_path.is_dir():
                            self.current_dir = new_path
                            append_output(f"Changed to: {self.current_dir}")
                        else:
                            append_output("Path not found")
                    except:
                        append_output("Invalid path")
                elif cmd.strip():
                    try:
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                        if result.stdout:
                            append_output(result.stdout.strip())
                        if result.stderr:
                            append_output(result.stderr.strip())
                    except subprocess.TimeoutExpired:
                        append_output("Command timed out")
                    except Exception as e:
                        append_output(f"Error: {str(e)}")
            
            input_entry = tk.Entry(
                input_frame,
                bg=self.colors["bg_darker"],
                fg=self.colors["accent_green"],
                font=self.fonts["mono"],
                insertbackground=self.colors["accent_cyan"],
                relief=tk.FLAT
            )
            input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            input_entry.bind("<Return>", execute_command)
            input_entry.focus()
            
            append_output("DOORS Terminal v2.0")
            append_output("Type 'help' for commands")
            
        self.create_window("Terminal", 800, 500, content)
        
    def open_matrix(self):
        """Open matrix rain animation window"""
        def content(frame):
            canvas = tk.Canvas(
                frame,
                bg=self.colors["bg_darker"],
                relief=tk.FLAT,
                highlightthickness=0
            )
            canvas.pack(fill=tk.BOTH, expand=True)
            
            matrix_chars = "10101010101010101010101"
            columns = []
            
            def animate_matrix():
                canvas.delete("all")
                width = canvas.winfo_width()
                height = canvas.winfo_height()
                
                if width < 2 or height < 2:
                    canvas.after(50, animate_matrix)
                    return
                    
                col_count = width // 15
                
                if not columns:
                    columns.extend([
                        {
                            "x": i * 15,
                            "chars": [random.choice(matrix_chars) for _ in range(20)],
                            "y": random.randint(-500, 0)
                        }
                        for i in range(col_count)
                    ])
                
                for col in columns:
                    col["y"] += 15
                    for i, char in enumerate(col["chars"]):
                        y = col["y"] + i * 15
                        if 0 < y < height:
                            color = self.colors["accent_green"]
                            canvas.create_text(
                                col["x"],
                                y,
                                text=char,
                                fill=color,
                                font=self.fonts["header"]
                            )
                    
                    if col["y"] > height + 300:
                        col["y"] = -300
                        col["chars"] = [random.choice(matrix_chars) for _ in range(20)]
                
                canvas.after(50, animate_matrix)
            
            canvas.after(100, animate_matrix)
            
        self.create_window("Matrix Rain", 600, 400, content)
        
    def open_paint(self):
        """Open advanced paint application"""
        def content(frame):
            canvas = tk.Canvas(
                frame,
                bg=self.colors["bg_darker"],
                relief=tk.FLAT,
                cursor="cross",
                highlightthickness=0
            )
            
            drawing_state = {"last_x": 0, "last_y": 0, "color": self.colors["accent_cyan"], "brush_size": 2}
            
            # Toolbar
            toolbar = tk.Frame(frame, bg=self.colors["window_bg"])
            toolbar.pack(fill=tk.X, padx=5, pady=5)
            
            # Color buttons
            color_label = tk.Label(
                toolbar,
                text="Colors:",
                font=self.fonts["small"],
                fg=self.colors["text_light"],
                bg=self.colors["window_bg"]
            )
            color_label.pack(side=tk.LEFT, padx=5)
            
            colors_list = [
                ("Cyan", self.colors["accent_cyan"]),
                ("Purple", self.colors["accent_purple"]),
                ("Green", self.colors["accent_green"]),
                ("Orange", self.colors["accent_orange"]),
                ("Red", self.colors["accent_red"]),
                ("White", "#ffffff"),
                ("Black", "#000000"),
            ]
            
            for label, color in colors_list:
                btn = tk.Button(
                    toolbar,
                    text="■",
                    bg=color,
                    fg=self.colors["bg_dark"],
                    relief=tk.RAISED,
                    bd=2,
                    padx=4,
                    command=lambda c=color: drawing_state.update({"color": c})
                )
                btn.pack(side=tk.LEFT, padx=1)
            
            # Brush size
            tk.Label(
                toolbar,
                text="| Size:",
                font=self.fonts["small"],
                fg=self.colors["text_light"],
                bg=self.colors["window_bg"]
            ).pack(side=tk.LEFT, padx=5)
            
            size_var = tk.IntVar(value=2)
            for size in [1, 2, 4, 8]:
                rb = tk.Radiobutton(
                    toolbar,
                    text=str(size),
                    variable=size_var,
                    value=size,
                    bg=self.colors["window_bg"],
                    fg=self.colors["accent_green"],
                    selectcolor=self.colors["accent_purple"],
                    command=lambda s=size: drawing_state.update({"brush_size": s})
                )
                rb.pack(side=tk.LEFT, padx=2)
            
            # Clear button
            clear_btn = tk.Button(
                toolbar,
                text="🗑️ Clear",
                command=lambda: canvas.delete("all"),
                font=self.fonts["small"],
                bg=self.colors["accent_red"],
                fg=self.colors["text_light"],
                relief=tk.RAISED,
                bd=1,
                padx=8
            )
            clear_btn.pack(side=tk.RIGHT, padx=5)
            
            # Save button
            def save_drawing():
                file_path = filedialog.asksaveasfilename(
                    initialdir=self.home_dir / "Pictures",
                    defaultextension=".postscript",
                    filetypes=[("PostScript", "*.ps"), ("All Files", "*.*")]
                )
                if file_path:
                    canvas.postscript(file=file_path)
                    messagebox.showinfo("Save", f"Drawing saved to:\n{file_path}")
            
            save_btn = tk.Button(
                toolbar,
                text="💾 Save",
                command=save_drawing,
                font=self.fonts["small"],
                bg=self.colors["accent_green"],
                fg=self.colors["bg_dark"],
                relief=tk.RAISED,
                bd=1,
                padx=8
            )
            save_btn.pack(side=tk.RIGHT, padx=2)
            
            canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            def start_draw(event):
                drawing_state["last_x"] = event.x
                drawing_state["last_y"] = event.y
                
            def draw(event):
                canvas.create_line(
                    drawing_state["last_x"], drawing_state["last_y"],
                    event.x, event.y,
                    fill=drawing_state["color"],
                    width=drawing_state["brush_size"],
                    capstyle=tk.ROUND,
                    join=tk.ROUND,
                    smooth=True
                )
                drawing_state["last_x"] = event.x
                drawing_state["last_y"] = event.y
                
            canvas.bind("<Button-1>", start_draw)
            canvas.bind("<B1-Motion>", draw)
            
        self.create_window("Paint Studio", 700, 550, content)
        
    def open_system_monitor(self):
        """Open advanced system monitor"""
        def content(frame):
            info_frame = tk.Frame(frame, bg=self.colors["window_bg"])
            info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            try:
                import psutil
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
            except:
                cpu_percent = 0
                memory = None
                disk = None
            
            system_data = [
                ("OS Name:", "DOORS v2.0 Advanced"),
                ("Kernel:", "DoorsKernel 2.0.0"),
                ("Architecture:", "x64"),
                ("Python Version:", f"{sys.version.split()[0]}"),
                ("Memory Usage:", f"{memory.percent}%" if memory else "N/A"),
                ("CPU Usage:", f"{cpu_percent}%"),
                ("Home Directory:", str(self.home_dir)),
                ("Total Windows:", f"{len(self.windows)}"),
            ]
            
            for label, value in system_data:
                row = tk.Frame(info_frame, bg=self.colors["window_bg"])
                row.pack(fill=tk.X, pady=8)
                
                lbl = tk.Label(
                    row,
                    text=label,
                    font=self.fonts["header"],
                    fg=self.colors["accent_purple"],
                    bg=self.colors["window_bg"],
                    width=20,
                    anchor="w"
                )
                lbl.pack(side=tk.LEFT)
                
                val = tk.Label(
                    row,
                    text=value,
                    font=self.fonts["body"],
                    fg=self.colors["accent_green"],
                    bg=self.colors["window_bg"]
                )
                val.pack(side=tk.LEFT, padx=20)
            
            # Uptime
            import time
            uptime_seconds = int(time.time())
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            seconds = uptime_seconds % 60
            
            uptime_row = tk.Frame(info_frame, bg=self.colors["window_bg"])
            uptime_row.pack(fill=tk.X, pady=8)
            
            uptime_lbl = tk.Label(
                uptime_row,
                text="Uptime:",
                font=self.fonts["header"],
                fg=self.colors["accent_purple"],
                bg=self.colors["window_bg"],
                width=20,
                anchor="w"
            )
            uptime_lbl.pack(side=tk.LEFT)
            
            uptime_val = tk.Label(
                uptime_row,
                text=f"{hours}h {minutes}m {seconds}s",
                font=self.fonts["body"],
                fg=self.colors["accent_green"],
                bg=self.colors["window_bg"]
            )
            uptime_val.pack(side=tk.LEFT, padx=20)
                
        self.create_window("System Monitor", 550, 400, content)
        
    def open_settings(self):
        """Open settings window"""
        def content(frame):
            settings_frame = tk.Frame(frame, bg=self.colors["window_bg"])
            settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            sections = [
                ("Display Settings", [
                    ("Theme:", "Dark Retro-Futuristic"),
                    ("Resolution:", "Fullscreen"),
                    ("Brightness:", "100%"),
                ]),
                ("System Settings", [
                    ("OS:", "DOORS v2.0"),
                    ("Auto-save:", "Enabled"),
                    ("Sound:", "Disabled"),
                ]),
                ("File System", [
                    ("Home Directory:", str(self.home_dir)),
                    ("Used Space:", "~50MB"),
                    ("Free Space:", "~15GB"),
                ]),
            ]
            
            for section_title, items in sections:
                section = tk.LabelFrame(
                    settings_frame,
                    text=section_title,
                    font=self.fonts["header"],
                    fg=self.colors["accent_cyan"],
                    bg=self.colors["window_bg"],
                    borderwidth=2,
                    relief=tk.RIDGE
                )
                section.pack(fill=tk.X, pady=10)
                
                for label, value in items:
                    row = tk.Frame(section, bg=self.colors["window_bg"])
                    row.pack(fill=tk.X, pady=5, padx=10)
                    
                    lbl = tk.Label(
                        row,
                        text=label,
                        font=self.fonts["body"],
                        fg=self.colors["accent_green"],
                        bg=self.colors["window_bg"],
                        width=20,
                        anchor="w"
                    )
                    lbl.pack(side=tk.LEFT)
                    
                    val = tk.Label(
                        row,
                        text=value,
                        font=self.fonts["small"],
                        fg=self.colors["accent_orange"],
                        bg=self.colors["window_bg"]
                    )
                    val.pack(side=tk.LEFT, padx=20)
                
        self.create_window("Settings", 600, 450, content)


class DoorsWindow:
    """A draggable window for the DOORS OS"""
    
    def __init__(self, parent, title, width, height, content_func, colors, fonts, windows_list):
        self.parent = parent
        self.title_text = title
        self.width = width
        self.height = height
        self.colors = colors
        self.fonts = fonts
        self.windows_list = windows_list
        self.is_minimized = False
        
        # Get parent dimensions safely
        parent.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # Calculate safe random position
        max_x = max(50, parent_width - width - 100)
        max_y = max(50, parent_height - height - 150)
        
        self.x = random.randint(50, max_x)
        self.y = random.randint(50, max_y)
        
        # Create main window container
        self.window = tk.Frame(parent, bg=self.colors["window_bg"], relief=tk.RIDGE, bd=3)
        self.window.place(x=self.x, y=self.y, width=self.width, height=self.height)
        
        # Titlebar
        self.create_titlebar()
        
        # Content area
        self.content_frame = tk.Frame(self.window, bg=self.colors["window_bg"])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Add content
        try:
            content_func(self.content_frame)
        except Exception as e:
            error_label = tk.Label(
                self.content_frame,
                text=f"Error: {str(e)}",
                fg=self.colors["accent_red"],
                bg=self.colors["bg_darker"],
                font=self.fonts["body"]
            )
            error_label.pack(fill=tk.BOTH, expand=True)
        
        # Dragging state
        self.drag_data = {"x": 0, "y": 0}
        
        # Bind events
        self.titlebar.bind("<Button-1>", self.start_drag)
        self.titlebar.bind("<B1-Motion>", self.drag)
        self.window.bind("<Button-1>", self.on_focus)
        
    def create_titlebar(self):
        """Create the window titlebar"""
        self.titlebar = tk.Frame(
            self.window,
            bg=self.colors["accent_purple"],
            height=28
        )
        self.titlebar.pack(fill=tk.X)
        self.titlebar.pack_propagate(False)
        
        # Title text
        title_label = tk.Label(
            self.titlebar,
            text=f"◆ {self.title_text}",
            font=self.fonts["header"],
            fg=self.colors["bg_dark"],
            bg=self.colors["accent_purple"]
        )
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_btn = tk.Button(
            self.titlebar,
            text="✕",
            font=self.fonts["small"],
            fg=self.colors["bg_dark"],
            bg=self.colors["accent_purple"],
            activebackground=self.colors["accent_red"],
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=2,
            command=self.close
        )
        close_btn.pack(side=tk.RIGHT, padx=8)
        
    def start_drag(self, event):
        """Start window drag"""
        self.drag_data["x"] = event.x_root - self.x
        self.drag_data["y"] = event.y_root - self.y
        
    def drag(self, event):
        """Drag window"""
        new_x = event.x_root - self.drag_data["x"]
        new_y = event.y_root - self.drag_data["y"]
        self.x = new_x
        self.y = new_y
        self.window.place(x=self.x, y=self.y)
        
    def on_focus(self, event):
        """Bring window to front"""
        self.window.lift()
        
    def set_z_order(self, order):
        """Set z-order (stacking order)"""
        self.window.lift()
        
    def close(self):
        """Close the window"""
        if self in self.windows_list:
            self.windows_list.remove(self)
        self.window.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Handle fullscreen (different for different OS)
    try:
        if sys.platform == "win32":
            root.state('zoomed')
        else:
            root.attributes('-zoomed', True)
    except:
        root.geometry("1400x900")
    
    # Import simpledialog for rename functionality
    import tkinter.simpledialog as simpledialog
    
    # Create OS
    os = DoorsOS(root)
    
    # Force the window to render before creating child windows
    root.update_idletasks()
    
    # Start with one window open
    os.open_terminal()
    
    root.mainloop()


if __name__ == "__main__":
    main()