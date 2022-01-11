import cv2
import time
import gestureControl as gs

print("\n--------WELCOME---------\n")
print("This is a hand tracking interface with gesture control")
print("With this program you can:")
print("--------------------------Control the volume[+/-]")
showFps = str(input("Show fps[y/n]: "))
background = str(input("Show the background[y/n]: "))
body = str(input("Show the whole body or only the hands.\n(May affect performance)[y/n]: "))
showVol = str(input("Show the volume level[y/n]: "))
isControllable = str(input("Control the volume[y/n]: "))

if body.lower() == 'y':
    body = True
else:
    body = False


gs.run(showFps, background, body, showVol, isControllable)