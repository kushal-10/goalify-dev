from pydantic import BaseModel, Field
from typing import List 
from restack_ai.workflow import workflow 
import pymupdf
import requests
from src.utils.split import split_text_into_chunks
from src.functions.weaviate_client import get_weaviate_client
import weaviate.classes as wvc
from weaviate.util import generate_uuid5


class PdfWorkflowInput(BaseModel):
    file_upload: List[dict] = Field(files=True) 

@workflow.defn()
class PdfWorkflow: 
    @workflow.run
    async def run(self, input: PdfWorkflowInput):
        file = input.file_upload[0]
        filename = str(file['name'])

        response = requests.get(f"{'http://localhost:6233'}/api/download/{filename}")
        response.raise_for_status()  # Raise an error for bad responses
        content = response.content
        
        doc = pymupdf.Document(stream=content)
        
        pdfContent = ""
        for page in doc:
            text = page.get_text()
            pdfContent += text

        chunks = split_text_into_chunks(text=pdfContent)

        client = get_weaviate_client()
        books_collection = client.collections.get("Book")
        
        try:
            with books_collection.batch.dynamic() as batch:
                for index, chunk in enumerate(chunks):
                    book_obj = {
                        "text": chunk,
                        "chunk_id": index
                    }
                    
                    batch.add_object(properties=book_obj, uuid=generate_uuid5(index))

                    print("Batch seeded successfully.")
                    
        finally:
            client.close()
        

        return { "message": "Pdf content inserted to weaviate successfully.", } 


        

        