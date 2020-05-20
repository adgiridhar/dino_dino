import numpy as np
import cv2
from mss import mss
from PIL import Image
import keyboard
import pyautogui

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
#-------------------------#

def read_templates():
	template = {}
	template['dino'] = cv2.cvtColor(np.array(cv2.imread(dir+'templates/dino.jpg')), cv2.COLOR_BGR2GRAY)
	template['dino_th'] = np.sum(template['dino']<85)
	template['cactus_S1'] = cv2.cvtColor(np.array(cv2.imread(dir+'templates/cactus_S1.jpg')), cv2.COLOR_BGR2GRAY)
	template['cactus_S1_th'] = np.sum(template['cactus_S1']<85)
	template['cactus_S2'] = cv2.cvtColor(np.array(cv2.imread(dir+'templates/cactus_S2.jpeg')), cv2.COLOR_BGR2GRAY)
	template['cactus_S2_th'] = np.sum(template['cactus_S2']<85)
	template['cactus_S3'] = cv2.cvtColor(np.array(cv2.imread(dir+'templates/cactus_S3.jpeg')), cv2.COLOR_BGR2GRAY)
	template['cactus_S3_th'] = np.sum(template['cactus_S3']<85)
	template['cactus_B1'] = cv2.cvtColor(np.array(cv2.imread(dir+'templates/cactus_B1.jpg')), cv2.COLOR_BGR2GRAY)
	template['cactus_B1_th'] = np.sum(template['cactus_B1']<85)
	template['cactus_B2'] = cv2.cvtColor(np.array(cv2.imread(dir+'templates/cactus_B2.jpeg')), cv2.COLOR_BGR2GRAY)
	template['cactus_B2_th'] = np.sum(template['cactus_B2']<85)
	template['cactus_B3'] = cv2.cvtColor(np.array(cv2.imread(dir+'templates/cactus_B3.jpeg')), cv2.COLOR_BGR2GRAY)
	template['cactus_B3_th'] = np.sum(template['cactus_B3']<85)
	template['bird'] = cv2.cvtColor(np.array(cv2.imread(dir+'templates/bird.jpeg')), cv2.COLOR_BGR2GRAY)
	template['bird_th'] = np.sum(template['bird']<85)
	
	print("Template Thresh: ")
	print("\t dino:", template['dino'].shape)
	print("\t cactus_S1:", template['cactus_S1'].shape)
	print("\t cactus_S2:", template['cactus_S2'].shape)
	print("\t cactus_S3:", template['cactus_S3'].shape)
	print("\t cactus_B1:", template['cactus_B1'].shape)
	print("\t cactus_B2:", template['cactus_B2'].shape)
	print("\t cactus_B3:", template['cactus_B3'].shape)
	print("\t bird:", template['bird'].shape)
	
	print("\t dino_th:", template['dino_th'])
	print("\t cactus_S1_th:", template['cactus_S1_th'])
	print("\t cactus_S2:", template['cactus_S2_th'])
	print("\t cactus_S3:", template['cactus_S3_th'])
	print("\t cactus_B1:", template['cactus_B1_th'])
	print("\t cactus_B2:", template['cactus_B2_th'])
	print("\t cactus_B3:", template['cactus_B3_th'])
	print("\t bird_th:", template['bird_th'])

	return template

def detect_object(screen_shot, template, thresh, result):
	mn, mx,mnLoc,_ = cv2.minMaxLoc(result)
	'''
	MPx,MPy = mnLoc
	trows,tcols = np.array(template).shape[:2]
	if (thresh +150 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (thresh - 150 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
		cv2.putText(screen_shot,'cactus_S1',(MPx,MPy), font, 2,(0,0,255),2,cv2.LINE_AA)
		cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
	'''
	# create threshold from min val, find where sqdiff is less than thresh
	mn_th = (mn + 1e-6) * 1.5
	match_locations = np.where(result <= mn_th)

	w, h = template.shape[:2]
	for (x, y) in zip(match_locations[1], match_locations[0]):
	    cv2.rectangle(screen_shot, (x, y), (x+w, y+h), [0,255,255], 2)
	return screen_shot

def screenShotOperations():
	global mouseX, mouseY, offsetX, offsetY, screen_shot
	
	template = read_templates()
	while True:
		
		screen_shot_ = cv2.cvtColor(np.array(sct.grab(bounding_box)), cv2.COLOR_BGR2GRAY)
		screen_shot = screen_shot_[200:,:]
		print("screen shot:::", screen_shot.shape)
		cv2.imwrite(dir+'dino0.jpg', screen_shot_)
		break
		
		#screen_shot = np.array(screen_shot_)#[: screenH, : screenW,:]
		#print(type(screen_shot))
		#print("screen_shot: : ", np.shape(screen_shot))
		
		mouseX, mouseY = pyautogui.position()
		
		if cursorFlag:
			cv2.putText(screen_shot,str(mouseX-offsetX)+','+str(mouseY-offsetY),(mouseX-offsetX,mouseY-offsetY), font, 2,(0,0,255),2,cv2.LINE_AA)
			cv2.line(screen_shot,(0,(mouseY-offsetY)),(screenW*2, (mouseY-offsetY)),(255,0,0),5)
			cv2.line(screen_shot,((mouseX-offsetX),0),((mouseX-offsetX), screenH*2),(255,0,0),5)
		
		result_dino = cv2.matchTemplate(screen_shot, template['dino'], cv2.TM_SQDIFF_NORMED)
		result_cactus_S1 = cv2.matchTemplate(screen_shot, template['cactus_S1'], cv2.TM_SQDIFF_NORMED)
		result_cactus_S2 = cv2.matchTemplate(screen_shot, template['cactus_S2'], cv2.TM_SQDIFF_NORMED)
		result_cactus_S3 = cv2.matchTemplate(screen_shot, template['cactus_S3'], cv2.TM_SQDIFF_NORMED)
		result_cactus_B1 = cv2.matchTemplate(screen_shot, template['cactus_B1'], cv2.TM_SQDIFF_NORMED)
		result_cactus_B2 = cv2.matchTemplate(screen_shot, template['cactus_B2'], cv2.TM_SQDIFF_NORMED)
		result_cactus_B3 = cv2.matchTemplate(screen_shot, template['cactus_B3'], cv2.TM_SQDIFF_NORMED)
		result_bird = cv2.matchTemplate(screen_shot, template['bird'], cv2.TM_SQDIFF_NORMED)


		mn,mx,mnLoc,_ = cv2.minMaxLoc(result_dino)
		MPx,MPy = mnLoc
		trows,tcols = np.array(template['dino']).shape[:2]
		#cv2.imshow('dino',screen_shot[MPy:MPy+trows, MPx:MPx+tcols])
		#print(template['dino_th'] -150, np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85), template['dino_th'] +150)
		if (template['dino_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['dino_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
			cv2.putText(screen_shot,'dino',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
			cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
			#print("D: %.3f %.3f" %(mn,mx), end=' ')
		



		mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_S1)
		MPx,MPy = mnLoc
		trows,tcols = np.array(template['cactus_S1']).shape[:2]
		if (template['cactus_S1_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_S1_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
			result_cactus_S1[MPy:MPy+trows, MPx:MPx+tcols] = mx
			cv2.putText(screen_shot,'cactus_S1',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
			cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
			#print("S1: %.3f %.3f" %(mn,mx), end=' ')
		
			mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_S1)
			MPx,MPy = mnLoc
			trows,tcols = np.array(template['cactus_S1']).shape[:2]
			if (template['cactus_S1_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_S1_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
				#result_cactus_S1[MPy:MPy+trows, MPx:MPx+tcols] = mx
				cv2.putText(screen_shot,'cactus_S1',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
				#print("S1: %.3f %.3f" %(mn,mx), end=' ')



		mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_S2)
		MPx,MPy = mnLoc
		trows,tcols = np.array(template['cactus_S2']).shape[:2]
		if (template['cactus_S2_th'] +250 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_S2_th'] - 250 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
			result_cactus_S2[MPy:MPy+trows, MPx:MPx+tcols] = mx
			cv2.putText(screen_shot,'cactus_S2',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
			cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
			#print("S2: %.3f %.3f" %(mn,mx), end=' ')
			mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_S2)
			MPx,MPy = mnLoc
			trows,tcols = np.array(template['cactus_S2']).shape[:2]
			if (template['cactus_S2_th'] +200 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_S2_th'] - 200 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
				#result_cactus_S2[MPy:MPy+trows, MPx:MPx+tcols] = mx
				cv2.putText(screen_shot,'cactus_S2',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
				#print("S2: %.3f %.3f" %(mn,mx), end=' ')




		mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_S3)
		MPx,MPy = mnLoc
		trows,tcols = np.array(template['cactus_S3']).shape[:2]
		#cv2.imshow('cactus_S3',screen_shot[MPy:MPy+trows, MPx:MPx+tcols])
		print(template['cactus_S3_th'] - 250,np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85),template['cactus_S3_th'] +250)
		if (template['cactus_S3_th'] +250 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_S3_th'] - 250 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
			result_cactus_S3[MPy:MPy+trows, MPx:MPx+tcols] = mx
			cv2.putText(screen_shot,'cactus_S3',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
			cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
			#print("S3: %.3f %.3f" %(mn,mx), end=' ')
			mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_S3)
			MPx,MPy = mnLoc
			trows,tcols = np.array(template['cactus_S3']).shape[:2]
			if (template['cactus_S3_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_S3_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
				#result_cactus_S3[MPy:MPy+trows, MPx:MPx+tcols] = mx
				cv2.putText(screen_shot,'cactus_S3',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
				#print("S3: %.3f %.3f" %(mn,mx), end=' ')




		mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_B1)
		MPx,MPy = mnLoc
		trows,tcols = np.array(template['cactus_B1']).shape[:2]
		if (template['cactus_B1_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_B1_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
			result_cactus_B1[MPy:MPy+trows, MPx:MPx+tcols] = mx
			cv2.putText(screen_shot,'cactus_B1',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
			cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
			#print("B1: %.3f %.3f" %(mn,mx), end=' ')
			mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_B1)
			MPx,MPy = mnLoc
			trows,tcols = np.array(template['cactus_B1']).shape[:2]
			if (template['cactus_B1_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_B1_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
				#result_cactus_B1[MPy:MPy+trows, MPx:MPx+tcols] = mx
				cv2.putText(screen_shot,'cactus_B1',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
				#print("B1: %.3f %.3f" %(mn,mx), end=' ')




		mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_B2)
		MPx,MPy = mnLoc
		trows,tcols = np.array(template['cactus_B2']).shape[:2]
		if (template['cactus_B2_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_B2_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
			result_cactus_B2[MPy:MPy+trows, MPx:MPx+tcols] = mx
			cv2.putText(screen_shot,'cactus_B2',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
			cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
			#print("B2: %.3f %.3f" %(mn,mx), end=' ')
			mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_B2)
			MPx,MPy = mnLoc
			trows,tcols = np.array(template['cactus_B2']).shape[:2]
			if (template['cactus_B2_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_B2_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
				#result_cactus_B2[MPy:MPy+trows, MPx:MPx+tcols] = mx
				cv2.putText(screen_shot,'cactus_B2',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(screen_shot, (MPx,MPy+50),(MPx+tcols,MPy+trows),(0,0,0),2)
				#print("B2: %.3f %.3f" %(mn,mx), end=' ')



		mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_B3)
		MPx,MPy = mnLoc
		trows,tcols = np.array(template['cactus_B3']).shape[:2]
		if (template['cactus_B3_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_B3_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
			result_cactus_B3[MPy:MPy+trows, MPx:MPx+tcols] = mx
			cv2.putText(screen_shot,'cactus_B3',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
			cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
			#print("B3: %.3f %.3f" %(mn,mx), end=' ')
			mn, mx,mnLoc,_ = cv2.minMaxLoc(result_cactus_B3)
			MPx,MPy = mnLoc
			trows,tcols = np.array(template['cactus_B3']).shape[:2]
			if (template['cactus_B3_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['cactus_B3_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
				cv2.putText(screen_shot,'cactus_B3',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
				#print("B3: %.3f %.3f" %(mn,mx), end=' ')



		mn, mx,mnLoc,_ = cv2.minMaxLoc(result_bird)
		MPx,MPy = mnLoc
		trows,tcols = np.array(template['bird']).shape[:2]
		if (template['bird_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['bird_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
			result_cactus_B3[MPy:MPy+trows, MPx:MPx+tcols] = mx
			cv2.putText(screen_shot,'bird',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
			cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
			#print("S1: %.3f %.3f" %(mn,mx))
			mn, mx,mnLoc,_ = cv2.minMaxLoc(result_bird)
			MPx,MPy = mnLoc
			trows,tcols = np.array(template['bird']).shape[:2]
			if (template['bird_th'] +300 > np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)) and (template['bird_th'] - 300 < np.sum(screen_shot[MPy:MPy+trows, MPx:MPx+tcols]<85)):
				result_cactus_B3[MPy:MPy+trows, MPx:MPx+tcols] = mx
				cv2.putText(screen_shot,'bird',(MPx,MPy+20), font, 1,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(screen_shot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,0),2)
				#print("S1: %.3f %.3f" %(mn,mx))

		
		#imScreen = cv2.resize(np.array(screen_shot), (600, 150))
		screen_shot_[200:,:] = screen_shot
		cv2.imshow('screen', np.array(screen_shot_))
		
		cv2.imshow('cactus_obs', screen_shot)
		
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


'''
25,100

70,100
25,150
X:  140  Y:  206
X:  140  Y:  206
X:  140  Y:  206
X:  140  Y:  206
X:  140  Y:  206
X:  140  Y:  206
X:  54  Y:  298
X:  54  Y:  298

'''