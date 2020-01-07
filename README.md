# monitor

## Motivation

When you want to monitor your system or an application you usually want to use psutil. Instead of everyone creating the same code snippets for basic and general monitoring using psutil, we should gather our forces to create an efficient and reliable package on top of psutil for daily use.

## Example usage

```
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
```