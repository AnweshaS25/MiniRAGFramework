"""
Framework constants.
"""


class LoaderTypes:
    PDF = "pdf"


class SplitterTypes:
    CHARACTER = "character"
    RECURSIVE = "recursive"
    TOKEN = "token"
    SENTENCE = "sentence"
    MARKDOWN = "markdown"
    CODE = "code"



class EmbeddingTypes:
    HUGGINGFACE = "huggingface"
    BGE = "bge"


class VectorStoreTypes:
    IN_MEMORY = "in_memory"
    CHROMA = "chroma"


class RetrieverTypes:
    SIMILARITY = "similarity"
    MMR = "mmr"


class LLMTypes:
    GROQ = "groq"
    OLLAMA = "ollama"
    GEMINI = "gemini"
    OPENAI = "openai"


class PromptTemplateTypes:
    DEFAULT = "default"


class MemoryTypes:
    CONVERSATION_BUFFER = "conversation_buffer"


class RerankerTypes:
    NONE = "none"
    CROSS_ENCODER = "cross_encoder"