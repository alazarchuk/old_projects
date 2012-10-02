#! /usr/bin/env python

print "OpenCV Python version of contours"

# import the necessary things for OpenCV
import sys
import cv

# some default constants
_SIZEW = 500
_SIZEH = 500

_MSIZEW = 1920*0.9
_MSIZEH = 1080*0.9

_DEFAULT_LEVEL = 4

# definition of some colors
_red =  (0, 0, 255, 0);
_green =  (0, 255, 0, 0);
_white = cv.RealScalar (255)
_black = cv.RealScalar (0)

# the callback on the trackbar, to set the level of contours we want
# to display
def on_trackbar (position):

    # create the image for putting in it the founded contours
    contours_image = cv.CreateImage ( (_SIZEW, _SIZEH), 8, 3)
    scale_factor = max(1.0*_SIZEW/_MSIZEW, 1.0*_SIZEH/_MSIZEH)
    contours_image_to_display = cv.CreateImage ( (_SIZEW/scale_factor, _SIZEH/scale_factor), 8, 3)

    # compute the real level of display, given the current position
    levels = position - 3

    # initialisation
    _contours = contours

    #if levels <= 0:
    #    # zero or negative value
    #    # => get to the nearest face to make it look more funny
    #    _contours = [] #contours.h_next().h_next().h_next()

    # first, clear the image where we will draw contours
    cv.SetZero (contours_image)

    # draw contours in red and green
    cv.DrawContours (contours_image, _contours,
                       _red, _green,
                       levels, 3, cv.CV_AA,
                        (0, 0))

    # finally, show the image
    cv.Resize(contours_image, contours_image_to_display, cv.CV_INTER_CUBIC)
    cv.ShowImage ("contours", contours_image_to_display)

if __name__ == '__main__':

    # create the image where we want to display results
    #image = cv.CreateImage ( (_SIZE, _SIZE), 8, 1)
    if len(sys.argv) <= 1:
        print "Image required"
        sys.exit(1)

    image_origin = cv.LoadImage(sys.argv[1], cv.CV_LOAD_IMAGE_GRAYSCALE)
    global _SIZEW, _SIZEH
    _SIZEW = image_origin.width
    _SIZEH = image_origin.height

    image_er = cv.CreateImage ( (image_origin.width, image_origin.height), 8, 1)
    image_dil = cv.CreateImage ( (image_origin.width, image_origin.height), 8, 1)
    image = cv.CreateImage ( (image_origin.width, image_origin.height), 8, 1)

    pos = 5
    element = cv.CreateStructuringElementEx(pos*2+1, pos*2+1, pos, pos, cv.CV_SHAPE_RECT)
    cv.Erode(image_origin, image_er, element, 1)
    cv.Dilate(image_er, image_dil, element, 1)
    cv.Canny(image_dil, image, pos*10,  pos * 10 * 3, 3)

    #image = image_dil
    ## start with an empty image
    #cv.SetZero (image)

    ## draw the original picture
    #for i in range (6):
    #    dx = (i % 2) * 250 - 30
    #    dy = (i / 2) * 150
    #
    #    cv.Ellipse (image,
    #                   (dx + 150, dy + 100),
    #                   (100, 70),
    #                  0, 0, 360, _white, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 115, dy + 70),
    #                   (30, 20),
    #                  0, 0, 360, _black, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 185, dy + 70),
    #                   (30, 20),
    #                  0, 0, 360, _black, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 115, dy + 70),
    #                   (15, 15),
    #                  0, 0, 360, _white, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 185, dy + 70),
    #                   (15, 15),
    #                  0, 0, 360, _white, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 115, dy + 70),
    #                   (5, 5),
    #                  0, 0, 360, _black, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 185, dy + 70),
    #                   (5, 5),
    #                  0, 0, 360, _black, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 150, dy + 100),
    #                   (10, 5),
    #                  0, 0, 360, _black, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 150, dy + 150),
    #                   (40, 10),
    #                  0, 0, 360, _black, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 27, dy + 100),
    #                   (20, 35),
    #                  0, 0, 360, _white, -1, 8, 0)
    #    cv.Ellipse (image,
    #                   (dx + 273, dy + 100),
    #                   (20, 35),
    #                  0, 0, 360, _white, -1, 8, 0)

    # create window and display the original picture in it
    cv.NamedWindow ("image", 1)

    scale_factor = max(1.0*_SIZEW/_MSIZEW, 1.0*_SIZEH/_MSIZEH)
    to_display = cv.CreateImage ( (_SIZEW/scale_factor, _SIZEH/scale_factor), 8, 1)
    cv.Resize(image, to_display, cv.CV_INTER_CUBIC)

    cv.ShowImage ("image", to_display)

    # create the storage area
    storage = cv.CreateMemStorage (0)

    # find the contours
    contours = cv.FindContours(image,
                               storage,
                               cv.CV_RETR_TREE,
                               cv.CV_CHAIN_APPROX_SIMPLE,
                               (0,0))

    # comment this out if you do not want approximation
    contours = cv.ApproxPoly (contours,
                                storage,
                                cv.CV_POLY_APPROX_DP, 3, 1)

    # create the window for the contours
    cv.NamedWindow ("contours", 1)

    # create the trackbar, to enable the change of the displayed level
    cv.CreateTrackbar ("levels+4", "contours", 4, 7, on_trackbar)

    # call one time the callback, so we will have the 1st display done
    on_trackbar (_DEFAULT_LEVEL)

    # wait a key pressed to end
    cv.WaitKey (0)
