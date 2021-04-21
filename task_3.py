import logging
import os
import psutil
import time

from pathlib import Path

logging.basicConfig(level=logging.DEBUG, filename="test_case.log", format='%(asctime)s [%(levelname)s]: %(message)s')


class TestException(Exception):
    pass


class PrepException(TestException):
    pass


class RunException(TestException):
    pass


class CleanUpException(TestException):
    pass


class TestBase:

    def __init__(self, tc_id, name):
        self.tc_id = tc_id
        self.name = name

    def prep(self):
        pass

    def run(self):
        pass

    def clean_up(self):
        pass

    def execute(self):
        logging.info(f"Checking TestCase {self.name}, id {self.tc_id} started")

        try:
            logging.info(f"TestCase {self.name} module prep started")
            self.prep()
            logging.info("OK")
        except PrepException as err:
            logging.error(f"{err}")
            return

        try:
            logging.info(f"TestCase {self.name} module run started")
            self.run()
            logging.info("OK")
        except RunException as err:
            logging.error(f"{err}")

        try:
            logging.info(f"TestCase {self.name} module clean_up started")
            self.clean_up()
            logging.info("OK")
        except CleanUpException as err:
            logging.error(f"{err}")

        logging.info(f"Checking TestCase {self.name}, id {self.tc_id} completed")


class TestCase1(TestBase):
    def prep(self):
        unix_time = int(time.time())
        if unix_time % 2 != 0:
            raise PrepException("UNIX time is odd number, test case interrupted")

    def run(self):
        home_path = str(Path.home())
        full_dir_list = os.listdir(home_path)
        file_list = []
        for element in full_dir_list:
            if os.path.isfile(os.path.join(home_path, element)):
                file_list.append(element)
        if len(file_list) > 0:
            logging.info(file_list)
        else:
            raise RunException("Home directory is empty")


class TestCase2(TestBase):

    RAM_SIZE = 1024 * 1024 * 1024  # 1 GB
    FILE_SIZE = 1024 * 1024  # 1024 KB

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test')

    def prep(self):
        ram_info = psutil.virtual_memory()
        total_ram = ram_info.total
        if total_ram < self.RAM_SIZE:
            raise PrepException("Total RAM less than 1Gb")

    def run(self):
        with open(self.path, "bw") as test_file:
            try:
                test_file.write(os.urandom(self.FILE_SIZE))
            except Exception:
                raise RunException

    def clean_up(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        else:
            raise CleanUpException


def run_tests():
    test_cases = [TestCase1(1, 'FilesList'),
                  TestCase2(2, 'RandomFile')]
    for case in test_cases:
        case.execute()
        logging.info('--------------')


if __name__ == '__main__':
    run_tests()
