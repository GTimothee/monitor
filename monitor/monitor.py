from threading import Thread


class Monitor(Thread):
    def __init__(self, logging=True, printing=True):
        """
        Arguments:
        ----------
            logging: a boolean
            printing: a boolean
        """
        self.run = False
        self.logging = logging 
        self.printing = printing


    def start(self):
        """ Start printing monitoring information.
        """
        self.run = True 
        while self.run:
            self.inspect()


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


    def system_info(self):
        """ Get system general infomation.
        """
        self.printer(f'\nGeneral information on the system:')
        nb_logic = psutil.cpu_count(logical=True)
        nb_physic = psutil.cpu_count(logical=False)
        self.printer(f'\t-Found {nb_logic} logical cores for {nb_physic} physical CPUs')


    def inspect(self):
        """ Print monitoring information.
        """
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
        ntuple = psutil.virtual_memory()
        self.printer(f'Available RAM: {ntuple.available}/{ntuple.total} ({ntuple.percent}%)')

        # from the docs at https://psutil.readthedocs.io/en/latest/
        THRESHOLD = 100 * 1024 * 1024  # 100MB
        if ntuple.available <= THRESHOLD:
            self.printer(f'WARNING: not much memory left.')
        

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
