import imagehash
from collections import namedtuple
import PIL
from PIL import Image, ImageFilter
from ssim import compute_ssim
import os
import operator
import cv2
import numpy as np

import numpy
import scipy

from .imageBank import ImageBank





class ImageSimilarity(object):
    """
    Given an image, score it based on its similarity to a known set
    of images using ssim, diff hash, average hash, and phash
    """
    def __init__(self, imageAddresses=[]):

        self._imageBank = ImageBank(imageAddresses)

        exit(0)
        self.scores = { self.getRootImageName(img.filename):0 for img in self._imageBank }

        # These are used only to record the individual scores from each algorithm.
        # These are indended to only be used for testing. In production only the
        # self.scores dictionary should be used, and updated on the fly.
        self.ssimScores = { img.name:0 for img in self._imageBank }
        self.avgHashScores = { self.getRootImageName(img.filename):0 for img in self._imageBank }
        self.pHashScores = { self.getRootImageName(img.filename):0 for img in self._imageBank }
        self.dHashScores = { self.getRootImageName(img.filename):0 for img in self._imageBank }

        self.totals = [0,0]
        self.hashScores = { 'ssim':0, 'avg':0, "p":0, "d":0, "imgMatch":0 }

        self.dHashWeight = 0.3018
        self.ssimWeight = 0.2308
        self.pHashWeight = 0.2262
        self.avgHashWeight = 0.2544


        self.resizedScoreThreshold = 0.8
        self.croppedScoreThreshold = 0.9
        self.classifiedScoreThreshold = 0.95




    def addImageToBank(self, location):
        self._imageBank.addImageToBank(location)

    def addImageListToBank(self, imageLocations):
        self._imageBank.addImageListToBank(location)

    def scoreImageFromURL(self, url):
        """
        @url string url

        This function allows users to provide either a URL instead of an
        image file.
        """
        img = self.downloadImage(url)
        return self.scoreImage(img)




    def resizedScore(self, image):
        """
        @image is a PIL Image object

        Returns a guess of what image is best matched, along with a score
        """

        avgHashedImage = imagehash.average_hash( image )
        pHashedImage = imagehash.phash( image )
        dHashedImage = imagehash.dhash( image )

        avgHashScore = ["",0]
        for img in self._imageBank:
            self.avgHashScores[ self.getRootImageName(img.filename) ] =  1.0 - ( (avgHashedImage - self.hashCache[ img.filename ]['avgHash'] ) / 64.0 )

            # Keep track of the highest score
            if self.avgHashScores[ self.getRootImageName(img.filename) ] > avgHashScore[1]:
                avgHashScore = [
                    self.getRootImageName(img.filename),
                    self.avgHashScores[ self.getRootImageName(img.filename) ]
                ]
        # Return with the best guess
        return avgHashScore

    def croppedScore(self, image):
        """
        @image is a PIL Image object

        Returns a guess of what image is best matched, along with a score
        """
        result = ["",0]
        try:
            for i in rane(1):
                image = Image.fromarray( cv2.medianBlur( np.array(image), 25 ) )
        except:
            pass

        imageArray = np.array(image.convert("L"))
        for img in self._imageBank:
            if any( [a > b for a,b in zip(image.size, img.size)] ):
                # If the image being searched is larger than the unknown image
                # in either dimension, it can't be the correct one.
                continue

            mt = cv2.matchTemplate(
                np.array(img.convert("L")),
                imageArray, cv2.TM_CCORR_NORMED
            )
            # Need max value for TM_CCORR_NORMED
            # returns: minVal, maxVal, minLoc, maxLoc
            loc = cv2.minMaxLoc( mt )[1]
            if loc > result[1]:
                result = [self.getRootImageName(img.filename), loc]
        return result


    def noiseScore(self, image):
        blurVal = 0.25
        kernel = np.ones((5,5), np.float32)/25
        # image = Image.fromarray( cv2.blur( np.array(image), (25,25)) )
        try:
            for i in rane(1):
                image = Image.fromarray( cv2.medianBlur( np.array(image), 25 ) )
        except:
            pass

        # self._imageBank = [ Image.fromarray(cv2.filter2D( np.array(img), -1, kernel )) for img in self._imageBank ]


        avgHashedImage = imagehash.average_hash( image )
        pHashedImage = imagehash.phash( image )
        dHashedImage = imagehash.dhash( image )

        result = ["", 0]


        for img in self._imageBank:

            # score = compute_ssim( image, img )

            # score =  1.0 - ( (avgHashedImage - imagehash.average_hash( self.hack[img.filename] )) / 64.0 )

            # score =  1.0 - ( (pHashedImage - imagehash.phash( self.hack[img.filename] )) / 64.0 )

            score =  1.0 - ( (dHashedImage - imagehash.dhash( self.hack[img.filename] )) / 64.0 )

            if score > result[1]:
                result = [
                    self.getRootImageName(img.filename),
                    score
                ]


        # results = sorted( self.scores.items(), key=operator.itemgetter(1), reverse=True )[0]
        # print( "Best guess:",results )
        return result



    def trackAccuracy(self, image, result):
        """
        @image should be a PIL Image
        @results should be
        """
        correct = result[0] in image.filename
        self.totals[ int(correct) ] += 1
        if not correct:
            print("wrong --> ",self.getRootImageName(image.filename), result)


    def scoreImage(self, image=None):
        """
        @image should be a PIL Image object

        This function will score the similarity to known images using several
        techniques.
        """

        # Score using the resized method
        # result = self.resizedScore( image )
        # if result[1] <= self.resizedScoreThreshold:
        #     # Score was not high enough to consider this our guess
        #     # check for cropping
        #     result = self.croppedScore( image )
        #     if result[1] <= self.croppedScoreThreshold:
        #         result = self.noiseScore(image)
        #

        # result = self.noiseScore( image )
        result = self.croppedScore( image )
        if result[1] <= self.classifiedScoreThreshold:
            image = image.transpose(Image.ROTATE_90)
            result = self.croppedScore( image )
            if result[1] <= self.classifiedScoreThreshold:
                image = image.transpose(Image.ROTATE_180)
                result = self.croppedScore( image )
        # result = self.resizedScore( image )

        self.trackAccuracy(image, result)
        return

        avgHashedImage = imagehash.average_hash( image )
        pHashedImage = imagehash.phash( image )
        dHashedImage = imagehash.dhash( image )

        for img in self._imageBank:
            self.ssimScores[ self.getRootImageName(img.filename) ] = compute_ssim( image, img )

            self.avgHashScores[ self.getRootImageName(img.filename) ] =  1.0 - ( (avgHashedImage - imagehash.average_hash( img )) / 64.0 )
            # print( 1.0 - (avgHashedImage - imagehash.average_hash( img )) / 64.0 )

            self.pHashScores[ self.getRootImageName(img.filename) ] =  1.0 - ( (pHashedImage - imagehash.phash( img )) / 64.0 )

            self.dHashScores[ self.getRootImageName(img.filename) ] =  1.0 - ( (dHashedImage - imagehash.dhash( img )) / 64.0 )

            self.scores[ self.getRootImageName(img.filename) ] = \
                self.ssimWeight * self.ssimScores[ self.getRootImageName(img.filename) ] + \
                self.avgHashWeight * self.avgHashScores[ self.getRootImageName(img.filename) ] + \
                self.pHashWeight * self.pHashScores[ self.getRootImageName(img.filename) ] + \
                self.dHashWeight * self.dHashScores[ self.getRootImageName(img.filename) ]


        results = sorted( self.scores.items(), key=operator.itemgetter(1), reverse=True )[0]
        print( "Best guess:",results )



        # # Compute SSIM scores
        #
        # for img in self._imageBank:
        #     self.ssimScores[ self.getRootImageName(img.filename) ] = compute_ssim( image, img )
        #
        ssimHashScore = sorted( self.ssimScores.items(), key=operator.itemgetter(1), reverse=True )[0]
        self.hashScores['ssim'] += int(ssimHashScore[0] in image.filename)
        #
        #
        # imgHash = imagehash.average_hash( image )
        # for img in self._imageBank:
        #     self.avgHashScores[ self.getRootImageName(img.filename) ] =  imgHash - imagehash.average_hash( img )# self.hashCache[img.filename]['avgHash']
        #
        avgHashScore = sorted( self.avgHashScores.items(), key=operator.itemgetter(1), reverse=True )[0]
        self.hashScores['avg'] += int(avgHashScore[0] in image.filename)
        #
        #
        #
        #
        # imgHash = imagehash.phash( image )
        # for img in self._imageBank:
        #     self.pHashScores[ self.getRootImageName(img.filename) ] =  imgHash - imagehash.phash( img )# self.hashCache[img.filename]['pHash']#
        #
        pHashScore = sorted( self.pHashScores.items(), key=operator.itemgetter(1), reverse=True )[0]
        self.hashScores['p'] += int(pHashScore[0] in image.filename)
        #
        #
        #
        #
        #
        # imgHash = imagehash.dhash( image )
        # for img in self._imageBank:
        #     self.dHashScores[ self.getRootImageName(img.filename) ] =  imgHash - imagehash.dhash( img )# self.hashCache[img.filename]['dHash']
        #
        dHashScore = sorted( self.dHashScores.items(), key=operator.itemgetter(1), reverse=True )[0]
        self.hashScores['d'] += int(dHashScore[0] in image.filename)



        guess = "-1" #results[0]
        # Totals: [51, 49]
        # Hash Scores: {'ssim': 39, 'avg': 46, 'imgMatch': 0, 'p': 33, 'd': 49}
        ssimThresh = 0.8
        avgThresh = 0.8
        pThresh = 0.8
        dThresh = 0.8
        if results[1] >= ssimThresh * avgThresh * pThresh * dThresh:
            guess = results[0]
        elif dHashScore[1] >= dThresh:
            guess = dHashScore[0]

        elif avgHashScore[1] >= avgThresh:
            guess = avgHashScore[0]

        elif ssimHashScore[1] >= ssimThresh:
            guess = ssimHashScore[0]

        elif pHashScore[1] >= pThresh:
            guess = pHashScore[0]




        # correct = ssimScore in image.filename or avgHashScore in image.filename or pHashScore in image.filename or dHashScore in image.filename
        correct = guess in image.filename
        # print(correct)
        self.totals[ int(correct) ] += 1

        if not correct:
            print(dHashScore)
            print(avgHashScore)
            print(ssimHashScore)
            print(pHashScore)
