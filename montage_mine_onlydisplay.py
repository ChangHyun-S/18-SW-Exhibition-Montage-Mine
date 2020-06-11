from picamera.array import PiRGBArray
from picamera import PiCamera
import telepot
import time
import datetime
import cv2

def detect(img, cascade):
    #temp = time.time()
    #temp = time.strftime("%Y/%m/%d %H:%M:%S")
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)

    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    
    print(nowDatetime)
    print('얼굴 인식됨...')
    
    cv2.imwrite('/home/pi/camera/' + str(nowDatetime)+'.jpg',vis)
    print('이미지 저장...')
    bot.sendMessage(chat_id = '726401952', text = '침입이 감지되었습니다.')
    goPhoto = open('/home/pi/camera/' + str(nowDatetime)+'.jpg', 'rb')
    bot.sendPhoto(chat_id = '726401952', photo = goPhoto)
    print('텔레그램 전송완료...\n')
    #bot.sendMessage(chat_id = '@sending_test_bot', text = '침입이 감지되었습니다')
    return rects

now = datetime.datetime.now()
print('서비스 시작 :', now.strftime('%Y-%m-%d %H:%M:%S'))
print()

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

cascade = cv2.CascadeClassifier('/home/pi/opencv/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_alt.xml')

#텔레그램
TOKEN = '797044289:AAERPOzCVLTy_K0sPPC-60GfCfY6nmPzmSo'
bot = telepot.Bot(TOKEN)

time.sleep(0.1)

# 긁는 다
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    rects = detect(gray, cascade)
    vis = img.copy()
    draw_rects(vis, rects, (0, 255, 0))

    # 미리보기띄우기1
    #cv2.imshow("Frame", vis) 커맨드라인 전용. 프레임 안띄움.
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    
    #q누르면1나감1
    if key == ord("q"):
        break
