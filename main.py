from monitor.monitor import Monitor
import time

if __name__ == "__main__":
    _monitor = Monitor()
    _monitor.system_info()
    _monitor.start(delay=2)
    try:
        for i in range(50):
            time.sleep(0.2)
    finally:    
        _monitor.stop()