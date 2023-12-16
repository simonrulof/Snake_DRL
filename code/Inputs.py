from pynput import keyboard
import time
import threading

import GlobalVar

class Inputs(threading.Thread):

    def run(self):
        with keyboard.Events() as events:
            for event in events:
                if event.key == keyboard.Key.right and GlobalVar.baseDirection != "right":
                    GlobalVar.direction = "right"
                if event.key == keyboard.Key.left and GlobalVar.baseDirection != "left":
                    GlobalVar.direction = "left"
                if event.key == keyboard.Key.down and GlobalVar.baseDirection != "down":
                    GlobalVar.direction = "down"
                if event.key == keyboard.Key.up and GlobalVar.baseDirection != "up":
                    GlobalVar.direction = "up"
                if event.key == keyboard.Key.esc:
                    GlobalVar.leave = True
                    break