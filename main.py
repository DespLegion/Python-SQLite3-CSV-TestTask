import sys
from app.src.commands import execute_from_command_line
from memory_profiler import memory_usage
import time

if __name__ == '__main__':
    start_time = time.time()
    execute_from_command_line(sys.argv)
    print("---------------------------")
    print(f"Program execution time: {(time.time() - start_time)} seconds")
    print(f"Program memory usage: {memory_usage(-1)[0]}(MB)")
