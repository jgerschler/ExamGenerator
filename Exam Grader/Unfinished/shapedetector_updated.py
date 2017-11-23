import cv2
import imutils
import math



def is_valid_triangle(c):
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.1 * perimeter, True) # alter 0.01 as req'd
    return True if len(approx) == 3 else False  

def filter_triangles(t_list):
    markers = []
    t_list.sort(key=lambda x: x[3])

    if (t_list[0][3] >= t_list[1][3] * 0.95 and
        t_list[0][3] <= t_list[1][3] * 1.05):

        markers.append(t_list[0])
    
    for i in range(len(t_list) - 2):
        i += 1
        if ((t_list[i][3] >= t_list[i - 1][3] * 0.95 and
            t_list[i][3] <= t_list[i - 1][3] * 1.05) or
            (t_list[i][3] >= t_list[i + 1][3] * 0.95 and
            t_list[i][3] <= t_list[i + 1][3] * 1.05)):

            markers.append(t_list[i])

    if (t_list[-1][3] >= t_list[-2][3] * 0.95 and
        t_list[-1][3] <= t_list[-2][3] * 1.05):

        markers.append(t_list[-1])

    return markers

image = cv2.imread("image.png")
 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY_INV)[1]
 
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

print(markers)

# test code!
top_markers = [markers[0], markers[2]]

d1 = 0.1200 # marker center to dot center distance factor
d2 = 0.0530 # lateral dot center to dot center distance factor
d3 = 0.0849 # row center to row center distance factor

x1 = top_markers[0][1]
y1 = top_markers[0][2]
x2 = top_markers[1][1]
y2 = top_markers[1][2]
print(x1, y1, x2, y2)

gamma = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)# not needed

#first_row_pnts = [[((1 - d1) * x2 - d1 * x1), y1]]
first_row_pnts = [[x2 - d1 * (x2 -x1), y2 - d1 * abs(y2 - y1)],
                  [x2 - (d1 + d2) * (x2 -x1), y2 - (d1 + d2) * abs(y2 - y1)],
                  [x2 - (d1 + 2 * d2) * (x2 -x1), y2 - (d1 + 2 * d2) * abs(y2 - y1)],
                  [x2 - (d1 + 3 * d2) * (x2 -x1), y2 - (d1 + 3 * d2) * abs(y2 - y1)],
                  [x2 - (d1 + 4 * d2 + d3) * (x2 -x1), y2 - (d1 + 4 * d2 + d3) * abs(y2 - y1)],
                  [x2 - (d1 + 5 * d2 + d3) * (x2 -x1), y2 - (d1 + 5 * d2 + d3) * abs(y2 - y1)],
                  [x2 - (d1 + 6 * d2 + d3) * (x2 -x1), y2 - (d1 + 6 * d2 + d3) * abs(y2 - y1)],
                  [x2 - (d1 + 7 * d2 + d3) * (x2 -x1), y2 - (d1 + 7 * d2 + d3) * abs(y2 - y1)],
                  [x2 - (d1 + 8 * d2 + 2 * d3) * (x2 -x1), y2 - (d1 + 8 * d2 + 2 * d3) * abs(y2 - y1)],
                  [x2 - (d1 + 9 * d2 + 2 * d3) * (x2 -x1), y2 - (d1 + 9 * d2 + 2 * d3) * abs(y2 - y1)],
                  [x2 - (d1 + 10 * d2 + 2 * d3) * (x2 -x1), y2 - (d1 + 10 * d2 + 2 * d3) * abs(y2 - y1)],
                  [x2 - (d1 + 11 * d2 + 2 * d3) * (x2 -x1), y2 - (d1 + 11 * d2 + 2 * d3) * abs(y2 - y1)]] # horizontal testing only

for entry in first_row_pnts:
    cv2.circle(image, (int(entry[0]), int(entry[1])), 5, (0, 0, 255), -1)

cv2.imshow("Image", image)
cv2.waitKey(0)
