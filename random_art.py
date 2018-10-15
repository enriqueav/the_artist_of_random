import argparse
import time
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
    parser.add_argument("-q", "--quantity",
                        help="Quantity of images to generate. Default is 1."
                             "If set, --dont_show is set to True. If --seed is set, "
                             "this seed is used for the first image and then 1 is added "
                             "for each one of the following.",
                        type=int,
                        default=1)
    args = parser.parse_args()

    if args.dont_show and not args.image_path:
        print("Warning: --dont_show is set and --image_path is not set. "
              "Not doing anything meaningful")

    seed = args.seed
    image_path = args.image_path
    for i in range(args.quantity):
        if args.seed:
            seed = args.seed + i
            pre = args.image_path or "./taor/examples/" + str(int(time.time()))
            image_path = pre + "_seed%d" % seed
        elif args.quantity > 1:
            pre = args.image_path or "./taor/examples/" + str(int(time.time()))
            image_path = pre + "_number%d" % i

        random_image(file_name=image_path,
                     dont_show=args.dont_show or args.quantity>1,
                     debug=args.debug,
                     seed=seed)
