from flask import Flask, render_template, Response, redirect
from camera import VideoCamera

app = Flask(__name__)
video_stream = None
stop = True

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/stop')
def stop():
   global stop
   global video_stream
   if not stop:
      video_stream.video.release()
      stop = True
   return redirect('/')

@app.route('/start')
def start():
   global stop
   global video_stream
   if stop:
      video_stream = VideoCamera()
      stop = False
   return redirect('/')

def gen(camera, i):
   try:
       while True:
           frame = camera.get_frame(i)
           if frame == None:
               break
           yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
   except:
      pass

@app.route('/video_feed')
def video_feed():
     return Response(gen(video_stream, 0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
     return Response(gen(video_stream, 1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
     return Response(gen(video_stream, 2), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed3')
def video_feed3():
     return Response(gen(video_stream, 3), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   app.run(debug = True)
