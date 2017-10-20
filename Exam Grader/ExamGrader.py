import cv2
import numpy as np
import subprocess
from PIL import Image
from binascii import unhexlify
from simplecrypt import decrypt
from time import sleep

class Grader(object):
    def __init__(self):
        self.dirpath = "C:\\ZBar\\bin\\zbarcam.exe"

        self.lookup_list = ['1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a',
                            '9a', '10a', '1b', '2b', '3b', '4b', '5b', '6b',
                            '7b', '8b', '9b', '10b', '1c', '2c', '3c', '4c',
                            '5c', '6c', '7c', '8c', '9c', '10c', '1d', '2d',
                            '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d',
                            '11a', '12a', '13a', '14a', '15a', '16a', '17a',
                            '18a', '19a', '20a', '11b', '12b', '13b', '14b',
                            '15b', '16b', '17b', '18b', '19b', '20b', '11c',
                            '12c', '13c', '14c', '15c', '16c', '17c', '18c',
                            '19c', '20c', '11d', '12d', '13d', '14d', '15d',
                            '16d', '17d', '18d', '19d', '20d', '21a', '22a',
                            '23a', '24a', '25a', '26a', '27a', '28a', '29a',
                            '30a', '21b', '22b', '23b', '24b', '25b', '26b',
                            '27b', '28b', '29b', '30b', '21c', '22c', '23c',
                            '24c', '25c', '26c', '27c', '28c', '29c', '30c',
                            '21d', '22d', '23d', '24d', '25d', '26d', '27d',
                            '28d', '29d', '30d', '31a', '32a', '33a', '34a',
                            '35a', '36a', '37a', '38a', '39a', '40a', '31b',
                            '32b', '33b', '34b', '35b', '36b', '37b', '38b',
                            '39b', '40b', '31c', '32c', '33c', '34c', '35c',
                            '36c', '37c', '38c', '39c', '40c', '31d', '32d',
                            '33d', '34d', '35d', '36d', '37d', '38d', '39d',
                            '40d']

    def lookup(self, i):
        return [self.lookup_list[i][:-1], self.lookup_list[i][-1:]]

    def zbar_reader(self, dirpath):
        print("Expose barcode to camera")
        raw_code = ''
        while raw_code == '':
            raw_code = subprocess.check_output(dirpath,shell=True)
        raw_code = raw_code.split()[0][8:]
        return decrypt('RSbv2HZbON6rseN!', unhexlify(raw_code))# change example passphrase

    def grade_exam(self, comp_list, answer_list):# no duplicate checking
        comp_list = sorted(comp_list, key=lambda answer: answer[0])
        for i in range(len(comp_list)):
            comp_list[i] = comp_list[i][0] + comp_list[i][1]
        questions = len(answer_list)
        correct, incorrect = 0, []
        for response in comp_list:
            if response in answer_list:
                correct += 1
            else:
                incorrect.append(answer_list[int(response[:-1]) - 1])

        return questions, correct, incorrect

    def run(self):
        cap = cv2.VideoCapture(0)

        while(True):
            retval, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 25, np.array([]), 10, 25, 8, 14)
            a, b, c = circles.shape

            for i in range(b):
                cv2.circle(frame, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow("Grade Cam", frame)
            if b == 120:
                center_coords = []
                for i in range(b):
                    center_coords.append((circles[0][i][0], circles[0][i][1]))
                cv2.imwrite("image.png",gray)
                cap.release()
                cv2.destroyAllWindows()
                print("Image saved!")

                sorted_coords = sorted(center_coords,key=lambda coord: (coord[0],coord[1]))# sorting circle centers from smallest to largest
                split_coords = []
                for i in range(12):
                    split_coords += sorted(sorted_coords[10*i:10*i+10],key=lambda coord: coord[1])# separating by y-value from smallest to largest

                im = Image.open("image.png")
                pix = im.load()
                comp_list = []

                for i in range(120):
                    gindex = 0
                    #compute simple average of white zones, and subtract constant to calculate threshold
                    gray_threshold = (pix[10, 240] + pix[630, 240] + pix[320, 10] + pix[320, 470]) / 4 - 30
                    #look in range of +/- 3 pixels in x and y directions
                    for j in range(int(split_coords[i][0]) - 3, int(split_coords[i][0]) + 3):
                        for k in range(int(split_coords[i][1]) - 3, int(split_coords[i][1]) + 3):
                            try:
                                if pix[j, k] < gray_threshold:
                                    gindex += 1
                            except:
                                if j >= 640: j = 639
                                elif j <= 0: j = 1
                                elif k >= 480: k = 479
                                elif k <= 0: k = 1
                                if pix[j, k] < gray_threshold:
                                    gindex += 1
                    if gindex > 18:# count dark enough circles as filled.
                        comp_list.append(self.lookup(i))
                    
                print("Scan the QR code now.")
                raw_code = self.zbar_reader(self.dirpath)
                answer_list = raw_code.decode('utf-8').split('x')[:-1]

                questions, correct, incorrect = self.grade_exam(comp_list, answer_list)

                print("{0} out of {1} correct.".format(correct, questions))
                print("Score: {0}".format(10 * round(correct, 2) / round(questions, 2)))
                print('Answers for incorrect responses are shown below:')
                print(incorrect)
                
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    new_instance = Grader()
    new_instance.run()
