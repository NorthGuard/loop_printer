from datetime import datetime, timedelta

import regex
import scipy as sc
from scipy import optimize
import numpy as np

from loop_printer.src.utility import _delta_time_str, _precision_on_microseconds, _get_difference_formatter


class LoopPrinterTimer:
    """
    This timer records the step-counts passed on to the LoopPrinter and records the times of being called.
    These is_first_call are used to compute various timing information such as time passed, estimated time left etc.
    """
    def __init__(self):
        self.time_stamps = []  # type: [timedelta]
        self.start_time = None  # type: datetime
        self.steps = []  # type: [int]
        self.time_left_method = "linear"

    def reset(self):
        self.time_stamps = []  # type: [timedelta]
        self.start_time = None  # type: datetime
        self.steps = []  # type: [int]
        self.time_left_method = "linear"

    def update_times_steps(self, count, is_first_call):
        """
        Updates the internal lists of information.
        :param int count: Current iteration.
        :param bool is_first_call: Indicates whether this is the first printing.
        """
        if is_first_call:
            self.start_time = datetime.now()
            self.steps = [1]
        else:
            self.time_stamps.append(datetime.now() - self.start_time)
            self.steps.append(count)

    def estimate_time_left(self, use_microseconds, n):
        """
        Computes the estimated time left by fitting a polynomial function to the time of each iteration.
        By extrapolating these values it estimates time left.
        :param bool use_microseconds: Indicates whether the returned string should have a microsecond precision.
        :param int n: Total number of iterations in loop.
        :return: str
        """
        n_steps = len(self.steps)
        time_left = None

        # Linear estimation (uses a 1st-degree polynomial)
        if n_steps > 1 and self.time_left_method.lower() == "linear":
            self.time_left_method = "poly1"

        # Polynomial
        if "poly" in self.time_left_method.lower():
            # Determine degree from input string
            degree = int(regex.search("\d+", self.time_left_method.lower()).group(0))

            # First few samples can only be approximated with a low-degree polynomial
            if n_steps < degree + 1:
                return None

            # Get seconds of each time-step
            seconds = np.array([time.total_seconds() for time in self.time_stamps])
            steps = np.array(self.steps[:-1])

            # Select polynomial based on degree (Forcing intersection at 0)
            if degree == 1:
                def fit_func(params, x):
                    return params[0] * x
            elif degree == 2:
                def fit_func(params, x):
                    return params[0] * x + params[1] * x ** 2
            elif degree == 3:
                def fit_func(params, x):
                    return params[0] * x + params[1] * x ** 2 + params[2] * x ** 3
            elif degree == 4:
                def fit_func(params, x):
                    return params[0] * x + params[1] * x ** 2 + params[2] * x ** 3 + params[3] * x ** 4
            else:
                raise NotImplementedError("ETA estimation using polynomial of degree > 4 has not been implemented "
                                          "(although it can easily be done).")

            # Define error function
            def error(p, x, y):
                return fit_func(p, x) - y

            # Initial values
            init_p = np.array([1] * degree)

            # Optimize polynomial
            p1 = optimize.leastsq(error, init_p, args=(steps, seconds))
            parameters = p1[0]

            # Predict time left
            time_left = max(0, fit_func(parameters, n) - seconds[-1])
            time_left = timedelta(seconds=time_left)

        # If a time left has been computed convert to string
        if time_left is not None:
            time_left = _delta_time_str(time_left.days, time_left.seconds, time_left.microseconds,
                                        use_microseconds)

        # Return
        return time_left

    def compute_timings(self, use_microseconds):
        """
        Compute timing statistics (time of last step, average step, total time).
        Returns one string for each of the informations.
        :param bool use_microseconds: Indicates whether the returned string should have a microsecond precision.
        :return: (str, str, str)
        """
        # Last time-step
        if len(self.time_stamps) == 1:
            last_step = self.time_stamps[-1]  # Last step
            total_step = self.time_stamps[-1]  # Total time
            avg_step = self.time_stamps[-1]  # Average step
        else:
            last_step = self.time_stamps[-1] - self.time_stamps[-2]  # Last step
            total_step = self.time_stamps[-1]  # Total time
            avg_step = self.time_stamps[-1] / len(self.time_stamps)  # Average step

        # Last step
        last_step = _delta_time_str(last_step.days, last_step.seconds, last_step.microseconds,
                                    use_microseconds)
        # Total time
        total_step = _delta_time_str(total_step.days, total_step.seconds, total_step.microseconds,
                                     use_microseconds)
        # Average step
        avg_step = _delta_time_str(avg_step.days, avg_step.seconds, avg_step.microseconds,
                                   use_microseconds)

        # Return
        return last_step, total_step, avg_step

    def time_message(self, count, total_counts, time_stamp, date_stamp, step_time, avg_step_time,
                     total_time, time_left, stamp_microseconds, time_microseconds):
        """
        Produces the final time-message used by the LoopPrinter.
        :param int count: Iteration counter.
        :param int total_counts: Total number of counts in loop.
        :param bool time_stamp: Do you want a time-stamp of the print?
        :param bool date_stamp: Do you want a date-stamp of the print?
        :param bool step_time: Do you want a print of the last iterations time?
        :param bool avg_step_time: Do you want a print of the average iteration time?
        :param bool total_time: Do you want a print of the total time?
        :param bool time_left: Do you want a print of the estimated time left?
        :param bool stamp_microseconds: Do you want the iteration-time-stamp to have microsecond precision?
        :param bool time_microseconds: Do you want the other stamps to have microsecond precision?
        :return: str
        """
        # Time stamp
        time_formatter = ("%H:%M:%S:%f" if stamp_microseconds else "%H:%M:%S") \
            if time_stamp else ""

        # Date stamp
        date_formatter = "%d-%m-%Y" if date_stamp else ""

        # Date and time
        timing_str = date_formatter + (" " if time_stamp and date_stamp else "") + time_formatter
        stamp = datetime.now().strftime(timing_str)
        if stamp_microseconds:
            stamp = _precision_on_microseconds(stamp, stamp_microseconds)

        # Output message
        time_message = stamp

        # Additional timing information
        information_selector = [step_time, avg_step_time, total_time, time_left]
        if any(information_selector):
            # Length of each time-information
            time_stamp_length = 8 + (time_microseconds + 1 if time_microseconds else 0)

            # Time formatter
            special_timing_formatter = _get_difference_formatter(time_stamp_length, information_selector, stamp)

            # Time difference stamp
            if count > 1 and (total_time or avg_step_time or step_time):
                last_diff, total_diff, avg_diff = self.compute_timings(time_microseconds)
            else:
                last_diff = avg_diff = total_diff = " " * time_stamp_length

            # Time left
            computed_time_left = None
            if time_left:
                computed_time_left = self.estimate_time_left(time_microseconds, total_counts)
                if computed_time_left is None:
                    computed_time_left = " " * time_stamp_length

            # Insert timings
            time_message += special_timing_formatter.format(last_diff, avg_diff, total_diff, computed_time_left)

        # Return
        return time_message
