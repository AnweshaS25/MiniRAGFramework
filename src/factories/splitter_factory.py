from src.splitters.character_text_splitter import CharacterTextSplitter
from src.splitters.recursive_text_splitter import RecursiveTextSplitter

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
        
        #Handle recursive splitter
        if SplitterTypes.RECURSIVE:
            return RecursiveTextSplitter()
        
        #Handle character splitter
        if SplitterTypes.CHARACTER:
            return CharacterTextSplitter()
        
        raise ValueError(
            f"Unsupported splitter type: {splitter_type}"
        )