import imagehash
import PIL
from PIL import Image
import operator
# from bkstring.bktree import BkTree

from .imageBank import ImageBank, ImageBankItem


class ImageSimilarity(object):
    """
    Given an image, score it based on its similarity to a known set
    of images using ssim, diff hash, average hash, and phash
    """

    def __init__(self, imageAddresses=[], debug=0):

        self._imageBank = ImageBank(imageAddresses)

        self.resetScores()

        self.DEBUG = debug

    def resetScores(self):
        self._scores = {
            'avgHash': {'name': "", "score": 0},
            'pHash': {'name': "", "score": 0},
            'dHash': {'name': "", "score": 0},
        }

        # wrong, right
        self._totals = [0, 0]
        self._individualHashScores = {'avgHash': 0, "pHash": 0, "dHash": 0}

        self.__totalsCounter = 0

    def getIndividualHashScores(self):
        return [(k, v / float(self.__totalsCounter)) for k, v in sorted(self._individualHashScores.items(), key=operator.itemgetter(1), reverse=True)]

    def getTotalScores(self):
        return self._totals, self._totals[1] / float(sum(self._totals))

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

    def trackAccuracy(self, image):
        """
        @image should be an ImageBankItem object
        """
        # sorted( self.dHashScores.items(), key=operator.itemgetter(1), reverse=True )
        correct = False
        for k in self._scores.keys():
            if self._scores[k]['name'] in image.getName():
                self._individualHashScores[k] += 1
                correct = True
        self._totals[int(correct)] += 1
        if not correct and self.DEBUG:
            print("wrong --> ", image.getName(), [self._scores[k]['name'] for k in self._scores.keys()])

    def scoreImage(self, image=None):
        """
        @image should be a PIL Image object

        This function will score the similarity to known images using several
        techniques.
        """
        # TODO: If we made an ImageBankItem object with this,
        # we could build a diff function that would return all the
        # results at once.
        image = ImageBankItem(image)

        # TODO: Make this faster. Don't check every single image. BK-tree? Log search sorted list?

        aDiff = self._aTree.search(image.getAvgHash(), 10)
        pDiff = self._aTree.search(image.getPHash(), 10)
        dDiff = self._aTree.search(image.getDHash(), 10)

        print("aDiff:", aDiff)
        print("pDiff:", pDiff)
        print("dDiff:", dDiff)

        #
        # for img in self._imageBank.getBank():
        #     score = 1.0 - ( (image.getAvgHash() - img.getAvgHash()) / 64.0 )
        #     if score >= self._scores['avgHash']['score']:
        #         self._scores['avgHash'] = {
        #             'name':img.getName(),
        #             'score':score,
        #         }
        #
        #     score = 1.0 - ( (image.getPHash() - img.getPHash()) / 64.0 )
        #     if score >= self._scores['pHash']['score']:
        #         self._scores['pHash'] = {
        #             'name':img.getName(),
        #             'score':score,
        #         }
        #
        #     score = 1.0 - ( (image.getDHash() - img.getDHash()) / 64.0 )
        #     if score >= self._scores['dHash']['score']:
        #         self._scores['dHash'] = {
        #             'name':img.getName(),
        #             'score':score,
        #         }

        self.__totalsCounter += 1
        self.trackAccuracy(image)
