import time


class StageTimer:
    """
    Utility for measuring execution time
    of framework stages.
    """

    def __init__(self):

        self.timings = {}

        self._starts = {}

    def start(self, stage):

        self._starts[stage] = time.perf_counter()

    def stop(self, stage):

        if stage not in self._starts:
            raise ValueError(
                f"Stage '{stage}' was never started."
            )

        elapsed = time.perf_counter() - self._starts[stage]

        self.timings[stage] = elapsed

        return elapsed

    def get_timings(self):

        return self.timings

    def reset(self):

        self.timings.clear()

        self._starts.clear()