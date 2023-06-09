from langchain.document_loaders.unstructured import UnstructuredFileLoader
from typing import List
from pathlib import Path
import re
from langchain.docstore.document import Document

class StructuredMarkdownLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        # from unstructured.__version__ import __version__ as __unstructured_version__
        # #from unstructured.partition.md import partition_md

        # # NOTE(MthwRobinson) - enables the loader to work when you're using pre-release
        # # versions of unstructured like 0.4.17-dev1
        # _unstructured_version = __unstructured_version__.split("-")[0]
        # unstructured_version = tuple([int(x) for x in _unstructured_version.split(".")])
        
        # if unstructured_version < (0, 4, 16):
        #     raise ValueError(
        #         f"You are on unstructured version {__unstructured_version__}. "
        #         "Partitioning markdown files is only supported in unstructured>=0.4.16."
        #     )
            
        filename = self.file_path 
        docs = []
        
        if filename.endswith(".md"):
            print(filename) #check the loading file
            path = Path(filename)  
            content = path.read_text()
            sections = self.extract_sections(content)
            for section in sections:
                new_doc = Document(page_content=section.strip(),metadata = {'source':filename}) # the source is used for repeated file check
                docs.append(new_doc)
        return docs 
    
    @staticmethod
    def extract_sections(content: str) -> list:
        pattern = r"\n## |\n### |\n#### |\Z"
        sections = re.split(pattern, content)
        sections = [s.strip() for s in sections if s.strip()]
        return sections
