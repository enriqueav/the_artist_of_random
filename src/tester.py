import sys
import randomgraph

if __name__ == "__main__":
    debug = False
    image_path = None

    # check for correct argument size
    arguments = sys.argv
    if len(arguments) > 3:
        print('\033[91m' + 'Argument Error!\nUsage: python tester.py [img_path] [--debug]' + '\033[0m')
        exit(1)
    if '--debug' in arguments:
        print('\033[92mDebug mode is ON\033[0m')
        arguments.remove('--debug')
        debug = True

    if len(arguments) > 1:
        image_path = sys.argv[1]

    randomgraph.image(file_name=image_path, show=True, debug=debug)
