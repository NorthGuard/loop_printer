# loop_printer

The LoopPrinter-class of these files does exactly what you would expect. It prints loops.  

Run `python -m loop_printer` to run a ton of different loop-prints. 

The idea is to pack a lot of typically required features into a one-liner method called in a loop, while using 
keyword-arguments to tick off wanted settings.  

First initialize the printer:
```python
loop_printer = LoopPrinter()
```

##### A for-loop and a while-loop

```python
n = 4
for idx in range(n):
    loop_printer.loop_print(idx, n)
   
# Iteration 1 / 4
# Iteration 2 / 4
# Iteration 3 / 4
# Iteration 4 / 4
```


```python
n = 4
idx = 0
while idx < n:
    loop_printer.loop_print(idx)
    idx += 1

# Iteration 2
# Iteration 3
# Iteration 1
# Iteration 4
```

Note that if the first value given to the loop_print-method is not 0, you must pass `first_count=X`, 
where X is the first count-value passed to the method.

##### Time and date stamp

```python
n = 4
for idx in range(n):
    time.sleep(0.5)
    loop_printer.loop_print(idx, n,
                            time_stamp=True, date_stamp=True)

# 05-06-2017 11:43:41 -> Iteration 1 / 4
# 05-06-2017 11:43:42 -> Iteration 2 / 4
# 05-06-2017 11:43:42 -> Iteration 3 / 4
# 05-06-2017 11:43:43 -> Iteration 4 / 4
```


##### Name, message and percentage

```python
n = 4
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            name="Step", message="Message {}".format(idx + 1), 
                            percentage=True)

# Step 1 / 4 ( 25.00%): Message 1
# Step 2 / 4 ( 50.00%): Message 2
# Step 3 / 4 ( 75.00%): Message 3
# Step 4 / 4 (100.00%): Message 4
```


##### Header

```python
n = 4
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            header_message="HEADER")

# HEADER
# Printing every 1 of 4 tasks.
# ---------------------------------------------------------------------------
# Iteration 1 / 4
# Iteration 2 / 4
# Iteration 3 / 4
# Iteration 4 / 4
```


##### Controlling when to print
Prints always include first and last iteration.  

Absolute step size:
```python
n = 10
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            fraction=-2, header_message="")

# Printing every 2 of 10 tasks.
# ---------------------------------------------------------------------------
# Iteration  1 / 10
# Iteration  2 / 10
# Iteration  4 / 10
# Iteration  6 / 10
# Iteration  8 / 10
# Iteration 10 / 10
```

Fractional step size:
```python
n = 10
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            fraction=0.25, header_message="")

# Printing progress at fractions of 0.25 with a total of 10 tasks.
# ---------------------------------------------------------------------------
# Iteration  1 / 10
# Iteration  3 / 10
# Iteration  5 / 10
# Iteration  8 / 10
# Iteration 10 / 10
```

Specific number of prints:
```python
n = 10
for idx in range(n):
    loop_printer.loop_print(idx, n,
                            fraction=4, header_message="")
                            
# Printing 4 reports for a total of 10 tasks.
# ---------------------------------------------------------------------------
# Iteration  1 / 10
# Iteration  4 / 10
# Iteration  7 / 10
# Iteration 10 / 10
```

##### Estimating time left

Linear extrapolation (each step takes the same time):
```python
n = 10
for idx in range(n):
    time.sleep(0.5)
    loop_printer.loop_print(idx, n, time_stamp=True,
                            time_left=True, header_message="")

# Printing every 1 of 10 tasks.
# Estimating remaining time with linear extrapolation.
# ---------------------------------------------------------------------------
# 11:57:56 [Time left:         ] -> Iteration  1 / 10
# 11:57:56 [Time left: 00:00:04] -> Iteration  2 / 10
# 11:57:57 [Time left: 00:00:04] -> Iteration  3 / 10
# 11:57:57 [Time left: 00:00:03] -> Iteration  4 / 10
# 11:57:58 [Time left: 00:00:03] -> Iteration  5 / 10
# 11:57:58 [Time left: 00:00:02] -> Iteration  6 / 10
# 11:57:59 [Time left: 00:00:02] -> Iteration  7 / 10
# 11:57:59 [Time left: 00:00:01] -> Iteration  8 / 10
# 11:58:00 [Time left: 00:00:01] -> Iteration  9 / 10
# 11:58:00 [Time left: 00:00:00] -> Iteration 10 / 10
```

2-degree polynomial extrapolation (each step takes linearly longer time than previous ones):
```python
n = 10
for idx in range(n):
    time.sleep(idx)
    loop_printer.loop_print(idx, n, time_stamp=True,
                            time_left=True, time_left_method="poly2", header_message="")
                            
# Printing every 1 of 10 tasks.
# Estimating remaining time with 2-degree polynomial
# ---------------------------------------------------------------------------
# 11:58:00 [Time left:         ] -> Iteration  1 / 10
# 11:58:01 [Time left:         ] -> Iteration  2 / 10
# 11:58:03 [Time left: 00:00:51] -> Iteration  3 / 10
# 11:58:06 [Time left: 00:00:49] -> Iteration  4 / 10
# 11:58:10 [Time left: 00:00:45] -> Iteration  5 / 10
# 11:58:15 [Time left: 00:00:40] -> Iteration  6 / 10
# 11:58:21 [Time left: 00:00:34] -> Iteration  7 / 10
# 11:58:28 [Time left: 00:00:27] -> Iteration  8 / 10
# 11:58:36 [Time left: 00:00:19] -> Iteration  9 / 10
# 11:58:45 [Time left: 00:00:10] -> Iteration 10 / 10
```

Time-left estimation with different starting point:
```python
n = 110
n_start = 100
for idx in range(n_start, n):
    time.sleep(2)
    loop_printer.loop_print(idx, n, fraction=5, time_stamp=True, first_count=n_start,
                            time_left=True, header_message="")
                            
# Printing 5 reports for tasks 101 to 110.
# Estimating remaining time with linear extrapolation.
# ---------------------------------------------------------------------------
# 13:27:37 [Time left:         ] -> Iteration 101 / 110
# 13:27:39 [Time left:         ] -> Iteration 102 / 110
# 13:27:43 [Time left: 00:00:14] -> Iteration 104 / 110
# 13:27:47 [Time left: 00:00:10] -> Iteration 106 / 110
# 13:27:51 [Time left: 00:00:06] -> Iteration 108 / 110
# 13:27:55 [Time left: 00:00:02] -> Iteration 110 / 110
```


##### Other timings
```python
n = 10
for idx in range(n):
    time.sleep(random.randint(3, 6))
    loop_printer.loop_print(idx, n,
                            step_time=True, avg_step_time=True, total_time=True)
                            
# [Step time:         , avg time:         , total time:         ] -> Iteration 1 / 5
# [Step time: 00:00:00, avg time: 00:00:00, total time: 00:00:00] -> Iteration 2 / 5
# [Step time: 00:00:00, avg time: 00:00:00, total time: 00:00:01] -> Iteration 3 / 5
# [Step time: 00:00:00, avg time: 00:00:00, total time: 00:00:01] -> Iteration 4 / 5
# [Step time: 00:00:00, avg time: 00:00:00, total time: 00:00:02] -> Iteration 5 / 5
```


##### Other settings

* Microsecond-precision.  
    * For microsecond-precision on time stamp, set `stamp_microseconds=True`.
    * For microsecond-precision on other timings (ex. time left), set `time_microseconds=True`.
* Starting at iteration-number different than 0.  
    Pass `first_count=X`, where `X` is the first value, to ensure consistency 
    (especially if you want to predict time left).
* Appending messages. If you have a lot on your heart you can pass multiple strings to loop_print,
    which will be printed on consecutive lines, with same indentation as the normal message.  
    This can be done with keyword: `appending_messages=["str1", "str2", ...]`
* Indentation. If you wan the loop_print to occur within other blocks of printed string, 
    you can indent the whole shebang using `indentation=X`, where `X` is either an integer 
    (number of spaces) or a string used for indentation.
* Single line print. If you want the loop_print method to print on the same line and update it,
    set `single_line=True`.
* Options can be sent directly to Python's print function, used for printing at each iteration, 
    by passing a dictionary of options to `print_options`.


##### The works

Here's a run with a lot of settings.
```python
the_list = range(0, 20)
for idx in the_list:
    time.sleep(0.5)
    loop_printer.loop_print(idx, the_list, fraction=0.25,
                            name="Step", message="Awesome", percentage=True,
                            header_message="The works.",
                            date_stamp=True, time_stamp=True,
                            step_time=True, avg_step_time=True, total_time=True, time_left=True)
loop_printer.end_line()

# The works.
# Printing progress at fractions of 0.25 with a total of 20 tasks.
# Estimating remaining time with linear extrapolation.
# ---------------------------------------------------------------------------
# 05-06-2017 12:17:25 [Step time:         , avg time:         , total time:         , time left:         ] -> Step  1 / 20 (  5.00%): Awesome
# 05-06-2017 12:17:27 [Step time: 00:00:00, avg time: 00:00:00, total time: 00:00:02, time left: 00:00:08] -> Step  5 / 20 ( 25.00%): Awesome
# 05-06-2017 12:17:29 [Step time: 00:00:00, avg time: 00:00:00, total time: 00:00:04, time left: 00:00:05] -> Step 10 / 20 ( 50.00%): Awesome
# 05-06-2017 12:17:32 [Step time: 00:00:00, avg time: 00:00:00, total time: 00:00:07, time left: 00:00:03] -> Step 15 / 20 ( 75.00%): Awesome
# 05-06-2017 12:17:34 [Step time: 00:00:00, avg time: 00:00:00, total time: 00:00:09, time left: 00:00:00] -> Step 20 / 20 (100.00%): Awesome
# ---------------------------------------------------------------------------
```

