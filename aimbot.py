import win32api
import win32gui
import win32con
import mss
import pydirectinput
from PIL import Image
import ctypes
from playsound import playsound
from time import sleep as time_sleep


sct = mss.mss()
fov = 15
next_to = 13
sens = 2.5
if not fov:
    fov = int(input('FOV: '))
if not next_to:
    next_to = int(input('Next To: '))
if not sens:
    sens = float(input('Sens: '))

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)

monitor = {
    'left': int(width / 2 - fov / 2),
    'top': int(height / 2 - fov / 2),
    'width': int(fov),
    'height': int(fov)
}
colors = [
    (140, 97, 90),
    (128, 82, 52),
    (140, 68, 35),
    (52, 46, 54),
    (52, 52, 40),
    (47, 55, 44)
]
nt_del = int(next_to / 2)
fov_del = int(fov / 2)
running = True
while True:
    in_game = win32gui.GetWindowText(win32gui.GetForegroundWindow()) == 'Counter-Strike: Global Offensive'
    if in_game:
        if win32api.GetAsyncKeyState(win32con.VK_NUMPAD1):
            if running:
                running = False
                playsound('off.wav')
            else:
                running = True
                playsound('on.wav')
            time_sleep(1)
        if running:
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            for i in range(monitor['width']):
                for j in range(monitor['height']):
                    r, g, b = img.getpixel((i, j))[:3]
                    breaked = False
                    for color in colors:
                        if color[0] - nt_del < r < color[0] + nt_del and color[1] - nt_del < g < color[1] + nt_del\
                                and color[2] - nt_del < b < color[2] + nt_del:
                            ctypes.windll.user32.mouse_event(
                                ctypes.c_uint(0x0001),
                                ctypes.c_uint(int((i - fov_del) / sens)),
                                ctypes.c_uint(int((j - fov_del) / sens)),
                                ctypes.c_uint(0),
                                ctypes.c_uint(0)
                            )
                            breaked = True
                            break
                    if breaked:
                        break
