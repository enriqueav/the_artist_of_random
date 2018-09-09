import sys
import randomgraph

if __name__ == "__main__":
    debug = False
    # check for correct argument size
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        print('\033[91m' + 'Argument Error!\nUsage: python tester.py <img_path> [--debug]' + '\033[0m')
        exit(1)
    if len(sys.argv) == 3 and sys.argv[2] == '--debug':
        print('\033[92mDebug mode is ON\033[0m')
        debug = True

    image_path = sys.argv[1]
    randomgraph.image(image_path, debug=debug)