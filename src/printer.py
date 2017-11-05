import warnings

from loop_printer.src.timer import LoopPrinterTimer
from loop_printer.src.utility import make_header, ensure_fraction_and_total, is_step, convert_indentation


class LoopPrinter(object):
    def __init__(self, line_length=75):
        self.last_print_count = None  # type: int
        self.line_length = line_length
        self.indentation = ""
        self.header_indentation = ""

        # Timing
        self.timer = LoopPrinterTimer()

    def _reset(self):
        self.last_print_count = None  # type: int

        # Timing
        self.timer.reset()

    def loop_print(self,
                   count, list_or_total=None, fraction=-1,  # Main options
                   *,  # Signals keyword-only arguments
                   first_count=0, is_zero_indexed=True,  # Enumeration settings
                   name="Iteration", message=None, appending_messages=None, percentage=False,  # Messages
                   header_message=None,  # Header
                   date_stamp=False, time_stamp=False,  # Time-stamps
                   time_left=False, time_left_method="linear",  # Time left estimation
                   time_memory=100,  # Number of samples to keep for estimating time left
                   total_time=False, avg_step_time=False, step_time=False,  # Computed timings
                   time_microseconds=False, stamp_microseconds=False,  # General settings
                   indentation=0, single_line=False,
                   print_options=None  # Options passed on
                   ):
        """
        Print-method for loops.
        Format: "<name> <count> / <total>: <message>" or "<name> <count>: <message>" (if no limit is given).
        The print always occurs at the very first and very last iteration (if limit is given).
        The following line can be used in loops with no counter:
            _, count = loop_printer.loop_print(count)

        Main options:
        :param int count: The counter in the loop.
        :param int | Collection list_or_total:
                        int: The total number of iterations
                        Collection: len(list_or_total) is used to find number of iterations.
        :param float fraction: Determines the number of prints.
            The printer always prints first and last iteration.
                fraction < 0 : Print at every abs(fraction)th-iteration. Thus -10 will print every tenth iteration.
            0 < fraction < 1 : Prints after every fraction-part.
                               For example 0.2 will print at 0%, 20%, 40%, 60%, 80% and 100%.
            1 < fraction     : Number of prints. 10 will thus print exactly 10 prints,
                               evenly spread out across the iterations.

        Enumeration:
        :param int first_count: What is the first number given? (necessary for time-left estimation, header etc.)
        :param bool is_zero_indexed: Specifies that the counter is
            True: 0-indexed
            False: 1-indexed

        Messages:
        :param str name: Name of iteration. Examples: loop, iteration, process, step etc.
        :param str message: Message to show after print (right-appended).
        :param [str] appending_messages: Messages to write on consecutive lines (makes print multi-lines).
        :param bool percentage: If true, the counter will show a percentage of the total number of iterations (if given)

        Header:
        :param str header_message: Writes a message at the header.
            None: No header
            "": Auto-generated header, with no user message.
            str: Auto-generated header, with user message.

        Time-stamps:
        :param bool date_stamp: Makes printer include date-stamp in print.
        :param bool time_stamp: Makes printer include time-stamp in print.

        Time left estimation:
        :param bool time_left: Estimated time left (linear extrapolation)
        :param str time_left_method:
            "linear"            : Linear estimation
            "polyX"             : Polynomial of 'X'-degree. Fx. "poly2"
            "exp"               : Exponential
        :param int time_memory: Number of time-stamps to keep in memory for estimating timing-information.

        Computed timings:
        :param bool total_time: Time since first print (total time)
        :param bool avg_step_time: Average step time
        :param bool step_time: Time difference since last print

        General settings:
        :param bool | int stamp_microseconds: Use microseconds when printing time stamp.
        :param bool | int time_microseconds: Use microseconds when printing other time-related information.
        :param int | str | tuple indentation: Indentation of print.
            A number prints that number of spaces. A string is prepended.
            A tuple does the same thing, but can contain two indentations: one for thea header and one for the lines.
        :param bool single_line: Allows printing on the same line.

        Options passed on:
        :param dict print_options: A dictionary with options passed directly on to Python's print-function.
        """

        # Ensure counting
        fraction, total_counts = ensure_fraction_and_total(fraction=fraction, list_or_total=list_or_total)

        # Ensure format
        count = int(count)

        # Check if this is first call
        is_first_call = False
        if first_count == count:
            is_first_call = True

        # For zero-indexing add 1
        if is_zero_indexed:
            count += 1
            first_count += 1

        # Reset at first call
        if is_first_call:
            self._reset()

        # Errors
        self.timer.time_left_method = time_left_method
        if total_counts is None and time_left:
            raise Exception("Can't estimate time left without knowing the number of tasks.")

        # Is printing needed?
        auto_print = is_first_call or count == total_counts
        do_print = is_step(fraction=fraction, n=total_counts, count=count, first_count=first_count) or auto_print

        # Update times and steps
        self.timer.update_times_steps(count=count, is_first_call=is_first_call, memory=time_memory)

        # Make boolean microseconds-options an integer of precision
        if time_microseconds:
            if isinstance(time_microseconds, bool):
                time_microseconds = 3
        if stamp_microseconds:
            if isinstance(stamp_microseconds, bool):
                stamp_microseconds = 3

        # Indentation
        if isinstance(indentation, tuple):
            header_indentation = indentation[0]
            indentation = indentation[1]
        else:
            header_indentation = indentation
        self.header_indentation = convert_indentation(header_indentation)
        self.indentation = convert_indentation(indentation)

        # Header
        header_string = make_header(count=count,
                                    fraction=fraction,
                                    time_left=time_left,
                                    time_left_method=time_left_method,
                                    total_counts=total_counts,
                                    is_first_call=is_first_call,
                                    header_message=header_message,
                                    indent=self.header_indentation,
                                    line_length=self.line_length)
        if header_string is not None:
            print(header_string)

        # Iteration print
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
                main_stamp = "{0} {1:" + str(len(str(total_counts))) + ",d} / {2:,d}"

                # Percentage
                if percentage:
                    main_stamp += " ({:7.2%})".format(float(count) / total_counts)
            else:
                main_stamp = "{0} {1:,d}"
            main_stamp = main_stamp.format(name, count, total_counts)

            # Printing formatter
            arrow_needed = time_stamp or date_stamp or step_time or avg_step_time or total_time or time_left
            final_string = time_message + (" -> " if arrow_needed else "")
            final_string += main_stamp + ((": " + message) if message else "")

            # Options for print-function
            print_options = print_options if print_options else {}
            if single_line:
                print_options = {**print_options, "end": "\r", "flush": True}

            # Print!
            final_string = self.indentation + final_string
            print(final_string, **print_options)

            # Appended multi-line messages
            if appending_messages is not None and message is not None:

                # Determine length of main stamp
                main_stamp_length = len(final_string) - len(message)

                # Append single string at end
                if isinstance(appending_messages, str):
                    print(" " * main_stamp_length + appending_messages, **print_options)

                # Append multiple strings at end
                elif isinstance(appending_messages, list):
                    for item in appending_messages:
                        print(" " * main_stamp_length + item, **print_options)

            # For next iteration
            self.last_print_count = count

        # Return
        return do_print, count + (0 if first_count else 1)

    def end_line(self):
        print(self.header_indentation + "-" * self.line_length)

    def print_line(self):
        print(self.indentation + "-" * self.line_length)
