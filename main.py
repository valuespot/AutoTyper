import pyperclip
import time
import pyautogui
from pynput import keyboard, mouse
from AppKit import NSWorkspace
from threading import Thread

# this set is used to track pressed keys
current_keys = set()
stop_typing = False

def type_slowly(text, delay=0.02, english_only=True):
    """
    Function to type text slowly with a given delay between characters.
    """
    global stop_typing
    stop_typing = False
    time.sleep(0.5)
    # iterate every character
    if english_only:
        pyautogui.PAUSE = 0
        for char in text:
            time.sleep(delay)
            if stop_typing:
                print("Focus changed, cancelling typing")
                break
            pyautogui.write(char)
    else:
        pyautogui.PAUSE = delay # don't make PAUSE too small
        for char in text:
            if stop_typing:
                print("Focus changed, cancelling typing")
                break
            pyperclip.copy(char)
            pyautogui.hotkey('command', 'v') 
        # restore content in clipboard
        pyperclip.copy(text)

def on_press(key):
    global current_keys, stop_typing
    try:
        stop_typing = True
        current_keys.add(key)
        # check if use pressed Cmd + C
        if keyboard.Key.cmd in current_keys and keyboard.KeyCode.from_char('c') in current_keys:
            print("Cmd + C was pressed")
        # check if use pressed Ctrl + C
        if keyboard.Key.ctrl in current_keys and keyboard.KeyCode.from_char('v') in current_keys:
            print("Ctrl + V was pressed")
    except AttributeError:
        pass

def on_release(key):
    global current_keys, stop_typing
    try:
        # remove released key from current_keys
        current_keys.remove(key)
        # check if released keys are Ctrl + V
        if keyboard.Key.ctrl in current_keys and key == keyboard.KeyCode.from_char('v'):
            clipboard_content = pyperclip.paste()
            print(f"Ctrl + V was released, Clipboard content: {clipboard_content}")
            type_slowly(clipboard_content)
    except KeyError:
        pass

def on_click(x, y, button, pressed):
    global stop_typing
    if pressed:
        stop_typing = True
        print("Mouse click detected, stop typing")

def on_move(x, y):
    global stop_typing
    stop_typing = True 
    print("Mouse move detected, stop typing")

# listen to keyboard
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

# listen to mouse
mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)
mouse_listener.start()

# run
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    keyboard_listener.stop()
    mouse_listener.stop()
