import cv2
import imutils
import math


def is_valid_triangle(c):
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.1 * perimeter, True) # alter 0.1 as req'd
    return True if len(approx) == 3 else False  

def filter_triangles(t_list):

    markers = []

    t_list = [x for x in t_list if x[3] > 125]

    if len(t_list) < 2:
        print("Tracking triangles not found!")
        return
    
    t_list.sort(key=lambda x: x[3])

    if len(t_list) > 2:
        if (t_list[0][3] >= t_list[1][3] * 0.85 and
            t_list[0][3] <= t_list[1][3] * 1.15):

            markers.append(t_list[0])
        
        for i in range(len(t_list) - 2):
            i += 1
            if ((t_list[i][3] >= t_list[i - 1][3] * 0.85 and
                t_list[i][3] <= t_list[i - 1][3] * 1.15) or
                (t_list[i][3] >= t_list[i + 1][3] * 0.85 and
                t_list[i][3] <= t_list[i + 1][3] * 1.15)):

                markers.append(t_list[i])

        if (t_list[-1][3] >= t_list[-2][3] * 0.85 and
            t_list[-1][3] <= t_list[-2][3] * 1.15):

            markers.append(t_list[-1])

    else:
        markers = t_list[:]

    return markers

image = cv2.imread("tc//tc1.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

background_thresh = 0.8 * ((int(blurred[10, 10]) + int(blurred[470, 630]) + int(blurred[470, 10]) + int(blurred[10, 630])) / 4)# alter threshold

print(background_thresh)

thresh = cv2.threshold(blurred, background_thresh, 255, cv2.THRESH_BINARY_INV)[1]
 
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[1]
triangles = []
i = 0

for c in cnts:
    # compute the center of the contour
    if is_valid_triangle(c):
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
        triangles.append((i, cX, cY, M["m00"]))
        i += 1

        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 2, (0, 0, 255), -1)

markers = filter_triangles(triangles)
markers.sort(key=lambda x:math.sqrt(x[1]**2 + x[2]**2))

d1 = 0.1250 # marker center to dot center distance factor
d2 = 0.0525 # horizontal dot center to dot center distance factor
d3 = 0.0879 # row center to row center distance factor
d4 = 0.0524 # vertical dot center to dot center distance factor

x1 = markers[0][1]
y1 = markers[0][2]
x2 = markers[1][1]
y2 = markers[1][2]

gamma = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
sin_a = (x2 - x1)/gamma
sin_b = (y2 - y1)/gamma

for i in range(10):
    for j in range(4):
        cv2.circle(image, (int(x2 - (d1 + j * d2) * (x2 - x1) - i * d4 * gamma * sin_b), int(y2 - (d1 + j * d2) * (y2 - y1) + i * d4 * gamma * sin_a)), 3, (0, 0, 255), -1)
        cv2.circle(image, (int(x2 - (d1 + (j + 4) * d2 + d3) * (x2 - x1) - i * d4 * gamma * sin_b), int(y2 - (d1 + (j + 4) * d2 + d3) * (y2 - y1) + i * d4 * gamma * sin_a)), 3, (0, 0, 255), -1)
        cv2.circle(image, (int(x2 - (d1 + (j + 8) * d2 + 2 * d3) * (x2 - x1) - i * d4 * gamma * sin_b), int(y2 - (d1 + (j + 8) * d2 + 2 * d3) * (y2 - y1) + i * d4 * gamma * sin_a)), 3, (0, 0, 255), -1)

cv2.imshow("Image", image)
cv2.waitKey(0)
