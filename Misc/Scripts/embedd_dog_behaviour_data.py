from pytidb import TiDBClient
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pytidb.rerankers import Reranker
from dotenv import load_dotenv

load_dotenv()


# ── CONFIG ────────────────────────────────────────────────────────────────
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASS = os.getenv("TIDB_PASS")
TIDB_PORT = os.getenv("TIDB_PORT")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")
JINA_AI_API_KEY = os.getenv("JINA_AI_API_KEY")
# ── END CONFIG ────────────────────────────────────────────────────────────


TIDB_DATABASE_URL=f"mysql+pymysql://{TIDB_USER}:{TIDB_PASS}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DATABASE}?ssl_ca=/etc/ssl/cert.pem"

db = TiDBClient.connect(TIDB_DATABASE_URL)

text_embed = EmbeddingFunction(
    model_name="jina_ai/jina-embeddings-v3",
    api_key=JINA_AI_API_KEY,
    timeout=60
)

class DogBehaviourData(TableModel, table=True):
    __tablename__ = "dog_behaviour_data"

    id: int = Field(primary_key=True)
    content: str = Field()
    content_vec: list[float] = text_embed.VectorField(
        source_field="content"
    )


# table = db.create_table(schema=DogBehaviourData, if_exists='skip')
# table.create_fts_index("content")

table = db.open_table("dog_behaviour_data")

print("Connected to TiDB database and created table!")

def load_pdf_text(pdf_path: str) -> str:
    """Read the full text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 200, chunk_overlap: int = 100):
    """Split text into overlapping chunks for embeddings."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return text_splitter.split_text(text)

pdf_path = "../Datasets/Dog_Behaviour_Data.pdf"
full_text = load_pdf_text(pdf_path)

chunks = chunk_text(full_text)

chunk_data_objects = []
random_id = 1214

for chunk in chunks:
    chunk_data_objects.append(DogBehaviourData(
        id = random_id,
        content = chunk
    ))
    random_id += 1

table.bulk_insert(chunk_data_objects)

print("Inserted the data into the table!")

reranker_model = Reranker(
    model_name="jina_ai/jina-reranker-m0", api_key=JINA_AI_API_KEY,
    timeout=60
)


df = (
    table.search("Is kennel cough deadly for my dog?", search_type="hybrid")
    .rerank(reranker_model, "content")
    .limit(5)
    .text_column("content")
    .to_list()
)

print("Dataframe is: ", df)

merged_content = "\n\n".join(data["content"] for data in df)

print("Merged Content is:", merged_content)
