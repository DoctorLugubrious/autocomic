#!/usr/bin/env python3
import matplotlib.image as img
import numpy as np
import sys
import os
from PIL import Image
import imghdr

# this file includes functions to split an image along reasonable split points.
# if a comic is too tall for a page, this will split it along reasonable lines.

#given an image, returns an array containing numbers between 0 and 1 describing how much
#variation there is on each row, with 0 being no variation and 1 being a lot of variation.
#channel is the image channel (R=0/G=1/B=2/A=3)
def getChannelVariation(channel, average):
	channel = np.copy(channel)

	uniqueFactor = getUniquePerRow(channel)

	channel.sort(axis=1)
	numOutliers = 2
	channel = channel[:,numOutliers: channel.shape[1] - numOutliers]

	deviations = np.std(channel, axis=1) / average

	return (0.1 * deviations + 0.9 * uniqueFactor)

def getUniquePerRow(channel):
	uniqueCounts = (np.abs(scaleArray(channel[:,1:]) - scaleArray(channel[:,:-1])) > 0.2).sum(axis=1)+1
	maxUnique = np.max(uniqueCounts)
	uniquePercentage = uniqueCounts / maxUnique

	return uniquePercentage

def getVariations(imageData):

	red_variation = getChannelVariation(imageData["r"], imageData["redMean"])
	green_variation = getChannelVariation(imageData["g"], imageData["greenMean"])
	blue_variation = getChannelVariation(imageData["b"], imageData["blueMean"])

	return (red_variation + green_variation + blue_variation) / 3

def scaleArray(array):
	if np.max(array) > 1:
		return array / 255
	return array

def scaleValue(mean):
	if (mean > 1):
		return mean / 255
	return mean

def getDifferentFactor(row, imageMean):
	imageMean = scaleValue(imageMean)
	rowMean = scaleValue(np.average(row))

	if (rowMean < imageMean):
		return (-rowMean / imageMean) + 1
	return ((rowMean - imageMean) / (1 - imageMean))


def getDifferentFactors(imageData):
	redFactor = np.apply_along_axis(getDifferentFactor, 1, imageData['r'], imageData['redMean'])
	greenFactor = np.apply_along_axis(getDifferentFactor, 1, imageData['g'], imageData['greenMean'])
	blueFactor = np.apply_along_axis(getDifferentFactor, 1, imageData['b'], imageData['blueMean'])

	return (redFactor + greenFactor + blueFactor) / 3

def getRowNearCenter(height):
	values = np.arange(height)
	return -(np.abs((2 / height) * values - 1) ** 3) + 1

def findBestSplitIndex(image, centerWeight):
	
	red =  np.copy(image[:,:,0])
	green =  np.copy(image[:,:,1])
	blue =  np.copy(image[:,:,2])

	redAverage = np.average(red)
	greenAverage = np.average(green)
	blueAverage = np.average(blue)

	imageData = {
		"r": red,
		"g": green,
		"b": blue,
		"redMean": redAverage,
		"greenMean": greenAverage,
		"blueMean": blueAverage,
	}

	solidColor = 1 - getVariations(imageData)
	differences = getDifferentFactors(imageData)
	nearCenter = getRowNearCenter(len(image))

	finalFitness = solidColor + differences + centerWeight * nearCenter
	#for i in [366, 831]:
	#	print("{0}: ({1}, {2}, {3})".format(i, solidColor[i], differences[i], nearCenter[i]))

	splitPoint = np.argmax(finalFitness)

	edgeOffset = 5
	if splitPoint == 0:
		splitPoint += edgeOffset
	elif splitPoint == len(finalFitness) - 1:
		splitPoint -= edgeOffset

	return splitPoint

def split(image, maxHeight, centerWeight=1):
	if (len(image) <= maxHeight):
		return [image]
	
	splitIndex = findBestSplitIndex(image, centerWeight)
	return split(image[:splitIndex], maxHeight) + split(image[splitIndex:], maxHeight)

# splits an image into multiple parts. Returns the filenames of the split version.
def splitFile(imageFile, maxHeight, axis=0):
	fileExtensions = ['jpg', 'gif', 'png']
	if not any(s in imageFile for s in fileExtensions):
		imageType = imghdr.what(imageFile)
		newName = imageFile + '.' + imageType
		os.rename(imageFile, newName)
		imageFile = newName
		
	imageInit = Image.open(imageFile).convert('RGB')
	imageInit.save(imageFile)
	image = None
	
	image = img.imread(imageFile)

	if axis is not 0:
		image = np.transpose(image, (1, 0, 2))
		images = split(image, maxHeight, 5)
	else:
		images = split(image, maxHeight)

	imageNames=[]

	num = 0
	for subImage in images:
		name = "images/" + os.path.splitext(os.path.basename(imageFile))[0] + "-" + str(num) + ".png"
		if axis is not 0:
			subImage = np.transpose(subImage, (1, 0, 2))
		img.imsave(name, subImage.copy(order='C'))
		imageNames.append(name)
		num += 1

	return imageNames

if __name__ == "__main__":
	splitFile(sys.argv[1], 1040, 0)