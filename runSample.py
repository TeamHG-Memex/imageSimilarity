
from PIL import Image
from glob import glob
# from imageSimilarity import imageSimilarity
from imageSimilarity import ImageSimilarity
from random import shuffle
if __name__ == '__main__':


    origImageFiles = glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/original/*")

    distImageFiles = []

    distImageFiles += glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/rotated/*")
    # distImageFiles += glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/resized/*")
    # distImageFiles += glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/cropped/*")
    # distImageFiles += glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/cropped_resized/*")
    # distImageFiles += glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/noisy/*")

    # shuffle(distImageFiles)

    # Can't use list comprehension because PIL doesn't close the image
    # pointers until the image data is used, or it is forced with a .load().
    # The loop below forces the files to be read and closed. Without this
    # Only about 100 images can be loaded before python will throw an exception
    # for having too many files open at the same time

    # origImages = [ Image.open(p) for p in origImageFiles ]
    # distImages = [ Image.open(p) for p in distImageFiles[:100] ]

    imgSim = ImageSimilarity(origImageFiles)



    distImages = []
    origImages = []

    for imgFile in origImageFiles:
        img = Image.open(imgFile)
        img.load()
        # img = img.convert("L")
        origImages.append( img )

    print("Originial images loaded")

    for imgFile in distImageFiles[:25]:
        img = Image.open(imgFile)
        # print(img.filename)
        img.load()
        # img = img.convert("L")
        distImages.append( img )

    print("Distorted images loaded")



    print("Found %d original images and %d distorted ones"%(len(origImages), len(distImages)))

    imgSim = ImageSimilarity( origImages )
    for count, distImg in enumerate(distImages):#int(len(distImages)/2)]:
        # print("\n\n\nTesting image:",distImg.filename.split("/")[-1])
        # print(100.0*float(count)/len(distImages))
        imgSim.scoreImage( distImg )
    print("Totals:",str(imgSim.totals))
    print("Hash Scores:",imgSim.hashScores)
