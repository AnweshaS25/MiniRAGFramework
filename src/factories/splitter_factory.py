from src.splitters.character_text_splitter import CharacterTextSplitter
from src.splitters.recursive_text_splitter import RecursiveTextSplitter
from src.splitters.token_text_splitter import TokenTextSplitter

from src.constants import SplitterTypes

class SplitterFactory:
    """
    Factory class for creating text splitters.
    """

    @staticmethod
    def create(splitter_type: str):
        """
        Creates and returns the requested splitter.
        """

        # Handle recursive splitter
        if splitter_type == SplitterTypes.RECURSIVE:
            return RecursiveTextSplitter()

        # Handle character splitter
        elif splitter_type == SplitterTypes.CHARACTER:
            return CharacterTextSplitter()

        # Handle token splitter
        elif splitter_type == SplitterTypes.TOKEN:
            return TokenTextSplitter()

        raise ValueError(
            f"Unsupported splitter type: {splitter_type}"
        )
        
        #Handle recursive splitter
        # if SplitterTypes.RECURSIVE:
        #     return RecursiveTextSplitter()
        
        # #Handle character splitter
        # elif SplitterTypes.CHARACTER:
        #     return CharacterTextSplitter()
        
        # elif splitter_type.TOKEN_TEXT_SPLITTER:
        #     return TokenTextSplitter()
        