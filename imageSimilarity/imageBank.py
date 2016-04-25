import PIL
import imagehash


class ImageBankItem(object):

    def __init__(self, image):
        self._raw = image
        self._pHash = self.pHashImage()
        self._avgHash = self.avgHashImage()
        self._dHash = self.dHashImage()

        self.name = self.getRootImageName()

    def __repr__(self):
        return self._pHash

    def __str__(self):
        return self.name

    def getName(self):
        return self.name

    def getPHash(self):
        return self._pHash

    def getAvgHash(self):
        return self._avgHash

    def getDHash(self):
        return self._dHash



    def getRootImageName(self):
        return '.'.join(self._raw.filename.split("/")[-1].split(".")[:-1])

    def pHashImage(self):
        return imagehash.phash( self._raw )

    def avgHashImage(self):
        return imagehash.average_hash( self._raw )

    def dHashImage(self):
        return imagehash.dhash( self._raw )





class ImageBank(object):


    def __init__(self, imageAddresses=[]):
        self._bank = [ ImageBankItem(self.loadImage(f)) for f in imageAddresses ]

    def getBank(self):
        return self._bank

    def loadImage(self, location):
        # print("opening:",location)
        img = PIL.Image.open(location)
        img.load()
        return img

    def downloadImage(self, url):
        """
        @url string url

        Download image data from a set URL
        """
        # TODO: cache data
        pass


    def getBank(self):
        return self._bank

    def addImageToBank(self, location):

        self._bank.append( ImageBankItem(self.loadImage(location)) )
        self._bank.sort()


    def addImageListToBank(self, imageLocations):

        self._bank += [ ImageBankItem(self.loadImage(location)) for location in imageLocations ]
        self._bank.sort()
