"""
Framework constants.
"""


class LoaderTypes:
    PDF = "pdf"


class SplitterTypes:
    CHARACTER = "character"
    RECURSIVE = "recursive"


class EmbeddingTypes:
    HUGGINGFACE = "huggingface"


class VectorStoreTypes:
    INMEMORY = "inmemory"
    CHROMA = "chroma"


class RetrieverTypes:
    SIMILARITY = "similarity"


class LLMTypes:
    GROQ = "groq"