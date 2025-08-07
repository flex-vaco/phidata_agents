from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.pgvector import PgVector
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()

pdf_knowledge_base = PDFKnowledgeBase(
    path=os.getenv("RESUMES_DIR"),
    # Table name: ai.pdf_documents
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
    reader=PDFReader(chunk=True),
)
# pdf_knowledge_base.load(recreate=True, upsert=True)