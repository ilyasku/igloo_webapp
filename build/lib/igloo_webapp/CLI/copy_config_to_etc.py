import shutil
import sys
from igloo_webapp.config_io import PATH_TO_CONFIG, ROOT_PATH_TO_CONFIG

def main():
    if len(sys.argv) != 2:
        print("Requires one argument: path to config file (default location is ~/.config/igloo_webapp.json)")
        return 1
    path_to_config = sys.argv[1]
    shutil.move(path_to_config, ROOT_PATH_TO_CONFIG)

if __name__ == "__main__":
    main()
