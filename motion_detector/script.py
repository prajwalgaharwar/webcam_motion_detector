import cv2,time,pandas
from datetime import datetime

first_frame=None
status=0
status_list=[None,None]
times=[]
video=cv2.VideoCapture(0)
df=pandas.DataFrame(columns=["Start","End"])

while True:
    check, frame=video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    if first_frame is None:
        first_frame=gray
        continue

    delt_frame=cv2.absdiff(first_frame,gray)

    thresh_frame=cv2.threshold(delt_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=3)

    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
            
        
        status=1
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+w),(0,255,0),3)

    status_list.append(status)

    status_list=status_list[-2:]
    
    if status_list[-2]==1 and status_list[-1]==0:
        times.append(datetime.now())

    elif status_list[-2]==0 and status_list[-1]==1:
        times.append(datetime.now())

    
    cv2.imshow("Capturing",gray)
    cv2.imshow("Delta",delt_frame)
    cv2.imshow("Threshold Delta",thresh_frame)
    cv2.imshow("colour",frame)

    key=cv2.waitKey(10)
    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break
    
for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

df.to_csv("times.csv")
print(times)
video.release()

cv2.destroyAllWindows