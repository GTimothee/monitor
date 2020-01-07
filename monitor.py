from threading import Thread


class Monitor(Thread):
    def __init__(self, logging=True, printing=True):
        """
        logging: a boolean
        printing: a boolean
        """
        self.run = False
        self.logging = logging 
        self.printing = printing

    def start(self):
        self.run = True 
        while self.run:
            self.inspect()


    def stop(self):
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


    def system_infos(self):
        cpu_ntuple = psutil.cpu_times(percpu=False)
        print_infos(cpu_ntuple, "CPU times")


    def inspect(self):
        psutil.cpu_percent(interval=None, percpu=False)


    def print_infos(self, ntuple, title=None):
        if title:
            self.printer(f'\nStatistics for {title}')
        for key, val in ntuple._asdict().items():
            self.printer(f'\t - {key}: {val}')


    def printer(self, string):
        if self.printing:
            print(string)
        if self.logging:
            logging.info(string)
