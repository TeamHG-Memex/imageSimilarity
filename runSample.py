
from PIL import Image
from glob import glob
from imageSimilarity import ImageSimilarity
from random import shuffle
if __name__ == '__main__':


    origImageFiles = glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/original/*")

    rotatedImageFiles = glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/rotated/*")
    resizedImageFiles = glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/resized/*")
    croppedImageFiles = glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/cropped/*")
    croppedResizedImageFiles = glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/cropped_resized/*")
    nosiyImageFiles = glob("/Users/hopperj/work/hyperionGray/catsImageDistortion/images/noisy/*")

    allDistortedImages = {
        "rotated":rotatedImageFiles,
        "resized":resizedImageFiles,
        "cropped":croppedImageFiles,
        "croppedResized":croppedResizedImageFiles,
        "nosiy":nosiyImageFiles,
    }

    imgSim = ImageSimilarity(origImageFiles)

    for name, distortedSet in allDistortedImages.items():
        imgSim.resetScores()
        for imgFile in distortedSet[:100]:
            imgSim.scoreImage( Image.open(imgFile) )

        print("\n\n--------------")
        print(name)
        print("Totals:",str(imgSim.getTotalScores()))
        print("Hash Scores:",imgSim.getIndividualHashScores())
        print("--------------")
