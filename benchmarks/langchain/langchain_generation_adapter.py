from benchmarks.langchain.langchain_pipeline import LangChainPipeline


class LangChainGenerationAdapter:
    """
    Adapter so LangChain pipeline can be evaluated using our EvaluationRunner.
    """

    def __init__(self, pipeline: LangChainPipeline):
        self.pipeline = pipeline

    def run(self, query: str, user=None):
        """
        Generate an answer using the LangChain pipeline.
        """
        answer = self.pipeline.generate(query)

        # Make it look like our Response object
        class Response:
            def __init__(self, text):
                self.text = text

        return Response(answer)