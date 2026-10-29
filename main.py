from colorama import Fore
from tqdm import tqdm
import time
import os
import pinglink
import pinguserip
import phoneinfo
import username
import webscanner

MENU_FILE = "menu.txt"

BANNER = r"""
  .--.--.          ,-.                   ,--,      ,--,
 /  /    '.    ,--/ /|                 ,--.'|    ,--.'|
|  :  /`. /  ,--. :/ |           ,--,  |  | :    |  | :
;  |  |--`   :  : ' /          ,'_ /|  :  : '    :  : '
|  :  ;_     |  '  /      .--. |  | :  |  ' |    |  ' |
 \  \    `.  '  |  :    ,'_ /| :  . |  '  | |    '  | |
  `----.   \ |  |   \   |  ' | |  . .  |  | :    |  | :
        \  \ | '  : |. \   | | ' |  | |  '  : |  '  : |__
 /  /`--'  / |  | ' \ \ :  | : ;  ; |  |  | '.'| |  | '.'|
'--'.     /  '  : |--'  '  :  `--'   \ ;  :    ; ;  :    ;
  `--'---'   ;  |,'     :  ,      .-./ |  ,   /  |  ,   /
             '--'        ------'      ----'    ----'
"""


option_next = "[N] Next"
option_quit = "[Q] Quit"
option_info = "[I] Info"
option_back = "[B] Back"

MENU_1 = f""" ┌─ {option_info}                                                                                               {option_next} ─┐
 ├─ {option_quit} ┌────────────┐                        ┌───────┐                           ┌───────────┐            │
 └─┬─────────┤ Pentesting ├─────────┬──────────────┤ Osint ├──────────────┬────────────┤ Utilities ├────────────┴─
   │         └────────────┘         │              └───────┘              │            └───────────┘
   ├─ 1 Target Link                 ├─ 7 Username Tracker                 ├─
   ├─ 2 Target IP                   ├─ 8 Phone Info                       ├─
   ├─ 3 Web Scanner                 ├─                                    ├─
   ├─ 4                             ├─                                    ├─
   ├─ 5                             ├─                                    ├─
   └─ 6                             ├─                                    ├─
                                    ├─                                    └─
                                    ├─
                                    ├─
                                    └─

"""

MENU_2 = f""" ┌─ {option_info}                                                                                                {option_next} ─┐
 ├─ {option_quit}  ┌───────────────┐                         ┌──────┐                              ┌────────┐    {option_back} ─┤
─┴─┬──────────┤               ├──────────┬──────────────┤      ├───────────────┬──────────────┤        ├──────────────┴─
   │          └───────────────┘          │              └──────┘               │              └────────┘
   └─                                    ├─                                    ├─
                                         ├─                                    ├─
                                         ├─                                    ├─
                                         └─                                    └─
"""

def load_menu():
    if not os.path.exists(MENU_FILE):
        return "1"
    return open(MENU_FILE).read().strip()

def save_menu(n):
    open(MENU_FILE, "w").write(n)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def menu_tool_info():
    print("""
[+] Name Tool     : SKULL
[+] Version       : 1.13
[+] Coding        : Python 3
[+] Language      : EN
[+] Creator       : Mriakulz
[+] Platform      : Windows 10/11 & Linux
    """)
    input(" [!] | Press to continue -> ")
    clear_screen()


def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        menu = load_menu()

        print(Fore.GREEN + BANNER)

        print(MENU_1 if menu == "1" else MENU_2)

        choice = input("> ").lower()

        if choice == "i" or choice == "I":
            menu_tool_info()
        if choice == "1":
            pinglink.pinglink()
        if choice == "2":
            pinguserip.pinguserip()
        if choice == "3":
            webscanner.webscanner()
        if choice == "7":
            username.username_tracker()
        if choice == "8":
            phoneinfo.phoneinfomenu()

        if choice == "n" or choice == "N":
            save_menu("2")
        elif choice == "b" or choice == "B":
            save_menu("1")
        elif choice == "q" or choice == "Q":
            print("Completion of work...")
            for _ in tqdm(range(100), desc="Closing the program"):
                time.sleep(0.02)
                save_menu("1")
            break
        else:
            clear_screen()
            print(Fore.RED + "Incorrect selection. Please try again.")

if __name__ == "__main__":
    main()
