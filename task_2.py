import hashlib
import os
import sys


BUF_SIZE = 65536

hash_methods = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha256': hashlib.sha256,
}

input_file_path = sys.argv[1]
files_dir = sys.argv[2]


def file_handler():
    with open(input_file_path, "r", encoding="UTF-8") as total_file:
        for line in total_file:
            try:
                file_name, hash_name, checksum = line.split()
            except ValueError:
                print(f"Fail to parse line {line}")
                continue
            result = calculate_checksum(file_name, hash_name, checksum)
            print(f"{file_name} {result}")


def calculate_checksum(file_name, hash_alg, checksum):
    hash_method = hash_methods.get(hash_alg.lower())

    if not hash_method:
        return f"{hash_alg} is incorrect hash method"

    hasher = hash_method()

    path = os.path.join(files_dir, file_name)
    if not os.path.exists(path):
        return "NOT FOUND"
    with open(path, "rb") as calculated_file:
        while True:
            data = calculated_file.read(BUF_SIZE)
            if not data:
                break
            hasher.update(data)

    return "OK" if hasher.hexdigest() == checksum else "FAIL"


if __name__ == '__main__':
    file_handler()
