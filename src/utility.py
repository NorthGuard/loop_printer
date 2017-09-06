import collections
import math

import regex


def convert_indentation(indentation):
    """
    Converts integer- or string- indentation into string indentation for prepending.
    :param int | str indentation:
    :return: str
    """
    return " " * indentation if isinstance(indentation, int) else indentation


def _get_difference_formatter(time_stamp_length, difference_selector, stamp):
    """
    Creates a formatter for including the time-statistics.
    :param int time_stamp_length: Length of the time stamp.
    :param [bool] difference_selector: Selects stats to print.
    :param str stamp: Optional stamp printed before time-stats.
    :return: str
    """
    # All possible stat-formatters
    difference_formatter = ["Step time: {0:<" + str(time_stamp_length) + "s}",
                            "Avg time: {1:<" + str(time_stamp_length) + "s}",
                            "Total time: {2:<" + str(time_stamp_length) + "s}",
                            "Time left: {3:<" + str(time_stamp_length) + "s}"]
    # Select chosen stats
    difference_formatter = [item for choice, item in zip(difference_selector, difference_formatter)
                            if choice]

    # Capital letter only on first stat
    difference_formatter[1:] = [item.lower() for item in difference_formatter[1:]]

    # Join stat-formatters
    difference_formatter = (" " if stamp != "" else "") + '[' + ', '.join(difference_formatter) + ']'
    return difference_formatter


def _precision_on_microseconds(string, precision):
    """
    Ensures a specific precision on microseconds.
    :param str string: Example: "00:00:01:1186"
    :param int precision:
    """
    # TODO: Make microseconds round instead of truncate.
    if precision is not None and precision:
        current_precision = string[::-1].find(":")
        # micro_text = string[-current_precision:]
        # microseconds = int(micro_text)
        if current_precision == precision:
            return string
        elif current_precision < precision:
            return string + "0" * (precision - current_precision)
        else:
            return string[:(precision - current_precision)]
    else:
        return string


def is_step(fraction, n, count, first_count):
    """
    Determines whether the current iteration is a step (an iteration with print).
    :param float fraction: Determines the frequency of prints.
    :param int n: Total number of iterations.
    :param int count: Current iteration.
    :param int first_count: Starting iteration.
    :return: bool
    """
    # Absolute steps
    if fraction < 0:
        mod = round(abs(fraction))
        return (count % mod) == 0

    # Convert to fraction
    if fraction > 1:
        fraction = max(2.0, fraction) - 1.0
        fraction = 1.0 / fraction

    # Compute step
    step = (n - first_count) * fraction

    # Find next split
    current_multiplier = math.floor(count / step)
    current_split = current_multiplier * step

    # Check if passed step
    return float(count - 1) < current_split <= float(count)


def _delta_time_str(days, seconds, microseconds, use_microseconds=False):
    """
    Turn days, seconds and microseconds into printable string.
    :param int days:
    :param int seconds:
    :param int microseconds:
    :param bool | int use_microseconds:
    :return:
    """
    # Conversion
    remainder = divmod(seconds, 3600)[1]
    temp = {
        'days': days,
        'hours': divmod(seconds, 3600)[0],
        'minutes': divmod(remainder, 60)[0],
        'seconds': divmod(remainder, 60)[1],
        'microseconds': microseconds
    }
    # Formatter
    formatter = "{hours:02d}:{minutes:02d}:{seconds:02d}"
    if use_microseconds:
        formatter += ":{microseconds:d}"
    if days == 1:
        formatter = "1 day, " + formatter
    elif days > 1:
        formatter = "{days} days, " + formatter

    string = formatter.format(**temp)
    string = _precision_on_microseconds(string, use_microseconds)
    return string


def fraction_header(fraction, indent, count, total_counts):
    # Specified number of prints
    if fraction > 1:
        header = "\n" + indent + "Printing {} reports".format(fraction)
        if count == 1:
            header += " for a total of {} tasks.".format(total_counts)
        else:
            header += " for tasks {} to {}.".format(count, total_counts)

    # Fractional number of prints
    elif fraction > 0:
        header = "\n" + indent + "Printing progress at fractions of {}".format(fraction)
        if count == 1:
            header += " with a total of {} tasks.".format(total_counts)
        else:
            header += " for tasks {} to {}.".format(count, total_counts)

    # Absolute number of prints
    else:
        header = "\n" + indent + "Printing every {}".format(-fraction)
        if total_counts is not None:
            if count == 1:
                header += " of {} tasks.".format(total_counts)
            else:
                header += " task, for tasks {} to {}.".format(count, total_counts)
        else:
            header += " task."

    return header


def make_header(count, fraction, time_left, time_left_method, total_counts, is_first_call,
                header_message, indent, line_length):
    header = ""

    # Check if any header is needed
    if is_first_call and header_message is not None:
        # Start header-formatter with any given message from user
        if header_message == "":
            header = ""
        else:
            header = "\n" + indent + header_message

        # Report of printing fraction
        header += fraction_header(fraction=fraction, indent=indent, count=count, total_counts=total_counts)

        # If time-left is computed, report method used to extrapolating time
        if time_left:
            # Special case for linear extrapolation
            if time_left_method == "linear" or time_left_method == "poly1":
                header += "\n" + indent + "Estimating remaining time with linear extrapolation."

            # Other polynomial methods
            elif "poly" in time_left_method:
                degree = int(regex.search("\d+", time_left_method.lower()).group(0))
                degree = min(degree, 4)
                header += "\n" + indent + "Estimating remaining time with {}-degree polynomial".format(degree)

        # Add finishing line to header
        header += "\n" + indent + "-" * line_length

    # Return header
    if header == "":
        return None
    return header


def ensure_fraction_and_total(fraction, list_or_total):
    # If no list_or_total is given, then print after absolute number of steps.
    if list_or_total is None:
        total_counts = None
        fraction = -max(round(abs(fraction)), 1)

    # If a number is given as list_or_total, consider this the maximum expected number of iterations.
    elif isinstance(list_or_total, int) or isinstance(list_or_total, float):
        total_counts = int(list_or_total)

    # If list_or_total is a sized-collection, determine its size and use that for the number of iterations.
    elif isinstance(list_or_total, collections.Sized):
        total_counts = len(list_or_total)

    # Otherwise something incorrect was given as list_or_total
    else:
        raise ValueError("total_counts is not set to anything useful in LoopPrinter")

    return fraction, total_counts