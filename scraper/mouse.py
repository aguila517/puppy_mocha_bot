import pyautogui
import random
import time

def click(button):
    pyautogui.mouseDown(button=button)
    pyautogui.mouseUp(button=button)

def move_to(x,y):
    pyautogui.moveTo(
                x=x, 
                y=y,
                duration=1
            )
    time.sleep(1)

def wiggle():
    max_wiggles = random.randint(2, 4)
    for _ in range(1, max_wiggles):
        coords = get_random_coords()
        move_to(coords[0], coords[1])
        time.sleep(1)
    

def get_random_coords():
    screen = pyautogui.size()
    width = screen[0]
    height = screen[1]
    
    return [
        random.randint(100, width - 200),
        random.randint(100, height - 200)
    ]