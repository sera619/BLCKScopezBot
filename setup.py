from cx_Freeze import Executable, setup
import sys
import os

include_files =[
    ("core", "core"),
    ("cogs", "cogs"),
    ("data", "data"),
    ("views", "views"),
    ("gui", "gui"),
    (".env", ".env"),
    ("utils.py", "utils.py")
]
include_dirs = [
    "gui",
    "data",
    "cogs",
    "core",
    "views"
]
build_exe_options = {
    "packages": [
        "asyncio",
        "disnake",
        "tkinter",
        "threading",
        "logging",
        "aiohttp",
        "dotenv"
    ],
    "excludes": [],
    "includes": [],
    "include_files": include_files,
    "include_msvcr": True
}

base = None
if sys.platform == "win32":
    base = "Win32gui"

setup(
    name = "BLCKScopezDiscordBot",
    version = "1.0",
    description = "Discord Bot for BLCKScopez",
    options = {"build_exe": build_exe_options},
    executables = [Executable("bot.py", base=base)]
)