from src.evaluation.timer import StageTimer
from src.evaluation.metrics_collector import MetricsCollector


class BenchmarkRunner:
    """
    Runs benchmark queries and collects performance metrics.
    """

    def __init__(
        self,
        pipeline,
    ):

        self.pipeline = pipeline

        self.timer = self.pipeline.timer
        
        self.collector = MetricsCollector()

    def run(
        self,
        queries,
        user,
    ):

        for query in queries:
            self.timer.reset()
            # self.timer.start("total")
            self.pipeline.run(
                query,
                user=user,
            )
            # self.timer.stop("total")            
            self.collector.add_record(
                timings=self.timer.get_timings(),
            )

        return self.collector.summary()