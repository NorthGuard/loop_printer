import math


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


def is_step(fraction, n, count):
    """
    Determines whether the current iteration is a step (an iteration with print).
    :param float fraction: Determines the frequency of prints.
    :param n: Total number of iterations.
    :param count: Current iteration.
    :return: bool
    """
    # Absolute steps
    if fraction < 0:
        mod = round(abs(fraction))
        return (count % mod) == 0
    # Convert to fraction
    if fraction > 1:
        fraction = max(2, fraction) - 1.0
        fraction = 1.0 / fraction
    # Compute step
    step = n * fraction
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
