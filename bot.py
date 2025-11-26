import asyncio, disnake, sys, os, subprocess, time, logging
from disnake.ext import commands

from core.config import DISCORD_TOKEN
from core.botcore import BLCKScopezBot
from core.logger import logger, setup_logger
import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import sys

bot: commands.Bot = BLCKScopezBot()
bot_thread = None
bot_loop = None

def load_cogs(bot: commands.Bot):
    #print("Initialize Cogs...\n")
    counter = 0
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog = f"cogs.{filename[:-3]}"
            # if cog =="cogs.rulez_cog":
            #     continue
            counter += 1
            #print(f"{counter}) Cog successfully loaded: {cog}")
            bot.load_extension(cog)
    print(f"\n{counter}s Cogs successfully loaded!")

def run_bot():
    global bot_loop
    load_cogs(bot)
    bot_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(bot_loop)
    try:
        bot_loop.run_until_complete(bot.start(DISCORD_TOKEN))
    except Exception as e:
        print(f"Bot stopped, error:\n{e}")

def update_repo(output_box, gui_instance):
    output_box.insert(tk.END, "Updating repository...\n")
    output_box.see(tk.END)
    
    bot_was_running = bot_thread is not None and bot_thread.is_alive()
    
    if bot_was_running:
        output_box.insert(tk.END, "Stopping bot for update...\n")
        output_box.see(tk.END)
        stop_bot_thread(output_box)
    
    try:
        process = subprocess.Popen(
            ["git", "pull"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        updated = False
        for line in process.stdout:
            output_box.insert(tk.END, line)
            output_box.see(tk.END)
            if "Updating" in line or "changed" in line:
                updated = True
        process.wait()
        
        if updated:
            output_box.insert(tk.END, "Repository updated successfully. Restarting GUI...\n")
            output_box.see(tk.END)
            # Neu starten
            gui_instance.after(1000, lambda: restart_gui())
        else:
            output_box.insert(tk.END, "No updates found.\n")
            output_box.see(tk.END)

    except Exception as e:
        output_box.insert(tk.END, f"Error updating repository: {e}\n")
        output_box.see(tk.END)

def restart_gui():
    """Ends GUI und start the script again."""
    python = sys.executable
    logger.warning(f"Bot restart BotGUI.")

    os.execl(python, python, *sys.argv)

def clear_logs(outputbox):
    log_dir = "./logs"
    if not os.path.exists(log_dir):
        outputbox.insert(tk.END, "Log directory didnt exist!\n")
        outputbox.see(tk.END)
        return
    try:
        # close all filehandler
        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                logger.removeHandler(handler)
                
        files = os.listdir(log_dir)
        deleted_files = 0
        for file in files:
            file_path = os.path.join(log_dir, file)
            if os.path.isfile(file_path):
               os.remove(file_path)
               deleted_files += 1
        outputbox.insert(tk.END, f"{deleted_files} Log-Files deleted!\n")
        outputbox.see(tk.END)
        
        # start new loggers
        setup_logger()
        outputbox.insert(tk.END, "New logger initialized.\n")
        outputbox.see(tk.END)
        
    except Exception as e:
        outputbox.insert(tk.END, f"Error delete logfiles: {e}\n")
        outputbox.see(tk.END)

def start_bot_thread(output_box=None):
    global bot_thread
    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        if output_box:
            output_box.insert(tk.END, "Bot gestartet!\n")
            output_box.see(tk.END)
        else:
            print("Bot gestartet!")
    else:
        if output_box:
            output_box.insert(tk.END, "Bot läuft bereits!\n")
            output_box.see(tk.END)
        else:
            print("Bot läuft bereits!")

def stop_bot_thread(output_box=None):
    global bot_loop
    if bot_loop is not None:
        asyncio.run_coroutine_threadsafe(bot.close(), bot_loop)
        if output_box:
            #output_box.insert(tk.END, "Bot wird gestoppt...\n")
            output_box.see(tk.END)
        else:
            pass
# ---------------- GUI ----------------
class BotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bot_start_time =None 
        self.title("BLCKScopez Discord Bot Launcher")
        self.geometry("500x600")
        self.configure(bg="#1e1e1e")

        # Header
        header = tk.Label(
            self,
            text="BLCKScopez Discord Bot Launcher",
            font=("Segoe UI", 16, "bold"),
            fg="#ffffff",
            bg="#1e1e1e"
        )
        header.pack(pady=15)

        # Status Frame (Status + Laufzeit)
        status_frame = tk.Frame(self, bg="#1e1e1e")
        status_frame.pack(pady=5)

        self.status_label = tk.Label(
            status_frame,
            text="Bot Status: Stopped",
            font=("Segoe UI", 12, "bold"),
            fg="#ff5555",
            bg="#1e1e1e"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.uptime_label = tk.Label(
            status_frame,
            text="Uptime: 00:00:00",
            font=("Segoe UI", 12, "bold"),
            fg="#dcdcdc",
            bg="#1e1e1e"
        )
        self.uptime_label.pack(side=tk.LEFT, padx=10)

        # Output Box
        self.log_area = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#2a2a2a",
            fg="#dcdcdc",
            insertbackground="white",
            borderwidth=0
        )
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Buttons Frame
        frame = tk.Frame(self, bg="#1e1e1e")
        frame.pack(pady=5)

        btn_style = {
            "bg": "#3c3c3c",
            "fg": "#ffffff",
            "activebackground": "#5a5a5a",
            "activeforeground": "#ffffff",
            "width": 14,
            "height": 2,
            "borderwidth": 0
        }

        self.start_button = tk.Button(
            frame,
            text="Bot Starten",
            command=lambda: self.start_bot(),
            **btn_style
        )
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(
            frame,
            text="Bot Stoppen",
            command=lambda: self.stop_bot(),
            **btn_style
        )
        self.stop_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(
            frame,
            text="Git Pull",
            command=lambda: update_repo(self.log_area, self),
            **btn_style
        )
        self.update_button.grid(row=0, column=2, padx=10)

        self.clear_log_button = tk.Button(
            frame,
            text="Clear Logs",
            command= lambda: clear_logs(self.log_area),
            **btn_style
        )
        self.clear_log_button.grid(row=0, column=3, padx=10)

        # Footer
        footer = tk.Label(
            self,
            text="© 2025 BLCKScopez – Bot Launcher v1.0",
            font=("Segoe UI", 9),
            fg="#808080",
            bg="#1e1e1e"
        )
        footer.pack(side=tk.BOTTOM, pady=10)

        # Redirect print to log_area
        self._stdout = self.log_area
        self._orig_stdout = sys.stdout
        sys.stdout = self

        # Start loop to update uptime every second
        self.update_uptime_loop()
        logger.info(f"Bot GUI startet!")

        
    # ---------- Bot Control Methods ----------
    def start_bot(self):
        start_bot_thread(self.log_area)
        self.bot_start_time = time.time()
        self.update_status()

    def stop_bot(self):
        stop_bot_thread(self.log_area)
        self.bot_start_time = None
        self.update_status()

    def update_status(self):
        global bot_thread
        if bot_thread is not None and bot_thread.is_alive():
            self.status_label.config(text="Bot Status: Running", fg="#55ff55")  # grün
        else:
            self.status_label.config(text="Bot Status: Stopped", fg="#ff5555")  # rot
            self.bot_start_time = None  # Reset uptime
            
    # ---------- Print Redirect ----------
    def write(self, message):
        self._stdout.insert(tk.END, message)
        self._stdout.see(tk.END)
        self.update_status() 
        
    def update_uptime_loop(self):
        if self.bot_start_time:
            elapsed = int(time.time() - self.bot_start_time)
            hrs, rem = divmod(elapsed, 3600)
            mins, secs = divmod(rem, 60)
            self.uptime_label.config(text=f"Uptime: {hrs:02}:{mins:02}:{secs:02}", fg="#55ff55")
        else:
            self.uptime_label.config(text="Uptime: 00:00:00", fg="#ff5555")
        self.after(1000, self.update_uptime_loop) 

    def flush(self):
        pass


def main():
    gui = BotGUI()
    gui.mainloop()
    #bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occured:\n{e}")
        logger.warning(f"Botlost connection or was stopped!\nError: {e}")
    finally:
        sys.exit()
