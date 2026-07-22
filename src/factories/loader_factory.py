from src.loaders.pdf_loader import PDFLoader
from src.loaders.docx_loader import DOCXLoader
from src.loaders.txt_loader import TXTLoader
from src.loaders.csv_loader import CSVLoader
from src.loaders.markdown_loader import MarkdownLoader
from src.loaders.html_loader import HTMLLoader
from src.loaders.web_loader import WebLoader

from src.constants import LoaderTypes

class LoaderFactory:
    """
    Factory class for creating document loaders.
    """

    @staticmethod
    def create(loader_type: str, **kwargs):

        if loader_type == LoaderTypes.PDF:
            return PDFLoader(
                kwargs["file_path"]
            )

        elif loader_type == LoaderTypes.DOCX:
            return DOCXLoader(
                kwargs["file_path"]
            )

        elif loader_type == LoaderTypes.TXT:
            return TXTLoader(
                kwargs["file_path"]
            )

        elif loader_type == LoaderTypes.CSV:
            return CSVLoader(
                kwargs["file_path"]
            )

        elif loader_type == LoaderTypes.MARKDOWN:
            return MarkdownLoader(
                kwargs["file_path"]
            )

        elif loader_type == LoaderTypes.HTML:
            return HTMLLoader(
                kwargs["file_path"]
            )

        elif loader_type == LoaderTypes.WEB:
            return WebLoader(
                kwargs["url"]
            )

        raise ValueError(
            f"Unsupported loader type: {loader_type}"
        )