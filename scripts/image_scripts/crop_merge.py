import os, sys
import Image
import argparse

parser = argparse.ArgumentParser(description="Doing image stuf and shit")
parser.add_argument('--width', metavar='-w', type=int, help="width of output")
parser.add_argument('--height',metavar='-h', type=int, help="height of output")
parser.add_argument('--foreground', metavar='-f',help="path to foreground picture")

args = parser.parse_args()
WIDTH = args.width
HEIGHT = args.height
FOREGROUND = args.foreground
BACKGROUND = "./background/"
RESIZED = "./resized/"
RESULT ="./result/"
SIZE = WIDTH, HEIGHT


i = 0
for forfile in os.listdir(FOREGROUND):
    print("TEST 1")
    bigForeground = Image.open(FOREGROUND + forfile).convert("RGBA")
    #bigForeground.thumbnail(SIZE)
    #bigForeground.save(RESULT +"foreground.png")
    print(str(bigForeground.size))
    SIZE = bigForground.size
    k = 0
    for infile in os.listdir(RESIZED):
        k = k+1
        outfile = BACKGROUND + str(k)+ ".jpg"
        if infile != outfile:
            try:
                im = Image.open(RESIZED + infile)
                print ("opening file: " + RESIZED + infile)
                print("saving thumbnail: " + outfile)

                im.thumbnail(SIZE)
                im.save(outfile)
            except IOError:
                print "cannot create Thumbnail for '%s'" % infile


    for infile in os.listdir(BACKGROUND):
        i = i +1
        outfile = RESULT + str(i) + ".png"
        openfile = BACKGROUND + infile
        try:
            if infile != outfile:
                print("open : " + openfile )
                background = Image.open(openfile).convert("RGBA")
                foreground = Image.open(RESULT + "foreground.png").convert("RGBA")
                print("background size: " + str(background.size))
                print("foreground size: " + str(foreground.size))
                Image.alpha_composite(background,foreground).save(outfile)
        except IOError:
            print "cannot create image for '%s'" % infile
