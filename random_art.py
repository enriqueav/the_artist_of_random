import argparse
from taor.randomgraph import random_image

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create a random image. By default is created in a tmp file'
                    ' and shown inmediatly. It can also be stored to a path using'
                    ' -i <image_path>.png'
    )
    parser.add_argument("-s", "--seed",
                        help="Initialize numpy with a given seed. "
                             "Same number will always create the same image.",
                        type=int)
    parser.add_argument("-i", "--image_path",
                        help="Name of the file to create. "
                             "Temporary file is used if -i is not specified.")
    parser.add_argument("-d", "--debug",
                        help="Enter DEBUG mode.",
                        action="store_true")
    parser.add_argument("-n", "--dont_show",
                        help="Do not open the image after creating it. "
                             "Only makes sense if -i is set.",
                        action="store_true")
    args = parser.parse_args()
    if args.dont_show and not args.image_path:
        print("Warning: --dont_show is set and --image_path is not set. "
              "Not doing anything meaningful")
    random_image(file_name=args.image_path,
                 show=not args.dont_show,
                 debug=args.debug,
                 seed=args.seed)
