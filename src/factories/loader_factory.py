from src.loaders.pdf_loader import PDFLoader

class LoaderFactory:
    """
    Factory class for creating document loaders.
    """

    @staticmethod
    def create(loader_type: str, **kwargs,):

        if loader_type == "pdf":
            return PDFLoader(
                kwargs["file_path"]
            )
        
        raise ValueError(
            f"Unsupported loader type: {loader_type}"
        )