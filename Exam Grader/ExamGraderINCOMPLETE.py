import numpy as np
import cv2, string, subprocess
from PIL import Image
from binascii import unhexlify
from simplecrypt import decrypt
from time import sleep

dirpath = "C:\\ZBar\\bin\\zbarcam.exe"

def Lookup(idxvalue):
    #left this going to 40 in case we want to expand in the future
    LookupList = ['1xa', '2xa', '3xa', '4xa', '5xa', '6xa', '7xa', '8xa', '9xa', '10xa', \
              '1xb', '2xb', '3xb', '4xb', '5xb', '6xb', '7xb', '8xb', '9xb', '10xb', \
              '1xc', '2xc', '3xc', '4xc', '5xc', '6xc', '7xc', '8xc', '9xc', '10xc', \
              '1xd', '2xd', '3xd', '4xd', '5xd', '6xd', '7xd', '8xd', '9xd', '10xd', \
              '11xa', '12xa', '13xa', '14xa', '15xa', '16xa', '17xa', '18xa', '19xa', \
              '20xa', '11xb', '12xb', '13xb', '14xb', '15xb', '16xb', '17xb', '18xb', \
              '19xb', '20xb', '11xc', '12xc', '13xc', '14xc', '15xc', '16xc', '17xc', \
              '18xc', '19xc', '20xc', '11xd', '12xd', '13xd', '14xd', '15xd', '16xd', \
              '17xd', '18xd', '19xd', '20xd', '21xa', '22xa', '23xa', '24xa', '25xa', \
              '26xa', '27xa', '28xa', '29xa', '30xa', '21xb', '22xb', '23xb', '24xb', \
              '25xb', '26xb', '27xb', '28xb', '29xb', '30xb', '21xc', '22xc', '23xc', \
              '24xc', '25xc', '26xc', '27xc', '28xc', '29xc', '30xc', '21xd', '22xd', \
              '23xd', '24xd', '25xd', '26xd', '27xd', '28xd', '29xd', '30xd', '31xa', \
              '32xa', '33xa', '34xa', '35xa', '36xa', '37xa', '38xa', '39xa', '40xa', \
              '31xb', '32xb', '33xb', '34xb', '35xb', '36xb', '37xb', '38xb', '39xb', \
              '40xb', '31xc', '32xc', '33xc', '34xc', '35xc', '36xc', '37xc', '38xc', \
              '39xc', '40xc', '31xd', '32xd', '33xd', '34xd', '35xd', '36xd', '37xd', \
              '38xd', '39xd', '40xd']
    
    mcidx = LookupList[idxvalue]
    mclist = mcidx.split('x')
    return mclist

def zbar_reader(self):
    print("Expose barcode to camera")
    raw_code = ''
    while raw_code == '':
        raw_code = subprocess.check_output(dirpath,shell=True)
    raw_code = raw_code.split()[0][8:]
    # insert decryption routine here
    return raw_code

def grade_exam(self, complist, answerlist):
    #no need to check for duplicates currently due to class policy
    #prep the reponse list
    complist = sorted(complist, key=lambda answer: answer[0])
    for i in range(len(complist)):
        complist[i] = complist[i][0]+complist[i][1]
    #how many questions on the exam?
    examquestions = len(answerlist)
    correctresponses = 0
    incorrectanswers = []
    for response in complist:
        if response in answerlist:
            correctresponses+=1
        else:
            try:
                incorrectanswers.append(answerlist[int(response[:-1])-1])
            except:
                pass
    return correctresponses, examquestions, incorrectanswers

def run(self):
    cap = cv2.VideoCapture(0)

    while(True):
        retval, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #delay here if display is saturated and no circles found.
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 25, np.array([]), 10, 25, 8, 14)
        a, b, c = circles.shape
        for i in range(b):
            cv2.circle(frame, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("Grade Cam", frame)
        if b == 120:
            centercoords = []
            for i in range(b):
                centercoords.append((circles[0][i][0], circles[0][i][1]))
            cv2.imwrite("image.png",gray)
            cap.release()
            cv2.destroyAllWindows()
            print("Image saved!")
            #the circle center coordinates are sorted by x,y value from smallest to largest
            sortedcoords = sorted(centercoords,key=lambda coord: (coord[0],coord[1]))
            splitcoords = []
            #the sorted coordinate list is separated into columns, which are sorted
            #by the y-values from smallest to largest.
            for i in range(len(sortedcoords)/10):
                segcoords = sorted(sortedcoords[10*i:10*i+10],key=lambda coord: coord[1])
                splitcoords.extend(segcoords)
            #since the x-values can vary depending on the orientation of the grading sheet,
            #we will use the y-values to determine which circle we are looking at.

            #loading the image for pixel analysis
            im = Image.open("image.png")
            pix = im.load()
            complist = []

            for i in range(len(splitcoords)):
                gindex = 0
                #compute simple average of white zones, and subtract constant to calculate threshold
                graythreshold = (pix[10,240]+pix[630,240]+pix[320,10]+pix[320,470])/4 - 30
                #look in range of +/- 3 pixels in x and y directions
                for j in range(int(splitcoords[i][0])-3,int(splitcoords[i][0])+3):
                    for k in range(int(splitcoords[i][1])-3,int(splitcoords[i][1])+3):
                        try:
                            #if pixel is darker than certain amount, increase the gray index and count it.
                            if pix[j,k] < graythreshold:
                                gindex += 1
                        except:
                            if j >= 640: j = 639
                            elif j <= 0: j = 1
                            elif k >= 480: k = 479
                            elif k <= 0: k = 1
                            if pix[j,k] < graythreshold:
                                gindex += 1
                if gindex > 18:
                    #if there are enough dark pixels in the circle, count it as filled.
                    #print("This circle is filled: ")
                    mclist = Lookup(i)
                    complist.append(mclist)
                
            #print(complist)

            print("Scan the QR code now.")
            rawcode = ZBarReader(dirpath)
            answerlist = rawcode.split('x')[:-1]
            #print(answerlist)

            correctresponses, examquestions, incorrectanswers = GradeExam(complist, answerlist)

            print(str(correctresponses) + " out of " + str(examquestions) + " correct.")
            print('Score: ' + str(10*round(correctresponses,2)/round(examquestions,2)))
            print('Answers for incorrect responses are shown below:')
            print(incorrectanswers)
            
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



