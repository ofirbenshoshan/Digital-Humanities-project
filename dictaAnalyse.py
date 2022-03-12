import pywinauto
from pywinauto.application import Application
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import webbrowser
import pyperclip
import sys

#C:\ti\lunas2\python\Scripts\python.exe test.py

url = 'https://morph-analysis.dicta.org.il/'

def morpo_analyse(sentence):
	#set chromodriver.exe path
	driver = webdriver.Chrome(executable_path="C:\\Users\\a0491561\\Desktop\\chromedriver.exe")
	driver.implicitly_wait(0.5)
	#launch URL
	driver.get("https://morph-analysis.dicta.org.il/")
	time.sleep(6)
	pyautogui.press('tab',5)
	pyperclip.copy(sentence)
	pyautogui.hotkey("ctrl", "v")
	time.sleep(2)
	pyautogui.press('tab',2)
	pyautogui.press('enter')
	time.sleep(2)
	pyautogui.press('tab',5)
	time.sleep(2)
	pyautogui.press('enter')
	time.sleep(2)
	pyautogui.press('enter')
	time.sleep(2)
	pyautogui.press('down',3)
	time.sleep(2)
	pyautogui.press('enter')
	time.sleep(2)
	for i in range(0,8):
		pyautogui.press('tab')
		time.sleep(0.2)
	pyautogui.press('enter')
	time.sleep(3)

def main(args):
	s = ''
	for i in range(1, len(args)):
		s += args[i] + " "				
	morpo_analyse(s)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	sentence = sys.argv
	main(sentence)