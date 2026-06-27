from src.core.document import Document
from src.splitters.code_splitter import CodeSplitter


document = Document(
    content="""
import os

class UserService:

    def login(self):
        pass

    def register(self):
        pass


def helper():
    pass
""",
    metadata={
        "source": "user_service.py",
    },
)

splitter = CodeSplitter()

chunks = splitter.split(
    [document],
)

print("=" * 60)
print("Code Splitter Test")
print("=" * 60)

for index, chunk in enumerate(
    chunks,
    start=1,
):

    print()

    print(f"Chunk {index}")

    print("-" * 60)

    print(chunk.content)

    print("-" * 60)