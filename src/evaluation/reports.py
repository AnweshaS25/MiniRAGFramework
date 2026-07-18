class ReportGenerator:
    """
    Generates benchmark reports.
    """

    def __init__(
        self,
        evaluator,
    ):

        self.evaluator = evaluator

    def generate_text(self):

        results = self.evaluator.compare()

        lines = []

        lines.append("=" * 50)

        lines.append("Framework Comparison Report")

        lines.append("=" * 50)

        for framework, metrics in results.items():

            lines.append("")

            lines.append(framework)

            lines.append("-" * len(framework))

            for stage, values in metrics.items():

                lines.append(
                    f"{stage}: {values['average']:.4f} sec"
                )

        return "\n".join(lines)