from monitor import Monitor
import time

if __name__ == "__main__":
    _monitor = Monitor()
    _monitor.system_infos()
    _monitor.start()
    try:
        for i in range(50):
            time.sleep(0.2)
    finally:    
        _monitor.stop()