import cv2
import os

def extractFrames(pathIn, pathOut):
    if not os.path.exists(pathOut):
        os.mkdir(pathOut)

    cap = cv2.VideoCapture(pathIn)
    count = 0

    while (cap.isOpened()):

        ret, frame = cap.read()

        if ret == True:
            cv2.imwrite(os.path.join(pathOut, "frame_{:06d}.jpg".format(count)), frame)
            count += 1
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    extractFrames('video.mp4', 'outputdir')

if __name__=="__main__":
    main()
