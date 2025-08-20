from pytidb import TiDBClient
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.rerankers import Reranker
import os
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
    api_key=JINA_AI_API_KEY
)

class SymptomRemediation(TableModel, table=True):
    __tablename__ = "symptom_remediation"

    id: int = Field(primary_key=True)
    owner_observation_notes: str = Field()
    clinical_notes: str = Field()
    prescriptions: str = Field()
    level_of_criticality: str = Field()
    owner_observation_notes_vec: list[float] = text_embed.VectorField(
        source_field="owner_observation_notes"
    )

# def csv_to_object_list(csv_file, batch_size=50):
#     with open(csv_file, newline='') as csvfile:
#         reader = list(csv.reader(csvfile))
#         rows = reader[1:]

#     object_lists = []
#     curr_list = []
#     count = 0
#     header = reader[0]
#     id_idx = header.index("id")
#     obs_notes_idx = header.index("Owner Observation Notes")
#     clinical_notes_idx = header.index("Clinical Notes")
#     prescriptions_idx = header.index("Prescriptions")
#     criticality_idx = header.index("Level of Criticality")

#     for row in rows:
#         curr_list.append(SymptomRemediation(
#             id = row[id_idx],
#             owner_observation_notes = row[obs_notes_idx],
#             clinical_notes = row[clinical_notes_idx],
#             prescriptions = row[prescriptions_idx],
#             level_of_criticality = row[criticality_idx]
#         ))
#         count += 1
#         if count == batch_size:
#             object_lists.append(curr_list)
#             curr_list = []
#             count = 0

#     if curr_list != []:
#         object_lists.append(curr_list)
    
#     return object_lists


# table = db.create_table(schema=SymptomRemediation)

# print("Connected to TiDB database and created table!")

# table.create_fts_index("owner_observation_notes")

# print("Created Full Text Search Index")

# object_list_of_lists = csv_to_object_list("../Datasets/pet_symptoms_remediation_dataset_deduped.csv")

# print("Converted data to table object!")

# table.bulk_insert(object_list_of_lists[0])

# print("Inserted the data into the table!")



table = db.open_table("symptom_remediation")

jinaai = Reranker(model_name="jina_ai/jina-reranker-m0", api_key=JINA_AI_API_KEY)

df = (
  table.search("My dog is having irritation in his ears and moves his head as if he is dizzy", search_type="hybrid")
    .rerank(jinaai, "owner_observation_notes")
    .limit(3)
    .text_column("owner_observation_notes")
    .to_pandas()
)

print(df)