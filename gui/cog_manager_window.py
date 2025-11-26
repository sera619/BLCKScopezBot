import os
import tkinter as tk
from tkinter import messagebox

class CogManagerWindow(tk.Toplevel):
    def __init__(self, master, bot, refresh_callback = None):
        super().__init__(master)
        self.bot = bot
        self.refresh_callback = refresh_callback
        
        self.title("Cog Manager")
        self.geometry("450x600")
        self.configure(bg="#1e1e1e")

        title = tk.Label(
            self,
            text="Loaded Cogs",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg="#1e1e1e",
            pady=10
        )
        title.pack()

        self.cog_frame = tk.Frame(self, bg="#1e1e1e")
        self.cog_frame.pack(fill=tk.BOTH, expand=True)

        self.update_cog_list()

    def update_cog_list(self):
        # erst alles löschen
        for widget in self.cog_frame.winfo_children():
            widget.destroy()

        row = 0
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                cog_name = filename[:-3]
                full_cog = f"cogs.{cog_name}"

                # Status check
                is_loaded = full_cog in self.bot.extensions

                status_color = "#55ff55" if is_loaded else "#ff5555"
                status_text = "Loaded" if is_loaded else "Unloaded"

                tk.Label(
                    self.cog_frame,
                    text=cog_name,
                    fg="#ffffff",
                    bg="#1e1e1e",
                    font=("Segoe UI", 11)
                ).grid(row=row, column=0, sticky="w", padx=10, pady=5)

                tk.Label(
                    self.cog_frame,
                    text=status_text,
                    fg=status_color,
                    bg="#1e1e1e",
                    font=("Segoe UI", 11)
                ).grid(row=row, column=1, padx=10)

                # Load / Unload Button
                if is_loaded:
                    tk.Button(
                        self.cog_frame,
                        text="Unload",
                        bg="#3c3c3c",
                        fg="#ffffff",
                        width=10,
                        command=lambda c=full_cog: self.unload_cog(c)
                    ).grid(row=row, column=2, padx=5)
                else:
                    tk.Button(
                        self.cog_frame,
                        text="Load",
                        bg="#3c3c3c",
                        fg="#ffffff",
                        width=10,
                        command=lambda c=full_cog: self.load_cog(c)
                    ).grid(row=row, column=2, padx=5)

                # Reload Button
                tk.Button(
                    self.cog_frame,
                    text="Reload",
                    bg="#3c3c3c",
                    fg="#ffffff",
                    width=10,
                    command=lambda c=full_cog: self.reload_cog(c)
                ).grid(row=row, column=3, padx=5)

                row += 1

    def load_cog(self, cog):
        try:
            self.bot.load_extension(cog)
            messagebox.showinfo("Cog Loaded", f"{cog} was loaded!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.update_cog_list()

    def unload_cog(self, cog):
        try:
            self.bot.unload_extension(cog)
            messagebox.showinfo("Cog Unloaded", f"{cog} was unloaded!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.update_cog_list()

    def reload_cog(self, cog):
        try:
            self.bot.reload_extension(cog)
            messagebox.showinfo("Cog Reloaded", f"{cog} was reloaded!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.update_cog_list()      