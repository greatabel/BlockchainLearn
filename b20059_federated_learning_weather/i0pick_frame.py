import cv2
 
# Opens the Video file
# movie_name = 'Blue_Planet_II'
movie_name = '妙言趣语'
cap= cv2.VideoCapture('demo_video/'+movie_name+'.mp4')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    print('i=', i)
    if ret == False:
        break
    if i % 50 == 0:
    	cv2.imwrite('movie/static/img/source/'+movie_name+'_'+str(i)+'.jpg',frame)
    i+=1
 
cap.release()
cv2.destroyAllWindows()