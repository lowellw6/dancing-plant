"""
Sorts image files with the naming convention of the Azure camera.

'python imsort.py <DIR>' --> show current sort of files in directory <DIR>.

'python imsort.py -r <DIR>' --> rename <DIR> in sortable military time and store at <DIR>/military-time/
Example:
    before > Webcam Shot Date February 9 2021 Time 12.59.19 AM.jpg
    after  > Webcam Shot Date February 9 2021 Time 00.59.19.jpg

'python imsort -i <DIR>' --> rename <DIR> in indexed format according to CURRENT SORT and store at <DIR/indexed/
Example:
    before > Webcam Shot Date February 9 2021 Time 00.59.19.jpg
    after  > 0000.jpg
This assumes that image is the first taken. The following will be 0001.jpg, 0002.jpg, and so on.

Standard procedure is to use '-r' on the original directory. Then use '-i' on that military-time directory
to get a structure like <BASE>/military-time/indexed/.
"""

import argparse
import os
import glob
from shutil import copyfile



def get_file_sort(args):
    images = glob.glob(os.path.join(args.path, '*.png')) + \
             glob.glob(os.path.join(args.path, '*.jpg'))
             
    images = sorted(images)
    for imp in images:
        print(imp)


def index(args):
    images = glob.glob(os.path.join(args.path, '*.png')) + \
             glob.glob(os.path.join(args.path, '*.jpg'))
             
    images = sorted(images)
    
    out_path = os.path.join(args.path, "indexed")
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    scale = len(images)
    zpad = 0
    while scale >= 1:
        scale /= 10
        zpad += 1

    for i, imp in enumerate(images):
        ext = imp.split('.')[-1]
        out_name = str(i).zfill(zpad) + '.' + ext
        out_file = os.path.join(out_path, out_name)
        print(out_file)
        copyfile(imp, out_file)


def revise(args):
    images = glob.glob(os.path.join(args.path, '*.png')) + \
             glob.glob(os.path.join(args.path, '*.jpg'))
             
    out_path = os.path.join(args.path, "military-time")
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    for imp in images:
        tokens = imp.split(' ')
        phase, ext = tokens[-1].split('.')
        hour, mint, sec = tokens[-2].split('.')

        hour = int(hour)
        if phase == "PM" and hour != 12:
            hour += 12
        elif phase == "AM" and hour == 12:
            hour = 0
        if hour < 10:
            hour = '0' + str(hour)
        else:
            hour = str(hour)

        mtime = ".".join([hour, mint, sec])
        ext = "." + ext
        ntokens = tokens[:-2] + [mtime]
        nimp = " ".join(ntokens) + ext

        file_path = os.path.join(out_path, os.path.basename(nimp))
        print(file_path)
        copyfile(imp, file_path)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="dataset for evaluation")
    parser.add_argument("--revise", "-r", action="store_true", help="revise to sortable military time") 
    parser.add_argument("--index", "-i", action="store_true", help="index according to current sort")
    args = parser.parse_args()

    if args.revise:
        revise(args)

    if args.index:
        index(args)

    if not args.revise and not args.index:
        get_file_sort(args)
