import random
import time
from loop_printer.src.printer import LoopPrinter

# Initialize
loop_printer = LoopPrinter()


# A for-loop and a while-loop

n = 4
for idx in range(n):
    loop_printer.loop_print(idx, n)

n = 4
idx = 0
while idx < n:
    loop_printer.loop_print(idx)
    idx += 1


# Time and date stamp

n = 4
for idx in range(n):
    time.sleep(0.5)
    loop_printer.loop_print(idx, n,
                            time_stamp=True, date_stamp=True)


# Name, message and percentage

n = 4
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            name="Step", message="Message {}".format(idx + 1),
                            percentage=True)


# Pre-message
n = 7
for idx in range(n):
    loop_printer.loop_print(idx, n,  header_message="Pre-message on even numbers!",
                            pre_message="pre-message" if idx % 2 == 0 else None)


# Header

n = 4
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            header_message="HEADER")


# Controlling when to print

n = 10
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            fraction=-2, header_message="")

n = 10
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            fraction=0.25, header_message="")

n = 10
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            fraction=4, header_message="")


# Estimating time left

n = 10
for idx in range(n):
    time.sleep(0.5)
    loop_printer.loop_print(idx, n, time_stamp=True,
                            time_left=True, header_message="")


n = 10
for idx in range(n):
    time.sleep(idx)
    loop_printer.loop_print(idx, n, time_stamp=True,
                            time_left=True, time_left_method="poly2", header_message="")


# Estimating time left with different starting point
n = 110
n_start = 100
for idx in range(n_start, n):
    time.sleep(2)
    loop_printer.loop_print(idx, n, fraction=5, time_stamp=True, first_count=n_start,
                            time_left=True, header_message="")


# Other timings
n = 10
for idx in range(n):
    time.sleep(random.randint(3, 6))
    loop_printer.loop_print(idx, n,
                            step_time=True, avg_step_time=True, total_time=True)

# The works
the_list = range(0, 20)
for idx in the_list:
    time.sleep(1.5)
    loop_printer.loop_print(idx, the_list, fraction=0.25,
                            name="Step", message="Awesome", percentage=True,
                            header_message="The works.",
                            date_stamp=True, time_stamp=True,
                            step_time=True, avg_step_time=True, total_time=True, time_left=True)
loop_printer.end_line()

# Loop with large number of time-step samples
n = 10000
for idx in range(n):
    time.sleep(0.001)
    loop_printer.loop_print(idx, n, fraction=-470, time_stamp=True, time_left=True,
                            message="Time stamps: {}".format(len(loop_printer.timer.time_stamps)))

