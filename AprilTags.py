#April Tag Software
import copy
import numpy as np
import cv2 as cv
import math as m
from pupil_apriltags import Detector
import os

RED = '\033[0;31m'


def Main():
    print(RED + "")
    #value of input device
    inputDevice = 0
    inputWidth = 1080
    inputHeight = 1920
    
    #Family of april tags being detected
    families = 'tag16h5'
    #sensitivity for detection
    nthreads = 30
    #low resolution input help
    quadDecimate = 0.0
    #blurring for easier processing in noisy images
    quadSigma = 4
    #edges snap to gradiants
    refineEdges = 3
    #helps with strange lighting
    decodeSharpening = -0.85
    debug = 0 
    
    #set video capture
    input = cv.VideoCapture(inputDevice)
    #set frame
    input.set(cv.CAP_PROP_FRAME_HEIGHT, inputHeight)
    input.set(cv.CAP_PROP_FRAME_WIDTH, inputWidth)
    
    #set detector settings
    at_detector = Detector(
    families = families,
    nthreads = nthreads,
    quad_decimate = quadDecimate,
    quad_sigma = quadSigma,
    refine_edges = refineEdges,
    decode_sharpening = decodeSharpening,
    debug = debug,
    )
    
    
    while True:
        #ret is bool saying if input can be read
        #image is set to input
        ret, image = input.read()
        if not ret:
            print("Input can not be accessed")
            break
        #make copy of image
        debugImage = copy.deepcopy(image)
        
        #convert image to black and white
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        tags = at_detector.detect(
        image,
        estimate_tag_pose= False,
        camera_params =None,
        tag_size=None,
        )
        
        #add tags to shown image

        debugImage = drawTags(debugImage, tags)
   
        key = cv.waitKey(1)
        if key == 27:  
            break
        
        
        cv.imshow('april tags', debugImage)
    input.release()
    cv.destroyAllWindows()


def drawTags(image, tags,):
    for tag in tags:
        #set variables of tags 
        tagID = tag.tag_id
        center = tag.center
        corners = tag.corners
        cross = 460, 260
            
        focalLength = 859.5
        realWidth = 15.0
        
        #define corners and center of tag
        center = (int(center[0]), int(center[1]))
        corner1 = (int(corners[0][0]), int(corners[0][1]))
        corner2 = (int(corners[1][0]), int(corners[1][1]))
        corner3 = (int(corners[2][0]), int(corners[2][1]))
        corner4 = (int(corners[3][0]), int(corners[3][1]))
        
        #define the center of the top and bottom of tag
        detx1 = (corner2[0] + corner3[0])/2
        detx2 = (corner3[0] + corner4[0])/2
        dety1 = (corner2[1] + corner1[1])/2
        dety2 = (corner3[1] + corner4[1])/2
        dett = (0, int(dety1))
        detb = (0, int(dety2))
        
        detx1s = (corner2[0] + corner3[0])/2
        detx2s = (corner3[0] + corner4[0])/2
        dety1s = (corner2[1] + corner3[1])/2
        dety2s = (corner3[1] + corner4[1])/2
        
        side1x = abs((corner1[0] - corner3[0]))
        side1y = abs((corner3[1] - corner4[1]))
        side2x = abs((corner3[0] - corner4[0]))
        side2y = abs((corner3[1] - corner4[1]))

        y = abs((dety1s - dety2s))
        x = abs((detx1s - detx2s))

        cv.circle(image, (cross[0], cross[1]), 5, (0, 255, 0), 5)

        #use distance formula on top and botom of tag
        if 400 > abs((dety1 - dety2)) > 25:
            d = m.dist(dett, detb)
        else:
            d = -1
        

        #make loop for calculating distance when possible
        if d > 0:
            #use distance formula to use pixel width, real width and focal length to find distance
            cv.circle(image, (center[0], center[1]), 5, (255, 0, 255), 2)
            
            xd = abs((cross[0] - center[0]))
            yd = abs((cross[1] - center[1]))
            print("xd: " + str(xd))
            print("yd: " + str(yd))
            if x > xd > 0 and y > yd > 0:
                aligned = 1
            elif x > xd > 0:
                aligned = 3
            elif y > yd > 0:
                aligned = 4
            else:
                aligned = 2
                
            cv.line(image, (cross[0], cross[1]), 
                    (center[0], center[1]), (255, 255, 0,), 2)
            
            if aligned == 2:
                cv.line(image, (corner1[0], corner1[1]),
                        (corner2[0], corner2[1]), (255, 0, 0), 2)
                cv.line(image, (corner2[0], corner2[1]),
                        (corner3[0], corner3[1]), (255, 0, 0), 2)
                cv.line(image, (corner3[0], corner3[1]),
                        (corner4[0], corner4[1]), (0, 0, 255), 2)
                cv.line(image, (corner4[0], corner4[1]),
                        (corner1[0], corner1[1]), (0, 0, 255), 2)
                distance = (realWidth * focalLength) / d
                
            if aligned == 1:
                cv.line(image, (corner1[0], corner1[1]),
                        (corner2[0], corner2[1]), (0, 255, 0), 2)
                cv.line(image, (corner2[0], corner2[1]),
                        (corner3[0], corner3[1]), (0, 255, 0), 2)
                cv.line(image, (corner3[0], corner3[1]),
                        (corner4[0], corner4[1]), (0, 255, 0), 2)
                cv.line(image, (corner4[0], corner4[1]),
                        (corner1[0], corner1[1]), (0, 255, 0), 2)
                cv.putText(image, "ALIGNED", (0, 200),
                           cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2, cv.LINE_AA)
                distance = (realWidth * focalLength) / d
                
            if aligned == 3:
                cv.line(image, (corner1[0], corner1[1]),
                        (corner2[0], corner2[1]), (255, 0, 0), 2)
                cv.line(image, (corner2[0], corner2[1]),
                        (corner3[0], corner3[1]), (0, 255, 0), 2)
                cv.line(image, (corner3[0], corner3[1]),
                        (corner4[0], corner4[1]), (0, 0, 255), 2)
                cv.line(image, (corner4[0], corner4[1]),
                        (corner1[0], corner1[1]), (0, 255, 0), 2)
                cv.putText(image, "ALIGNED HORIZONTAL", (0, 200),
                        cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0 , 0), 2, cv.LINE_AA)
                distance = (realWidth * focalLength) / d
                
            if aligned == 4:
                cv.line(image, (corner1[0], corner1[1]),
                        (corner2[0], corner2[1]), (0, 255, 0), 2)
                cv.line(image, (corner2[0], corner2[1]),
                        (corner3[0], corner3[1]), (0, 0, 255), 2)
                cv.line(image, (corner3[0], corner3[1]),
                        (corner4[0], corner4[1]), (0, 255, 0), 2)
                cv.line(image, (corner4[0], corner4[1]),
                        (corner1[0], corner1[1]), (0, 0, 255), 2)
                cv.putText(image, "ALIGNED VERTICAL", (0, 200),
                        cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0 , 0), 2, cv.LINE_AA)
                distance = (realWidth * focalLength) / d

            #make distane that is printed to screen rounded
            dishow = round(distance)
            #show distance from tags 
            cv.putText(image, str(dishow), (center[0] - 80, center[1] - 20),
                  cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 255), 2, cv.LINE_AA)
            cv.putText(image, ("cm"), (center[0] - 80, center[1] - 0),
                  cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 255), 2, cv.LINE_AA)
            #show exact measurement in console
            cv.putText(image, str(tagID), (center[0] - 10, center[1] - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 255), 2, cv.LINE_AA)
            #print(distance)
        else:
            break
        #put tag id on tags
        
    return image
    return distance 
    
Main()