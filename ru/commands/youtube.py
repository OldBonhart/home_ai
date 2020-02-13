import pyautogui
import time


class YouTube:
    
    def later_watch(self):
        
        pyautogui.click(60,10, duration=0.15)
        time.sleep(1)
        pyautogui.click(160, 120, duration=0.15)
        time.sleep(1)
        pyautogui.write("youtube")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(4)
        pyautogui.click(210, 337, duration=0.25)
        time.sleep(6)
        pyautogui.click(65, 175, duration=0.25)
        time.sleep(2)
        pyautogui.click(65, 450, duration=0.25)
        time.sleep(2)
        pyautogui.click(600, 280, duration=0.25)
        time.sleep(6)
        pyautogui.click(1180,860, duration=0.25)

    def pause(self):
        pyautogui.press("space")
    
    def exit(self):
        pyautogui.press("esc")
        time.sleep(3)
        pyautogui.click(1660, 55, duration=0.25)
        
        
#pyautogui.moveTo(1660, 55)