from threading import Thread
import logging
import psutil
import time 
import os
from os import mkdir
from os.path import join, isdir

from .utils import get_module_dir, get_today_date

clear = lambda: os.system('clear') # on Linux System

class Monitor(Thread):
    def __init__(self, enable_print=True, enable_log=True, log_dirpath='default', log_filename='default', log_level=logging.INFO, save_data=False):
        """ 
        Outputs information in the console by default.
        
        Options:
        ----------
            enable_print: enables printing info into console, default is True
            log_filepath: activate logging to file
            log_level: logging level for logging (inclusive)
        """
        super(Monitor, self).__init__()

        self.running = False
        self.delay = 1
        if save_data:
            self.pile = list('Initialization.')
        else:
            self.pile = None

        # options
        self.enable_print = enable_print
        # if self.enable_print:
        #     self.clear_console = True
        self.enable_log = enable_log
        self.log_dirpath = log_dirpath
        self.log_filename = log_filename
        self.log_level = log_level

        if self.enable_log:
            self.setup_logging()
        

    def setup_logging(self):
        if self.log_dirpath == 'default':
            module_dir = get_module_dir()
            if module_dir:
                self.log_dirpath = join(module_dir, 'logs')
                if isdir(module_dir) and not isdir(self.log_dirpath):
                    mkdir(self.log_dirpath)
            else:
                raise ValueError(f'Error: unabled to setup default log dirpath. \
                    Please setup logging manually with `log_dirpath`.')
        
        if self.log_filename == 'default':
            date_time = get_today_date()
            self.log_filename = date_time + '.log'

        log_filepath = join(self.log_dirpath, self.log_filename)
        logging.basicConfig(filename=log_filepath, level=self.log_level)


    def run(self):
        """ Start printing monitoring information.

        Options:
        --------
            delay: time in second before printing monitoring data
        """
        print(f'\nMonitoring successfully started...')
        self.running = True
        self.inspect()  # do a first inspection at start time
        last_t = time.time() 
        while self.running:
            if time.time() - last_t >= self.delay:
                self.inspect()
                last_t = time.time()


    def stop(self):
        """ Stop printing monitoring information.
        """
        self.running = False
        if self.enable_log:
            print(f'\nMonitoring log available as {self.log_filename} at {self.log_dirpath}')

        if self.pile:
            return self.get_pile()
        else:
            print(f'no pile found')


    def enable_clearconsole(self):
        self.clear_console = True


    def disable_clearconsole(self):
        self.clear_console = False


    def set_logging(self, enable_log, log_dirpath='default', log_level=logging.INFO):
        """
        logging: a boolean
        """
        self.enable_log = enable_log
        if self.enable_log:
            self.setup_logging(log_dirpath)


    def set_log_level(self, log_level):
        self.log_level = log_level
        if not self.enable_log:
            print(f'WARNING: setting log_level without logging being activated.')

    
    def set_printing(self, enable_print):
        """
        enable_print: a boolean
        """
        self.enable_print = enable_print

    
    def set_delay(self, delay):
        """ Set delay before printing information.
        
        Arguments:
        ----------
            delay: delay in seconds
        """
        self.delay = delay


    def system_info(self):
        """ Get system general infomation.
        """
        self.printer(f'\n-----------------')
        self.printer(f'General information on the system')
        self.printer(f'-----------------')

        nb_logic = psutil.cpu_count(logical=True)
        nb_physic = psutil.cpu_count(logical=False)
        self.printer(f'Found {nb_logic} logical cores for {nb_physic} physical CPUs')


    def inspect(self):
        """ Print monitoring information.
        """
        if self.enable_print and self.clear_console:
            clear()

        self.printer(f'\n-----------------')
        self.printer(f'System status')
        self.printer(f'-----------------')

        self.print_memory_info()

        cpu_ntuple = psutil.cpu_times(percpu=False)
        self.print_info(cpu_ntuple, "CPU times")

        self.printer(f'\nSupplementary statistics')
        cpu_percent = psutil.cpu_percent(interval=None, percpu=False)
        self.printer(f'\tCPU usage: {cpu_percent}%')


    def print_memory_info(self):
        """ Custom printer for neatly printing memory info.
        """
        self.printer(f'\nStatistics for Virtual Memory')
        mem = psutil.virtual_memory()
        self.printer(f'\tUsed RAM: {mem.percent}%')
        self.printer(f'\tAvailable RAM: {mem.available /1024 /1024:.2f}/{mem.total /1024 /1024:.2f} MB')

        # from the docs at https://psutil.readthedocs.io/en/latest/
        THRESHOLD = 100 * 1024 * 1024  # 100MB
        if mem.available <= THRESHOLD:
            message = f'WARNING: Not much memory left.'
            if self.enable_log:
                logging.warn(message)
            if self.enable_print:
                print(message)
        
        swap = psutil.swap_memory()
        self.printer(f'\tSwap used: {swap.used /1024 /1024:.2f}/{swap.total /1024 /1024:.2f} MB ({swap.percent}%)')


    def print_info(self, ntuple, title=None):
        """ Generic printer without fancy explanation.
        Given a named tuple, print information contained in it.
        """
        if title:
            self.printer(f'\nStatistics for {title}')
        for key, val in ntuple._asdict().items():
            self.printer(f'\t{key}: {val}')


    def printer(self, string):
        """ Print data to console, log file or both.
        """
        if self.enable_print:
            print(string)
        if self.enable_log:
            logging.info(string)
        if self.pile:
            self.pile.append(string)


    def get_pile(self):
        return self.pile