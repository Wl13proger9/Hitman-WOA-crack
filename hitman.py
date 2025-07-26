#pyinstaller hitman.py --onefile --noconfirm --clean --noconsole --upx-dir "C:\upx" --exclude-module test --exclude-module tkinter
#вместо "C:\upx" ставь свой путь если есть

import subprocess
import os
import time
import sys
import ctypes



#[язык]
lang = "eng"
if "-ru" in sys.argv:lang = "ru"
elif "-eng" in sys.argv:lang = "eng"
else:pass



#[переменые]
ab_path = os.getcwd()
peacock_path = os.path.join(ab_path, 'peacock', 'PeacockPatcher.exe')
peacock_cmd_path = os.path.join(ab_path, 'peacock', 'Start Server.cmd')
game_path = os.path.join(ab_path, 'steamclient_loader_x64.exe')



#[Windows флаги для запуска без окна]
DETACHED_PROCESS = 0x00000008
CREATE_NO_WINDOW = 0x08000000



#[запуск патчера]
try:subprocess.Popen([peacock_path], creationflags=DETACHED_PROCESS)
except:
    if lang == "eng":ctypes.windll.user32.MessageBoxW(0, "<PeacockPatcher.exe> not found!", "Error with code: 1", 0x10)
    else: ctypes.windll.user32.MessageBoxW(0, "<PeacockPatcher.exe> не найден!", "Ошибка с кодом: 1", 0x10)



#[запуск сервера]
try:subprocess.Popen(["cmd.exe", "/c", peacock_cmd_path],creationflags=CREATE_NO_WINDOW)
except:
    if lang == "eng":ctypes.windll.user32.MessageBoxW(0, "<Start Server.cmd> not found!", "Error with code: 2", 0x10)
    else: ctypes.windll.user32.MessageBoxW(0, "<Start Server.cmd> не найден!", "Ошибка с кодом: 2", 0x10)



#[ожидание в 0.3 секунды]
time.sleep(0.3)



#[запуск самой игры]
try:subprocess.Popen([game_path], creationflags=DETACHED_PROCESS)
except:
    if lang == "eng":ctypes.windll.user32.MessageBoxW(0, "<steamclient_loader_x64.exe> not found!", "Error with code: 3", 0x10)
    else: ctypes.windll.user32.MessageBoxW(0, "<steamclient_loader_x64.exe> не найден!", "Ошибка с кодом: 3", 0x10)