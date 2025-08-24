from pytidb import TiDBClient
from pytidb.schema import TableModel, Field, VectorField, DistanceMetric
from pytidb.embeddings import EmbeddingFunction
from pytidb.rerankers import Reranker
import tensorflow_hub as hub
import os
from google.adk.agents.callback_context import CallbackContext


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

yamnet_model = hub.load("petfit_agent/yamnet")

text_embed = EmbeddingFunction(
    model_name="jina_ai/jina-embeddings-v3",
    api_key=JINA_AI_API_KEY,
    timeout=90
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

class DogSoundIdentification(TableModel, table=True):
    __tablename__ = "dog_sound_identification"

    id: int = Field(primary_key=True)
    sound_identification: str = Field()
    audio_vector: list[float] = VectorField(dimensions=1024, distance_metric=DistanceMetric.L2)

class DogBehaviourData(TableModel, table=True):
    __tablename__ = "dog_behaviour_data"

    id: int = Field(primary_key=True)
    content: str = Field()
    content_vec: list[float] = text_embed.VectorField(
        source_field="content"
    )

class Pets(TableModel, table=True):
    __tablename__ = "Pets"

    pet_id: str = Field(primary_key=True)
    pet_type: str = Field()
    gender: str = Field()
    age: int = Field()
    name: str = Field()
    owner_id: int = Field()


class PetWeeklyHistoryCache(TableModel, table=True):
    __tablename__ = "pet_weekly_history_cache"

    pet_id: str = Field(primary_key=True)
    information: str = Field()


reranker_model = Reranker(
    model_name="jina_ai/jina-reranker-m0", api_key=JINA_AI_API_KEY,
    timeout=60
)


def get_table(table_name):
    return db.open_table(table_name)


def save_pet_weekly_history_cache(callback_context:CallbackContext, info: str):
    table = get_table("pet_weekly_history_cache")
    pet_id = callback_context.state["pet_information"]["pet_id"]
    existing_row = table.get(pet_id)
    if existing_row:
        existing_info = existing_row.information
        info = existing_info + "\n\n" + info
        table.save({"pet_id": pet_id, "information": info})
        print("Updated data successfully!")
    else:
        table.insert({"pet_id": pet_id, "information": info})
        print("Inserted data successfully!")
    
    return "Saved data"