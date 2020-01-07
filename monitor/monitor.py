from threading import Thread
import logging
import psutil
import time 

import os
clear = lambda: os.system('clear') #on Linux System


class Monitor(Thread):
    def __init__(self, printing=True, log_filepath=None, log_level=logging.INFO):
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
        self.printing = printing

        if log_filepath:
            self.logging = True 
            logging.basicConfig(filename=log_filepath,level=log_level)
        else:
            self.logging = False


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


    def set_logging(logging):
        """
        logging: a boolean
        """
        self.logging = logging

    
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
        self.printer(f'\t-Found {nb_logic} logical cores for {nb_physic} physical CPUs')


    def inspect(self, clear_console=True):
        """ Print monitoring information.
        """
        if self.printing and clear_console:
            clear()

        self.print_memory_info()

        cpu_ntuple = psutil.cpu_times(percpu=False)
        self.print_info(cpu_ntuple, "CPU times")

        self.printer(f'\nSupplementary statistics')
        cpu_percent = psutil.cpu_percent(interval=None, percpu=False)
        self.printer(f'\t-CPU usage: {cpu_percent}%')


    def print_memory_info(self):
        """ Custom printer for neatly printing memory info.
        """
        self.printer(f'\nStatistics for Virtual Memory')
        mem = psutil.virtual_memory()
        self.printer(f'\t-Used RAM: {mem.percent}%')
        self.printer(f'\t-Available RAM: {mem.available /1024 /1024:.2f}MB /{mem.total /1024 /1024:.2f}MB')

        # from the docs at https://psutil.readthedocs.io/en/latest/
        THRESHOLD = 100 * 1024 * 1024  # 100MB
        if mem.available <= THRESHOLD:
            message = f'WARNING: Not much memory left.'
            if self.logging:
                logging.warn(message)
            if self.printing:
                print(message)
        
        swap = psutil.swap_memory()
        self.printer(f'\t-Swap used: {swap.used /1024 /1024:.2f}MB /{swap.total /1024 /1024:.2f}MB ({swap.percent}%)')


    def print_info(self, ntuple, title=None):
        """ Generic printer without fancy explanation.
        Given a named tuple, print information contained in it.
        """
        if title:
            self.printer(f'\nStatistics for {title}')
        for key, val in ntuple._asdict().items():
            self.printer(f'\t-{key}: {val}')


    def printer(self, string):
        """ Print data to console, log file or both.
        """
        if self.printing:
            print(string)
        if self.logging:
            logging.info(string)
