import os
import shutil
import sys
import xml.etree.ElementTree as ET


def check_args():
    args = sys.argv
    if len(args) != 2:
        raise OSError("Incorrect number of arguments, must be 2")
    return args[1]


def parse_file(config_file_path):
    try:
        tree = ET.parse(config_file_path)
    except ET.ParseError:
        print("Can't parse file")
        return
    root = tree.getroot()
    return root


def copy_files(root):
    for child in root:
        source_path = os.path.join(child.attrib['source_path'], child.attrib['file_name'])
        destination_path = os.path.join(child.attrib['destination_path'], child.attrib['file_name'])
        try:
            shutil.copyfile(source_path, destination_path)
        except PermissionError:
            print("Permission denied")
        except FileNotFoundError:
            print("No such file or directory or file path is invalid for current OS")


if __name__ == '__main__':
    try:
        file_path = check_args()
    except OSError as err:
        print(err)
        exit(1)
    else:
        root = parse_file(file_path)
        if root:
            copy_files(root)
