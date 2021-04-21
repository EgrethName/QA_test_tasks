from pathlib import Path
import logging
import os
import psutil
import sys
import time

logging.basicConfig(level=logging.DEBUG, filename="test_case.log", format='%(asctime)s %(levelname)s:%(message)s')


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
            logging.info("TestCase(number) module prep started")
            self.prep()
            logging.info("OK")
        except PrepException:
            logging.error("FAIL")

        try:
            logging.info("TestCase(number) module run started")
            self.run()
            logging.info("OK")
        except RunException:
            logging.error("FAIL")

        try:
            logging.info("TestCase(number) module clean_up started")
            self.clean_up()
            logging.info("OK")
        except CleanUpException:
            logging.error("FAIL")

        logging.info(f"Checking TestCase {self.name}, id {self.tc_id} completed")


class TestCase1(TestBase):
    def prep(self):
        unix_time = int(time.time())
        if unix_time % 2 != 0:
            raise PrepException
        return True

    def run(self):
        home_path = str(Path.home())
        full_dir_list = os.listdir(home_path)
        file_list = []
        for element in full_dir_list:
            if os.path.isfile(os.path.join(home_path, element)):
                file_list.append(element)
        if len(file_list) > 0:
            return file_list
        else:
            raise RunException

    def clean_up(self):
        pass

    def execute(self):
        logging.info("Checking TestCase1 started")

        logging.info("TestCase1 module prep started")
        try:
            self.prep()
            logging.info("OK")
        except PrepException:
            logging.error("FAIL")
            return

        logging.info("TestCase1 module run started")
        try:
            file_list = self.run()
            logging.info(file_list)
            logging.info("OK")
        except RunException:
            logging.info("File's list is empty")
            logging.error("FAIL")

        logging.info("TestCase1 module clean_up started")
        try:
            logging.info("SKIPPED")
        except CleanUpException:
            pass

        logging.info("Checking TestCase1 completed")


class TestCase2(TestBase):
    def prep(self):
        ram_info = psutil.virtual_memory()
        total_ram = ram_info.total
        if total_ram < 1073741824:
            raise PrepException

    def run(self):
        with open("test", "bw") as test_file:
            try:
                test_file.write(os.urandom(1048576))
            except Exception:
                raise RunException

    def clean_up(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test')
        if path:
            os.remove(path)
        else:
            raise CleanUpException

    def execute(self):
        logging.info("Checking TestCase2 started")

        logging.info("TestCase2 module prep started")
        try:
            self.prep()
            logging.info("OK")
        except PrepException:
            logging.error("FAIL")
            return

        logging.info("TestCase2 module run started")
        try:
            self.run()
            logging.info("OK")
        except RunException:
            logging.error("FAIL")

        logging.info("TestCase2 module clean_up started")
        try:
            self.clean_up()
            logging.info("OK")
        except CleanUpException:
            logging.error("FAIL")

        logging.info("Checking TestCase2 completed")


a = TestCase1(1, 'FilesList')
b = TestCase2(2, 'RandomFile')
a.execute()
b.execute()
