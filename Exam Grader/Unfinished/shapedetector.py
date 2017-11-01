import cv2
import imutils

def is_valid_triangle(c):
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.1 * perimeter, True)
    return True if len(approx) == 3 else False  

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread("image.png")
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
 
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
 
# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[1]

# loop over the contours
for c in cnts:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    shape = is_valid_triangle(c)

    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)

cv2.imshow("Image", image)
cv2.waitKey(0)
