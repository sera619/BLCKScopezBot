from cx_Freeze import Executable, setup
from core.config import BOT_VERSION
import sys
import os

include_files =[
    ("core", "core"),
    ("cogs", "cogs"),
    ("data", "data"),
    ("views", "views"),
    ("gui", "gui"),
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
    
target = Executable(
    script="bot.py",
    base="Win32GUI",
    target_name="BLCKScopezDiscordBot",
    copyright='Copyright (c) 2025, S3R43o3',
    shortcut_name='BLCKScopezDiscordBot'
)


setup(
    name = "BLCKScopezDiscordBot",
    version = f"{BOT_VERSION}",
    author="S3R43o3",
    description = "Discord Bot for BLCKScopez",
    options = {"build_exe": build_exe_options},
    executables = [target]
)