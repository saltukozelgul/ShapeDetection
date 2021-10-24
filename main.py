
import simpleaudio as sa
from cv2 import cv2

def getContours(img):
    shapes = []
    imgCopy = preProc()[1]
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area>700:
            peri = cv2.arcLength(contour,True)
            apr = cv2.approxPolyDP(contour,0.026*peri,True)
            if len(apr) >=3 and len(apr) < 12:
                cord = len(apr)
                x, y, w, h = cv2.boundingRect(apr)
                if (h < 100):
                    if  cord == 3 :
                        objectType = "Ucgen"
                        id = "3"
                    elif cord == 8:
                        objectType = "Daire"
                        id = "2"
                    elif cord == 9:
                        objectType = "Yildiz"
                        id = "4"
                    elif cord == 11:
                        objectType = "Semsiye"
                        id = "1"
                    object = {
                        "imgCopy": imgCopy,
                        "contour": contour,
                        "objectType": objectType,
                        "x" : x,
                        "y" : y,
                        "w" : w,
                        "h" : h,
                        "id" : id
                    }
                    shapes.append(object)
    return shapes
def drawShapes(shapes):
    sortedShapes = [{},{},{},{}]
    for shape in shapes:
        if shape["id"] == "1":
            sortedShapes[0] = shape
        elif shape["id"] == "2":
            sortedShapes[1] = shape
        elif shape["id"] == "3":
            sortedShapes[2] = shape
        elif shape["id"] == "4":
            sortedShapes[3] = shape
    for shape in sortedShapes:
        print(shape["id"])
        x = shape["x"]
        y = shape["y"]
        w = shape["w"]
        h = shape["h"]
        objectType = shape["objectType"]
        contour = shape["contour"]
        imgCopy = shape["imgCopy"]
        cv2.rectangle(imgCopy, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), 3)
        cv2.drawContours(imgCopy, contour, -1, (255, 0, 0), 5)
        cv2.putText(imgCopy, objectType, (x + (w // 2), y + h + 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0),
                    0)
        cv2.waitKey(3000)
        cv2.imshow("3", imgCopy)
        wave_object = sa.WaveObject.from_wave_file('assets/ding.wav')
        play_object = wave_object.play()
def preProc():

    img = cv2.imread("assets/testimage.jpg")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    imgCopy = img.copy()
    cv2.imshow("3",imgCopy)
    returnList = [imgCanny,imgCopy]
    return returnList

shapes = getContours(preProc()[0])
drawShapes(shapes)
cv2.waitKey(0)