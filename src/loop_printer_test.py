import time
from loop_printer import LoopPrinter


printer = LoopPrinter()
short_time = 0.2
long_time = 0.5

n_loops = 60

the_list = range(0, 10)
for idx in the_list:
    printer.loop_print(idx, the_list, header_message="10 Loops with every print",
                       fraction=10)
print("\n")

print("60 loops with various numbers of prints:")
for nr_prints in range(2, 7):
    the_list = range(0, n_loops)
    for idx in the_list:
        printer.loop_print(idx, the_list, fraction=nr_prints,
                           header_message="",
                           indentation=3)
print("\n")

for nr_prints in range(2, 7):
    the_list = range(0, n_loops)
    for idx in the_list:
        printer.loop_print(idx, the_list, header_message="",
                           fraction=1.0 / nr_prints)
print("\n")

for step in range(2, 7):
    print("\n{0} Loops with print at every {1}-step:".format(n_loops, step))
    the_list = range(0, n_loops)
    for idx in the_list:
        printer.loop_print(idx, the_list, fraction=-step)
print("\n")

print("While loop with {0} iterations with print at every step and 1-indexing:".format(10))
idx = 0
while idx < 10:
    idx += 1
    printer.loop_print(idx, first_count=False)
print("\n")

for step in range(2, 7):
    print("\nWhile loop with {0} iterations with print at every {1}-step:".format(n_loops, step))
    idx = 0
    while idx < n_loops:
        printer.loop_print(idx, fraction=step)
        idx += 1
print("\n")

print("10 Loops with 4 prints and time:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(short_time)
    printer.loop_print(idx, the_list, fraction=4, time_stamp=True)
print("\n")

print("10 Loops with 4 prints and date:")
the_list = range(0, 10)
for idx in the_list:
    printer.loop_print(idx, the_list, fraction=4, date_stamp=True)
print("\n")

print("10 Loops with 4 prints and date and time:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(short_time)
    printer.loop_print(idx, the_list, fraction=4, date_stamp=True, time_stamp=True)
print("\n")

print("10 Loops with 4 prints and detailed date and time:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(short_time)
    printer.loop_print(idx, the_list, fraction=4, date_stamp=True, time_stamp=True)
print("\n")

print("10 Loops with 4 prints and time to microseconds:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(short_time)
    printer.loop_print(idx, the_list, fraction=4, time_stamp=True, stamp_microseconds=True, time_microseconds=True)
print("\n")

print("10 Loops with 4 prints with name and message:")
the_list = range(0, 10)
for idx in the_list:
    printer.loop_print(idx, the_list, fraction=4, name='name', message='message')
print("\n")

print("10 Loops, 4 prints with step-times:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(long_time)
    printer.loop_print(idx, the_list, fraction=4, step_time=True)
print("\n")

print("10 Loops, 4 prints with average times:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(long_time)
    printer.loop_print(idx, the_list, fraction=4, avg_step_time=True)
print("\n")

print("10 Loops, 4 prints with total-times:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(long_time)
    printer.loop_print(idx, the_list, fraction=4, total_time=True)
print("\n")

print("10 Loops, 4 prints with step-times and average times:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(long_time)
    printer.loop_print(idx, the_list, fraction=4, step_time=True, avg_step_time=True)
print("\n")

print("10 Loops, 4 prints with average times and total-times:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(long_time)
    printer.loop_print(idx, the_list, fraction=4, avg_step_time=True, total_time=True)
print("\n")

print("10 Loops, 4 prints with step-times and total-times:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(long_time)
    printer.loop_print(idx, the_list, fraction=4, step_time=True, total_time=True)
print("\n")

print("10 Loops, 4 prints with step-, average and total-times:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(long_time)
    printer.loop_print(idx, the_list, fraction=4, step_time=True, avg_step_time=True, total_time=True)
print("\n")

print("10 Loops with time-left calculation:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(long_time)
    printer.loop_print(idx, the_list, fraction=-1, time_left=True)
print("\n")

print("10 Loops with the works:")
the_list = range(0, 10)
for idx in the_list:
    time.sleep(long_time)
    printer.loop_print(idx, the_list, fraction=-1, date_stamp=True, time_stamp=True, message="Awesome",
                       name="Process",
                       step_time=True, avg_step_time=True, total_time=True, time_left=True)
print("\n")
