PPM Image Creator

#takes a number, a lowest possible number, and a highest possible number, and sets the number to the min or max if not in the range, and returns the number otherwise
def clampValueToRange(value, low, high):
    if value <= low:
        return int(low)
    elif value >= high:
        return int(high)
    else:
        return int(value)

#takes a line from a file, which is 5 numbers separated by a space, and returns a list of the first three, which are the rgb values of the pixel
def returnColor(line):
    lineList = line.split(" ")
    numList = []
    for num in lineList[:3]:
        numList.append(int(num))
    return numList

#takes a line from a file, which is 5 numbers separated by a space, and returns a list of the last two, which are the x and y coordinates of the pixel
def returnLocation(line):
    lineList = line.split(" ")
    numList = []
    for num in lineList[3:]:
        numList.append(int(num))
    return numList

#takes 4 ints and checks to make sure the x and y coordinates are within the allowed range of coordinates
def locationValid(x, width, y, height):
    return x >= 0 and y >= 0 and x < width and y < height

#takes the list returned by returnColor and turns it into a dictionary in the form {r:red, g:green, b:blue}
def convertPixel(color):
    colDict = {}
    red = clampValueToRange(color[0], 0, 255)
    colDict['r'] = red
    green = clampValueToRange(color[1], 0, 255)
    colDict['g'] = green
    blue = clampValueToRange(color[2], 0, 255)
    colDict['b'] = blue
    return colDict

#takes the x and y coordinates of the pixel, and the color dictionary from convertPixel, and returns a dictionary in the form {'pixel':color, 'x': x, 'y': y}
def positionPixel(x, y, color):
    return {'pixel':color, 'x': x, 'y': y, }

#takes a pixel dictionary returned from position pixel and a list of pixel dictionaries, and appends the pixel dictionary to the list of pixel dictionaries
def updateChangeList(pixel, pixelList):
    pixelList.append(pixel)

#takes a list of pixel dictionaries and a file, where each line in the file is a pixel’s rgb and xy coord values, converts the line to the pixel dictionary returned by position pixel, and adds each pixel dictionary to the list of pixel dictionaries
def readPixelFile(pixels, filename):
    with open(filename) as file:
        for line in file:
            line = line.rstrip('\n')
            color = convertPixel(returnColor(line))
            loc = returnLocation(line)
            pixel = positionPixel(loc[0], loc[1], color)
            updateChangeList(pixel, pixels)

#creates a picture (as a list of lists of dictionaries) of width x height with every pixel having every color value be zero.
def generateEmptyPicture(width, height):
    loloD = []
    for h in range(height):
        rowlst = []
        for w in range(width):
            rowlst.append(convertPixel([0,0,0]))
        loloD.append(rowlst)
    return loloD

#takes list of dictionaries from position pixel and list of lists of dictionaries, and changes all of the color values in image to the color values of the pixels, at their respective locations
def insertPixelList(pixels, image):
    for dic in pixels:
        if locationValid(int(dic['x']), len(image), int(dic['y']), len(image[0])):
            image[dic['x']][dic['y']]['r'] = dic['pixel']['r']
            image[dic['x']][dic['y']]['g'] = dic['pixel']['g']
            image[dic['x']][dic['y']]['b'] = dic['pixel']['b']

#takes image from generateEmptyPicture and the name of the file for the image to be written to, and writes out a P3 image file
def writePPM(image, filename):
    with open(filename, 'w') as f:
        f.write('P3\n' + str(len(image[0])) + ' ' + str(len(image)) + '\n255\n')
        for row in image:
            for dic in row:
                f.write(str(dic['r']) + ' ' + str(dic['g']) + ' ' + str(dic['b']) + '\n')

#mutates each pixel in pixels in the radius of the circle to have the color value specified
def addCircleToList(x, y, r, color, pixels):
    for xT in range(x-r, x+r+1):
        for yT in range(y-r, y+r+1):
            if (xT - x)**2 + (yT - y)**2 <= r**2:
                pixels.append(positionPixel(xT, yT, color))

#same as circle function but a rectangle instead
def addRectangleToList(x1, x2, y1, y2, pixel, pixels):
    if x1 > x2:
        temp = x1
        x1 = x2
        x2 = temp
    if y1 > y2:
        temp = y1
        y1 = y2
        y2 = temp
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            pixels.append(positionPixel(x, y, pixel))

#creates whatever I want
def yourPictureFunction():
    pic = generateEmptyPicture(200, 200)
    writePPM(pic, "C:/Users/prjr1/OneDrive/Documents/UB Assignments/milestone3.ppm")

    pixels = []
    addCircleToList(100, 100, 50, convertPixel([255, 100, 100]), pixels)
    addCircleToList(150, 100, 20, convertPixel([0, 0, 255]), pixels)
    addCircleToList(50, 100, 20, convertPixel([200, 200, 200]), pixels)
    addCircleToList(100, 50, 20, convertPixel([100, 100, 100]), pixels)
    addCircleToList(100, 150, 20, convertPixel([0, 255, 0]), pixels)
    addRectangleToList(0, 200, 95, 105, convertPixel([255, 255, 0]), pixels)
    addRectangleToList(95, 105, 0, 200, convertPixel([0, 255, 200]), pixels)
    insertPixelList(pixels, pic)
    writePPM(pic, "C:/Users/prjr1/OneDrive/Documents/UB Assignments/milestone3.ppm")
    
 

