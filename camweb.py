import cv2
import numpy as np
import time
import datetime
import sys
from flask import Flask, render_template, Response

faceCascade = cv2.CascadeClassifier("haarcascade_frontface.xml")
num = 3
app = Flask(__name__)

camera = cv2.VideoCapture(0)
width = camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
height = camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)   

@app.route('/')
def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
            'title':'Image Streaming',
            'time': timeString
            }
    return render_template('index.html', **templateData)
    # return render_template('index.html')

def gen_frames():
    time.sleep(0.2)
    lastTime = time.time()*1000.0
    while True:
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5)
        delt = time.time()*1000.0-lastTime
        s = str(int(delt))
        #print (delt," Found {0} faces!".format(len(faces)) )
        lastTime = time.time()*1000.0

        # 가이드라인 그려서 영역지정( 동그라미)
        # for (x, y, w, h) in faces:
        #     cv2.circle(frame, (int(x+w/2), int(y+h/2)), int((w+h)/3), (255, 255, 255), 3)
        # cv2.putText(frame, s, (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # now = datetime.datetime.now()
        # timeString = now.strftime("%Y-%m-%d %H:%M")
        # cv2.putText(frame, timeString, (10, 45),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        # cv2.imshow("Frame", frame)
      
        #가이드라인 그려서 영역지정( 사각형)
        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, s, (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        cv2.putText(frame, timeString, (10, 45),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.imshow("Frame", frame)

      
        key = cv2.waitKey(1) & 0xFF
     # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    # out.realease()
    cv2.destroyAllWindows()
       
 
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0') 