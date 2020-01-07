from threading import Thread
import logging
import psutil
import time 
import os
from os.path import join

from .utils import get_module_dir, get_today_date

clear = lambda: os.system('clear') # on Linux System

class Monitor(Thread):
    def __init__(self, printing=True, logging=True, log_dirpath='default', log_level=logging.INFO):
        """ 
        Outputs information in the console by default.
        
        Options:
        ----------
            printing: enables printing info into console, default is True
            log_filepath: activate logging to file
            log_level: logging level for logging (inclusive)
        """
        self.run = False
        self.delay = 1

        # options
        self.printing = printing
        self.logging = logging
        self.log_dirpath = log_dirpath
        self.log_level = log_level

        if self.logging:
            self.setup_logging()
        

    def setup_logging(self):
        if self.log_dirpath == 'default':
            module_dir = get_module_dir()
            if module_dir:
                self.log_dirpath = join(module_dir, 'logs')
            else:
                raise ValueError(f'Error: unabled to setup default log dirpath. \
                    Please setup logging manually with `log_dirpath`.')
        
        date_time = get_today_date()
        log_filepath = join(self.log_dirpath, date_time + '.log')
        logging.basicConfig(filename=log_filepath,level=self.log_level)


    def start(self, delay=1):
        """ Start printing monitoring information.

        Options:
        --------
            delay: time in second before printing monitoring data
        """
        self.delay = delay
        self.run = True
        last_t = time.time() 
        while self.run:
            if time.time() - last_t >= self.delay:
                self.inspect()
                last_t = time.time()


    def stop(self):
        """ Stop printing monitoring information.
        """
        self.run = False


    def set_logging(logging, log_dirpath='default', log_level=logging.INFO):
        """
        logging: a boolean
        """
        self.logging = logging
        if self.logging:
            self.setup_logging(log_dirpath)


    def set_log_level(log_level):
        self.log_level = log_level
        if not self.logging:
            print(f'WARNING: setting log_level without logging being activated.')

    
    def set_printing(printing):
        """
        printing: a boolean
        """
        self.printing = printing

    
    def set_delay(delay):
        """ Set delay before printing information.
        
        Arguments:
        ----------
            delay: delay in seconds
        """
        self.delay = delay


    def system_info(self):
        """ Get system general infomation.
        """
        self.printer(f'\nGeneral information on the system:')
        nb_logic = psutil.cpu_count(logical=True)
        nb_physic = psutil.cpu_count(logical=False)
        self.printer(f'\tFound {nb_logic} logical cores for {nb_physic} physical CPUs')


    def inspect(self, clear_console=True):
        """ Print monitoring information.
        """
        if self.printing and clear_console:
            clear()

        self.print_memory_info()

        cpu_ntuple = psutil.cpu_times(percpu=False)
        self.print_info(cpu_ntuple, "CPU times")

        self.printer(f'Supplementary statistics')
        cpu_percent = psutil.cpu_percent(interval=None, percpu=False)
        self.printer(f'\tCPU usage: {cpu_percent}%')


    def print_memory_info(self):
        """ Custom printer for neatly printing memory info.
        """
        self.printer(f'Statistics for Virtual Memory')
        mem = psutil.virtual_memory()
        self.printer(f'\tUsed RAM: {mem.percent}%')
        self.printer(f'\tAvailable RAM: {mem.available /1024 /1024:.2f}/{mem.total /1024 /1024:.2f} MB')

        # from the docs at https://psutil.readthedocs.io/en/latest/
        THRESHOLD = 100 * 1024 * 1024  # 100MB
        if mem.available <= THRESHOLD:
            message = f'WARNING: Not much memory left.'
            if self.logging:
                logging.warn(message)
            if self.printing:
                print(message)
        
        swap = psutil.swap_memory()
        self.printer(f'\tSwap used: {swap.used /1024 /1024:.2f}/{swap.total /1024 /1024:.2f} MB ({swap.percent}%)')


    def print_info(self, ntuple, title=None):
        """ Generic printer without fancy explanation.
        Given a named tuple, print information contained in it.
        """
        if title:
            self.printer(f'Statistics for {title}')
        for key, val in ntuple._asdict().items():
            self.printer(f'\t{key}: {val}')


    def printer(self, string):
        """ Print data to console, log file or both.
        """
        if self.printing:
            print(string)
        if self.logging:
            logging.info(string)
