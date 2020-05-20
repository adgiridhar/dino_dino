import numpy as np
import cv2
from mss import mss
from PIL import Image
import keyboard
import pyautogui
import time

import os
cmdSpace = """
osascript -e 'tell application "System Events" to keystroke " "' 
"""



#####----PARAMETERS----####
font = cv2.FONT_HERSHEY_SIMPLEX

screenTop = 200
screenLeft = 70
screenW = 600
screenH = 150


bounding_box = {'top': screenTop, 'left': screenLeft, 'width': screenW, 'height': screenH}
	
offsetX = 0
offsetY = 0

sct = mss()
screen_shot = None
mouseX = 0
mouseY = 0

fNum = 0

cursorFlag = False

dir = '/Users/gakiladh/Documents/rebirth/dino_dino/'

def screenShotOperations():
	global mouseX, mouseY, offsetX, offsetY, screen_shot
	time.sleep(5)
	prev_obs_arr = []
	while True:
		
		screen_shot = cv2.cvtColor(np.array(sct.grab(bounding_box)), cv2.COLOR_BGR2GRAY)
		obs_screen = np.copy(screen_shot[200:200+82,:])
		#print("screen shot:::", screen_shot_)

		mouseX, mouseY = pyautogui.position()

		if cursorFlag:
			cv2.putText(screen_shot,str(mouseX-offsetX)+','+str(mouseY-offsetY),(mouseX-offsetX,mouseY-offsetY), font, 2,(0,0,255),2,cv2.LINE_AA)
			cv2.line(screen_shot,(0,(mouseY-offsetY)),(screenW*2, (mouseY-offsetY)),(255,0,0),5)
			cv2.line(screen_shot,((mouseX-offsetX),0),((mouseX-offsetX), screenH*2),(255,0,0),5)


		#imScreen = cv2.resize(np.array(screen_shot), (600, 150))
		#screen_shot_[200:,:] = screen_shot
		#cv2.imshow('screen', np.array(screen_shot_))

		mask_arr = [0]

		dino_bed = 56
		dino_end = 136

		mask_prev = np.copy(obs_screen[:,dino_end+1])
		mask_prev[mask_prev < 100] = 1
		mask_prev[mask_prev > 100] = 0
		for i in range(dino_end+1,dino_end+1+len(obs_screen[0,dino_end+1:])):
			mask_i = np.copy(obs_screen[:,i])
			mask_i[mask_i < 100] = 1
			mask_i[mask_i > 100] = 0
			th = np.sum((mask_i - mask_prev)**2)
			#print(i, th)
			mask_prev = np.copy(mask_i)
			if th>10:
				mask_arr.append(i)
				#obs_screen[:,i] = 85
		mask_arr.append(1200)

		mask_arr_diff = np.diff(mask_arr)

		#for i in range(len(mask_arr)):
		#	print(i,mask_arr[i])

		#print(mask_arr)
		#print(mask_arr_diff)

		obs_arr = []
		for i in range(len(mask_arr_diff)):
			if mask_arr_diff[i]>50:
				#print(i)
				if mask_arr[i] != 0:
					obs_arr.append(mask_arr[i])
					screen_shot[200:200+82,mask_arr[i]-2:mask_arr[i]] = 85
				if i != len(mask_arr_diff)-1:
					obs_arr.append(mask_arr[i+1])
					screen_shot[200:200+82,mask_arr[i+1]:mask_arr[i+1]+2] = 85
		if len(obs_arr) > 0:
			if len(obs_arr) % 2 != 0 and obs_arr[-1]>1000:
				obs_arr.append(1200)
		
		if len(prev_obs_arr)>1 and len(obs_arr)>1:	
			print(prev_obs_arr[0]-obs_arr[0], obs_arr)
		if len(obs_arr) > 0:
			if len(obs_arr)>2:
				if obs_arr[2] - obs_arr[1] < 350 and obs_arr[0] < 450:
					print("\tJump2")
					for i in range(10):
						os.system(cmdSpace)
			if obs_arr[0] < 400:
				print("Jump1")
				os.system(cmdSpace)
				#keyboard.press_and_release('space')
				#keyboard.press_and_release('s')
		
		prev_obs_arr = obs_arr
		#cv2.imshow('cactus_obs', screen_shot)
		
		if keyActions()=='q':
			break


def keyActions():
	global mouseX, mouseY, offsetX, offsetY, screen_shot, fNum, cursorFlag
	keyPress = cv2.waitKey(1)
	keyChar = chr(keyPress & 0xFF)
	if keyChar == 'a':
		offsetX = mouseX
		offsetY = mouseY
	if keyChar == 's':
		print("X: ", mouseX-offsetX, " Y: ", mouseY-offsetY)
	if keyChar == 'q':
		cv2.destroyAllWindows()
		return 'q'
	if keyChar == 'z':
		cv2.imwrite(dir+'dino_sep.jpg', screen_shot[206:298,54:141,:])
		print("saved")
	if keyChar == 'x':
		cv2.imwrite(dir+'dino'+str(fNum)+'.jpg', screen_shot)
		print('dino'+str(fNum)+'.jpg' + "saved...")
		fNum+=1
	if keyChar == 'c':
		cursorFlag = not cursorFlag



def main():
	screenShotOperations()


if __name__ == '__main__':
    main()

