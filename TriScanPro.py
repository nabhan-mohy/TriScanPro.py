import subprocess
import os
import shutil
from colorama import init, Fore, Back, Style
import pyfiglet  # For ASCII art

# Initialize Colorama
init(autoreset=True)

def print_header():
    """Print the header with the tool name in ASCII art."""
    ascii_banner = pyfiglet.figlet_format("TriScanPro", font="slant")  # You can use different fonts here
    print(Fore.YELLOW + Style.BRIGHT + ascii_banner)
    print(Fore.YELLOW + Style.BRIGHT + "=========================================")
    print(Fore.YELLOW + Style.BRIGHT + " A Powerful Multi-Tool Scanner for Web & Network ")
    print(Fore.YELLOW + Style.BRIGHT + "=========================================")

def run_nmap(target, mode):
    """Run Nmap scan with the selected mode."""
    print(f"Running Nmap on {target} in {mode} mode...")
    nmap_command = {
        "quick": ["nmap", "-T4", "-F", target],
        "fast": ["nmap", "-T4", "-A", "-v", target],
        "slow": ["nmap", "-T1", "-p-", "-A", "-v", target]
    }
    subprocess.run(nmap_command.get(mode, []))

def run_gobuster(target, mode, wordlist):
    """Run Gobuster directory scan with the selected mode."""
    print(f"Running Gobuster on {target} in {mode} mode...")
    gobuster_command = {
        "quick": ["gobuster", "dir", "-u", target, "-w", wordlist, "-t", "10", "-b", "403"],
        "fast": ["gobuster", "dir", "-u", target, "-w", wordlist, "-t", "20", "-b", "403"],
        "slow": ["gobuster", "dir", "-u", target, "-w", wordlist, "-t", "5", "-b", "403"]
    }
    subprocess.run(gobuster_command.get(mode, []))

def run_nikto(target, mode):
    """Run Nikto web scanner with the selected mode."""
    print(f"Running Nikto on {target} in {mode} mode...")
    nikto_command = {
        "quick": ["nikto", "-h", target, "-Tuning", "1"],
        "fast": ["nikto", "-h", target, "-Tuning", "x"],
        "slow": ["nikto", "-h", target]
    }
    subprocess.run(nikto_command.get(mode, []))

def get_tool_choice():
    """Prompt user to select a tool to run."""
    print(Fore.YELLOW + Style.BRIGHT + "\nSelect a tool to use: ")
    print(Fore.YELLOW + Style.BRIGHT + "[1] Nmap")
    print(Fore.YELLOW + Style.BRIGHT + "[2] Gobuster")
    print(Fore.YELLOW + Style.BRIGHT + "[3] Nikto")
    print(Fore.YELLOW + Style.BRIGHT + "[4] All tools")

    choice = input(Fore.YELLOW + "Enter your choice (1-4): ").strip()
    if choice == "1":
        return "nmap"
    elif choice == "2":
        return "gobuster"
    elif choice == "3":
        return "nikto"
    elif choice == "4":
        return "all"
    else:
        print(Fore.RED + "Invalid choice. Please enter a number between 1 and 4.")
        return get_tool_choice()

def get_mode_choice():
    """Prompt user to select a scan mode."""
    print(Fore.YELLOW + Style.BRIGHT + "\nSelect a scan mode: ")
    print(Fore.YELLOW + Style.BRIGHT + "[1] Quick")
    print(Fore.YELLOW + Style.BRIGHT + "[2] Fast")
    print(Fore.YELLOW + Style.BRIGHT + "[3] Slow")

    choice = input(Fore.YELLOW + "Enter your choice (1-3): ").strip()
    if choice == "1":
        return "quick"
    elif choice == "2":
        return "fast"
    elif choice == "3":
        return "slow"
    else:
        print(Fore.RED + "Invalid choice. Please enter a number between 1 and 3.")
        return get_mode_choice()

def get_wordlist():
    """Prompt user for a wordlist path."""
    wordlist = input("Enter the path to the wordlist you want to use for Gobuster: ").strip()
    if os.path.isfile(wordlist):
        return wordlist
    else:
        print(Fore.RED + "Invalid wordlist path. Please try again.")
        return get_wordlist()

def main():
    # Ensure necessary tools are installed
    if not shutil.which("nmap") or not shutil.which("gobuster") or not shutil.which("nikto"):
        print(Fore.RED + "Error: Ensure nmap, gobuster, and nikto are installed and available in PATH.")
        exit(1)

    # Print header
    print_header()

    # Get user input
    tool = get_tool_choice()
    target = input(Fore.YELLOW + "Enter the target (e.g., https://example.com or an IP address): ").strip()
    mode = get_mode_choice()

    # Run the selected tool(s)
    if tool == "nmap":
        run_nmap(target, mode)
    elif tool == "gobuster":
        wordlist = get_wordlist()
        run_gobuster(target, mode, wordlist)
    elif tool == "nikto":
        run_nikto(target, mode)
    elif tool == "all":
        run_nmap(target, mode)
        wordlist = get_wordlist()
        run_gobuster(target, mode, wordlist)
        run_nikto(target, mode)

if __name__ == "__main__":
    main()
