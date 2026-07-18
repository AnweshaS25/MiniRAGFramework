from statistics import mean, stdev
import copy


class MetricsCollector:
    """
    Collects and aggregates framework metrics.
    """

    def __init__(self):

        self.records = []

    def add_record(
        self,
        timings: dict,
        metadata: dict | None = None,
    ):

        record = {
            "timings": copy.deepcopy(timings),
            "metadata": copy.deepcopy(metadata or {}),
        }

        self.records.append(record)

    def reset(self):

        self.records.clear()

    def get_records(self):

        return self.records

    def summary(self):

        if not self.records:
            return {}

        stages = {}

        for record in self.records:
            for stage, value in record["timings"].items():
                stages.setdefault(stage, []).append(value)

        summary = {}

        for stage, values in stages.items():

            summary[stage] = {
                "average": mean(values),
                "minimum": min(values),
                "maximum": max(values),
                "standard_deviation": stdev(values) if len(values) > 1 else 0.0,
                "runs": len(values),
            }

        return summary