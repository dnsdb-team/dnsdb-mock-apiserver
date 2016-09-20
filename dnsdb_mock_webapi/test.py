import mockserver
import time

if __name__ == '__main__':
    mockserver.start()
    mockserver.total = 5
    time.sleep(1000)
