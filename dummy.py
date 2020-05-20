import numpy as np
import cv2
from mss import mss
from PIL import Image
import keyboard
import pyautogui

from scipy.spatial.distance import cdist

dir = '/Users/gakiladh/Documents/rebirth/dino_dino/'
screen_shot = cv2.cvtColor(np.array(cv2.imread(dir+'dino0.jpg')), cv2.COLOR_BGR2GRAY)
screen_shot = cv2.cvtColor(np.array(cv2.imread(dir+'templates/scrshts/dino_0.jpg')), cv2.COLOR_BGR2GRAY)

#tempD = cv2.cvtColor(np.array(cv2.imread(dir+'templates/D.jpg')), cv2.COLOR_BGR2GRAY)
#tempB = cv2.cvtColor(np.array(cv2.imread(dir+'templates/B.jpg')), cv2.COLOR_BGR2GRAY)
#tempCS1 = cv2.cvtColor(np.array(cv2.imread(dir+'templates/CS1.jpg')), cv2.COLOR_BGR2GRAY)
#tempCS2 = cv2.cvtColor(np.array(cv2.imread(dir+'templates/CS2.jpg')), cv2.COLOR_BGR2GRAY)
#tempCS3 = cv2.cvtColor(np.array(cv2.imread(dir+'templates/CS3.jpg')), cv2.COLOR_BGR2GRAY)
#tempCB1 = cv2.cvtColor(np.array(cv2.imread(dir+'templates/CB1.jpg')), cv2.COLOR_BGR2GRAY)
#tempCB2 = cv2.cvtColor(np.array(cv2.imread(dir+'templates/CB2.jpg')), cv2.COLOR_BGR2GRAY)
#tempCB3 = cv2.cvtColor(np.array(cv2.imread(dir+'templates/CB3.jpg')), cv2.COLOR_BGR2GRAY)


screen = np.copy(screen_shot)



'''
for i in range(len(screen)):
	if i % 50==0:
		screen[i,:] = 85
for i in range(len(screen[0])):
	if i % 50==0:
		screen[:,i] = 85
'''


#cv2.imwrite(dir+'templates/dino_4_.jpg',cv2.cvtColor(np.array(cv2.imread(dir+'templates/dino_4.jpg')), cv2.COLOR_BGR2GRAY)[100:200+82,:])

#template = tempCS1
#screen[200:200+ template.shape[0],150:150+ template.shape[1]] = template



#print(tempD.shape)
#print(tempCB3.shape)

obs_screen = np.copy(screen[200:200+82,:])

'''
for i in range(len(obs_screen[0])-template.shape[1]):
	A = obs_screen[:,i:i+template.shape[1]]
	A[A < 100] = 1
	A[A > 100] = 0
	B = template
	B[B < 100] = 1
	B[B > 100] = 0
	d = np.sum((A -B)**2)
	print(i,d)
	if d <50:
		screen[:,i+template.shape[1]] = 85
'''






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

for i in range(len(mask_arr)):
	print(i,mask_arr[i])

print(mask_arr)
print(mask_arr_diff)


for i in range(len(mask_arr_diff)):
	if mask_arr_diff[i]>50:
		print(i)
		if mask_arr[i] != 0:
			obs_screen[:,mask_arr[i]] = 85
		if i != len(mask_arr_diff)-1:
			obs_screen[:,mask_arr[i+1]] = 85


cv2.imshow('screen', obs_screen)


print(np.sum(screen_shot <85))

while True:
	keyPress = cv2.waitKey(1)
	keyChar = chr(keyPress & 0xFF)
	if keyChar == 'q':
		break