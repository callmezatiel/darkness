#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path

PACMAN_CONF = Path("/etc/pacman.conf")

BANNER = r"""
\033[91m
██████╗  █████╗ ██████╗ ██╗  ██╗███╗   ██╗███████╗███████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝████╗  ██║██╔════╝██╔════╝██╔════╝
██║  ██║███████║██████╔╝█████╔╝ ██╔██╗ ██║█████╗  ███████╗███████╗
██║  ██║██╔══██║██╔══██╗██╔═██╗ ██║╚██╗██║██╔══╝  ╚════██║╚════██║
██████╔╝██║  ██║██║  ██║██║  ██╗██║ ╚████║███████╗███████║███████║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝
\033[1;m
| BlackArch Tool Manager (Red / Blue / Purple)
"""

# =====================================================
# CATEGORÍAS + SUBCATEGORÍAS (SANITIZADAS)
# =====================================================

CATEGORIES = {
    "Information Gathering": {
        "nmap": "nmap",
        "masscan": "masscan",
        "dnsenum": "dnsenum",
        "dnsrecon": "dnsrecon",
        "theharvester": "theharvester",
        "recon-ng": "recon-ng",
        "amass": "amass",
    },

    "Vulnerability Analysis": {
        "sqlmap": "sqlmap",
        "nikto": "nikto",
        "lynis": "lynis",
        "nuclei": "nuclei",
        "openvas": "openvas",
    },

    "Exploitation Tools": {
        "metasploit": "metasploit",
        "beef": "beef",
        "setoolkit": "set",
        "armitage": "armitage",
    },

    "Web Applications": {
        "burpsuite": "burpsuite",
        "gobuster": "gobuster",
        "wfuzz": "wfuzz",
        "wpscan": "wpscan",
        "zaproxy": "zaproxy",
    },

    "Password Attacks": {
        "hashcat": "hashcat",
        "john": "john",
        "hydra": "hydra",
        "crunch": "crunch",
    },

    "Sniffing & Spoofing": {
        # dnschef ELIMINADO (404 recurrente)
        "bettercap": "bettercap",
        "responder": "responder",
        "ettercap": "ettercap",
        "dsniff": "dsniff",
        "tcpdump": "tcpdump",
    },

    "Forensics Tools": {
        "volatility": "volatility",
        "autopsy": "autopsy",
        "binwalk": "binwalk",
        "foremost": "foremost",
    },

    "Reverse Engineering": {
        "radare2": "radare2",
        "ghidra": "ghidra",
        "jadx": "jadx",
        "apktool": "android-apktool",
    },

    "Wireless Attacks": {
        "aircrack-ng": "aircrack-ng",
        "wifite": "wifite",
        "kismet": "kismet",
        "reaver": "reaver",
    },

    "Maintaining Access": {
        "weevely": "weevely",
        "pwncat": "pwncat",
        "nishang": "nishang",
    },

    "🟣 Kali Purple (Blue + Red)": {
        "zeek": "zeek",
        "suricata": "suricata",
        "sigma": "sigma",
        "velociraptor": "velociraptor",
        "yara": "yara",
        "osquery": "osquery",
    }
}

# =====================================================
# FUNCIONES BASE (ROBUSTAS)
# =====================================================

def require_root():
    if os.geteuid() != 0:
        sys.exit("[!] Run as root")

def run(cmd):
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_package(name, pkg):
    print(f"[+] Installing {name}")
    if not run(["pacman", "-S", "--noconfirm", pkg]):
        print(f"[!] Failed: {name} (skipped)")
        return False
    return True

# =====================================================
# MENÚS
# =====================================================

def main_menu():
    print("""
1) Install tools by category
2) Exit
""")

def category_menu():
    for i, cat in enumerate(CATEGORIES.keys(), 1):
        print(f"{i}) {cat}")
    print("0) Back")

def tool_menu(category):
    tools = CATEGORIES[category]
    print(f"\n[{category}]")
    for i, tool in enumerate(tools.keys(), 1):
        print(f"{i}) {tool}")
    print("a) Install ALL")
    print("0) Back")

# =====================================================
# MAIN
# =====================================================

def main():
    require_root()
    print(BANNER)

    while True:
        main_menu()
        c = input("bt > ").strip()

        if c == "1":
            while True:
                category_menu()
                sel = input("cat > ").strip()
                if sel == "0":
                    break
                try:
                    category = list(CATEGORIES.keys())[int(sel) - 1]
                except:
                    print("[!] Invalid")
                    continue

                while True:
                    tool_menu(category)
                    t = input("tool > ").strip()
                    tools = list(CATEGORIES[category].items())

                    if t == "0":
                        break
                    elif t.lower() == "a":
                        for name, pkg in tools:
                            install_package(name, pkg)
                    else:
                        try:
                            name, pkg = tools[int(t) - 1]
                            install_package(name, pkg)
                        except:
                            print("[!] Invalid")

        elif c == "2":
            print("[*] Exiting")
            break
        else:
            print("[!] Invalid option")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Operator aborted")

