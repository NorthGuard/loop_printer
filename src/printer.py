import collections

import regex

from loop_printer.src.timer import _ITakeCareOfTime
from .utility import _is_step, _do_post_function


class LoopPrinter(object):
    def __init__(self, line_length=75):
        self.last_print_count = None  # type: int
        self.line_length = line_length
        self.single_line = False
        self.indentation = 0

        # Timing
        self.timer = _ITakeCareOfTime()

    def _reset(self):
        self.last_print_count = None  # type: int
        self.single_line = False

        # Timing
        self.timer.reset()

    def loop_print(self,
                   count, list_or_total=None, fraction=0.1,  # Main options
                   *,  # Signals keyword-only arguments
                   name="Iteration", message=None, appending_messages=None,  # Messages
                   header=True, header_message=None,  # Header
                   date_stamp=False, time_stamp=False,  # Time-stamps
                   time_left=False, time_left_method="linear",  # Time left estimation
                   total_time=False, avg_step_time=False, step_time=False,  # Computed timings
                   first_count=0, time_microseconds=False, stamp_microseconds=False,  # General settings
                   indentation=0, single_line=False,
                   print_options=None  # Options passed on
                   ):
        """
        Print-method for loops.
        Format: "<name> <count> / <total>: <message>" or "<name> <count>: <message>" (if no limit is given)
        The print always occurs at the very first and very last iteration.

        Main options:
        :param int count: The counter in the loop.
        :param int | Collection list_or_total:
                        int: The total number of iterations
                        Collection: len(list_or_total) is used to find number of iterations.
        :param float fraction: Determines the number of prints.
            The printer always prints first and last iteration.
                fraction < 0 : Print at every abs(fraction)th-iteration. Thus -10 will print every tenth iteration.
            0 < fraction < 1 : Prints after every fraction-part. For example 0.2 will print at 20%, 40%, 60% etc.
            1 < fraction     : Number of prints (excluding first print). Thus 10 will print at first iteration,
                    followed by 10 prints, evenly spread out across the remaining iterations.

        Messages:
        :param str name: Name of iteration. Examples: loop, iteration, processes, steps etc.
        :param str message: Message to show after counters (right-appended).
        :param [str] appending_messages: Messages to write on consecutive lines (makes print multi-lines).

        # Header:
        :param bool header: Enables a header that is printed at first iteration.
        :param str header_message: Writes a message at the header.

        Time-stamps:
        :param bool date_stamp: Makes printer include date-stamp in print.
        :param bool time_stamp: Makes printer include time-stamp in print.

        Time left estimation:
        :param bool time_left: Estimated time left (linear extrapolation)
        :param str time_left_method:
            "linear"            : Linear estimation
            "polyX"             : Polynomial of 'X'-degree. Fx. "poly2"
            "exp"               : Exponential

        Computed timings:
        :param bool total_time: Time since first print (total time)
        :param bool avg_step_time: Average step time
        :param bool step_time: Time difference since last print

        General settings:
        :param int first_count: What is the first number given? (necessary for counting)
            False: one-indexing is used.
        :param bool | int time_microseconds: Use microseconds when printing times.
        :param bool | int stamp_microseconds: Use microseconds when printing time stamp.
        :param int | str indentation: Indentation of print.
            A number prints that number of spaces. A string is prepended.
        :param bool single_line: Allows printing on the same line.

        Options passed on:
        :param dict print_options: A dictionary with options passed directly on to Python's print-function.
        """

        # Number of loops and indexing
        if list_or_total is None:
            total_counts = None
            fraction = -max(round(abs(fraction)), 1)
        elif isinstance(list_or_total, int) or isinstance(list_or_total, float):
            total_counts = int(list_or_total)
        elif isinstance(list_or_total, collections.Sized):
            total_counts = len(list_or_total)
        else:
            raise ValueError("total_counts is not set to anything useful in LoopPrinter")

        # Check if this is first call
        is_first_call = False
        if first_count == count:
            is_first_call = True

        # Reset at first call
        if is_first_call:
            self._reset()

        # Errors
        self.timer.time_left_method = time_left_method
        if total_counts is None and time_left:
            raise Exception("Can't estimate time left without knowing the number of tasks.")

        # Is printing needed?
        auto_print = is_first_call or count == total_counts
        do_print = _is_step(fraction, total_counts, count) or auto_print

        # Update times and steps
        self.timer.update_times_steps(count=count, is_first_call=is_first_call)

        # Print on same line
        self.single_line = single_line

        # Make time_microseconds an interger of precision
        if time_microseconds:
            if isinstance(time_microseconds, bool):
                time_microseconds = 3
        if stamp_microseconds:
            if isinstance(stamp_microseconds, bool):
                stamp_microseconds = 3

        # Indentation
        self.indentation = indentation
        indent = (" " * indentation if isinstance(indentation, int) else str(indentation))

        # Header
        if is_first_call and header:
            formatter = "\n" + indent + header_message if header_message is not None else "\n"
            if fraction > 1:
                formatter += "\n" + indent + "Printing {} reports for a total of ".format(fraction)
            elif fraction > 0:
                formatter += "\n" + indent + "Printing progress at fractions of {} with a total of ".format(fraction)
            else:
                formatter += "\n" + indent + "Printing every {} of ".format(-fraction)
            if total_counts is not None:
                formatter += "{} tasks."
            else:
                formatter += "."
            print(indent + formatter.format(total_counts))

            if time_left:
                if time_left_method == "linear" or time_left_method == "poly1":
                    print(indent + "Estimating remaining time with linear extrapolation.")
                elif "poly" in time_left_method:
                    degree = int(regex.search("\d+", time_left_method.lower()).group(0))
                    degree = min(degree, 4)
                    print(indent + "Estimating remaining time with polynomial of degree {}".format(degree))

            print(indent + "-" * self.line_length)

        # Print?
        if do_print:
            # Timing
            time_message = self.timer.time_message(count=count,
                                                   total_counts=total_counts,
                                                   time_stamp=time_stamp,
                                                   date_stamp=date_stamp,
                                                   step_time=step_time,
                                                   avg_step_time=avg_step_time,
                                                   total_time=total_time,
                                                   time_left=time_left,
                                                   stamp_microseconds=stamp_microseconds,
                                                   time_microseconds=time_microseconds)

            # Main stamp
            if total_counts:
                main_stamp = "{0} {1:" + str(len(str(total_counts))) + "d} / {2}"
            else:
                main_stamp = "{0} {1}"

            # Make sure message it okay
            if message is not None:
                message = message.replace("{", "{{").replace("}", "}}")

            # Printing formatter
            arrow_needed = time_stamp or date_stamp or step_time or avg_step_time or total_time or time_left
            formatter = time_message + (" -> " if arrow_needed else "")
            formatter += main_stamp + ((": " + message) if message else "")

            # Print options
            if not print_options:
                print_options = {}

            # Options for printing on same line and post-function printing
            if self.single_line:
                print_options = {**print_options, "end": "\r"}

            # Print!
            final_output = indent + formatter.format(name, count, total_counts)
            print(final_output, **print_options)
            if appending_messages is not None and message is not None:
                main_stamp_length = len(final_output) - len(message)
                if isinstance(appending_messages, str):
                    print(" "*main_stamp_length + appending_messages, **print_options)
                elif isinstance(appending_messages, list):
                    for item in appending_messages:
                        print(" " * main_stamp_length + item, **print_options)

            # For next iteration
            self.last_print_count = count

        # Return
        return do_print, count + (0 if first_count else 1)

    def end_line(self):
        indent = (" " * self.indentation if isinstance(self.indentation, int) else str(self.indentation))
        print(indent + "-" * self.line_length)

    def print_line(self):
        indent = (" " * self.indentation if isinstance(self.indentation, int) else str(self.indentation))
        print(indent + "-" * self.line_length)
