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


# Other timings

n = 10
for idx in range(n):
    time.sleep(random.randint(3, 6))
    loop_printer.loop_print(idx, n,
                            step_time=True, avg_step_time=True, total_time=True)

# The works
the_list = range(0, 20)
for idx in the_list:
    time.sleep(0.5)
    loop_printer.loop_print(idx, the_list, fraction=0.25,
                            name="Step", message="Awesome", percentage=True,
                            header_message="The works.",
                            date_stamp=True, time_stamp=True,
                            step_time=True, avg_step_time=True, total_time=True, time_left=True)
loop_printer.end_line()

