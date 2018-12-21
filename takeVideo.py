import numpy as np
import cv2
import imutils
import serial
import time

# Always changes !!IMPORTANT TO CHECK!!
# Stream video dari link ini : Via IP Webcam
stream = cv2.VideoCapture("http://192.168.43.1:8080/video")

# variabel untuk komunikasi dengan serial Arduino
serialArduino = serial.Serial('COM12', 9600)

while(True):    
    # Decode, dan baca frame
    ret, frame = stream.read()
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Varible tinggi, lebar, channel framenya
    height, width, channel = frame.shape

    # Atur nilai HSV (atau RGB?) yang ingin di"lihat"
    BLUE_MIN = np.array([110, 50, 50], np.uint8)
    BLUE_MAX = np.array([130, 255, 255], np.uint8)

    # Convert warnanya dari BGR ke HSV
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(hsv_img,(5,5),0) #blur the image

    # Cek apakah melihat nilai HSV yang diinginkan
    frame_threshed = cv2.inRange(blur, BLUE_MIN, BLUE_MAX)

    # Atur ukuran kernel untuk image processing
    kernel = np.ones((10, 10), np.uint8)
    opening = cv2.morphologyEx(frame_threshed, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((20, 20), np.uint8)
    dilation = cv2.dilate(opening, kernel, iterations=1)

    # Cari outline dari gambar dan yang ingin dilihat 
    cnts = cv2.findContours(
        dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # batas yang menentukan apakah robot masih berada di tengah jalan
    boundLeft = int(width * 0.40)
    boundRight = int(width * 0.60)

    # Loops over
    for c in cnts:
        # Yang terbesar
        con = max(cnts, key=cv2.contourArea)
        
        # Cari tengahnya
        M = cv2.moments(con)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # Gambar contournya
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

        # Define the x, y coordinates; width and height of the bounding object
        x, y, w, h = cv2.boundingRect(con)

        # gambar titik ditengahnya
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

        # gambar batas untuk tanda robot berada di tengah
        cv2.line(frame, (boundLeft, 0), (boundLeft, height), (255, 0, 0), 3)
        cv2.line(frame, (boundRight, 0), (boundRight, height), (255, 0, 0), 3)

        # Cek ada dimana garisnya.
        if cX >= boundRight:
            # Move to the right --- 1
            serialArduino.write('1'.encode())
            print("Kanan")
        elif cX <= boundLeft:
            # Move to the left 	--- 2
            serialArduino.write('2'.encode())
            print("Kiri")
        else:
            # Forward
            serialArduino.write('3'.encode())
            print("Maju")

    # Kasih liat gambarnya
    cv2.imshow("Image", frame)

     # Close the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        serialArduino.write('2'.encode())
        break

stream.release()
cv2.destroyAllWindows()	