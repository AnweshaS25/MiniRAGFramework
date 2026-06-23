"""
Framework constants.
"""


class LoaderTypes:
    PDF = "pdf"


class SplitterTypes:
    CHARACTER = "character"
    RECURSIVE = "recursive"
    TOKEN = "token"


class EmbeddingTypes:
    HUGGINGFACE = "huggingface"
    BGE = "bge"


class VectorStoreTypes:
    INMEMORY = "inmemory"
    CHROMA = "chroma"


class RetrieverTypes:
    SIMILARITY = "similarity"


class LLMTypes:
    GROQ = "groq"