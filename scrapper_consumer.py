from utils.scrapper import run
from multiprocessing import freeze_support
from utils.logger import logging

if __name__ == '__main__':
    run()
    freeze_support()
    logging("debug", 'Scores longpool запущен!')



