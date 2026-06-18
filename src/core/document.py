from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass    #Decorator - the following class is mainly for storing data, due to this Python automatically creates useful methods like: __init__(), __repr__(), __eq__()
class Document:
    """
    Represents a document or a part of a document.
    """

    content: str #Every Document must have a field called content, and it must be a string
    metadata: Dict[str, Any] = field(default_factory=dict) #default_factory=dict => whenever we create a new document, make a brand new empty dictionary, so that the same dictionary wouldnt be used by every document instance. 

    def __repr__(self):
        preview = self.content[:60].replace("\n", " ")
        return f"Document(content='{preview}...', metadata={self.metadata})"