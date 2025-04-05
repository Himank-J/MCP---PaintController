import pyautogui, time
from pynput import mouse

print("Press Ctrl-C to quit.")

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse CLICKED at position: x={x}, y={y}")

# Create a listener for mouse clicks
listener = mouse.Listener(on_click=on_click)
listener.start()

try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: x={x}, y={y}")
        time.sleep(1)
except KeyboardInterrupt:
    listener.stop()
    print('\nDone.')