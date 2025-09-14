from pytidb import TiDBClient
from pytidb.schema import TableModel, Field, VectorField, DistanceMetric
from pytidb.embeddings import EmbeddingFunction
from pytidb.rerankers import Reranker
import tensorflow_hub as hub
import os
from google.adk.agents.callback_context import CallbackContext
from typing import List, Optional
from google.adk.agents import Agent
from google.adk.tools import google_search
import certifi


# ── CONFIG ────────────────────────────────────────────────────────────────
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASS = os.getenv("TIDB_PASS")
TIDB_PORT = os.getenv("TIDB_PORT")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")
JINA_AI_API_KEY = os.getenv("JINA_AI_API_KEY")
# ── END CONFIG ────────────────────────────────────────────────────────────


TIDB_DATABASE_URL=f"mysql+pymysql://{TIDB_USER}:{TIDB_PASS}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DATABASE}?ssl_ca={certifi.where()}"

db = TiDBClient.connect(TIDB_DATABASE_URL)

BASE_DIR = os.path.dirname(__file__)

yamnet_path = os.path.join(BASE_DIR, "yamnet")
yamnet_model = hub.load(yamnet_path)

text_embed = EmbeddingFunction(
    model_name="jina_ai/jina-embeddings-v3",
    api_key=JINA_AI_API_KEY,
    timeout=90
)

image_embed = EmbeddingFunction(
    model_name="jina_ai/jina-embeddings-v4",
    api_key=JINA_AI_API_KEY,
    multimodal=True,
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


class Users(TableModel, table=True):
    __tablename__ = "auth_user"

    id: int =  Field(primary_key=True)
    password: str = Field()
    last_login: str = Field()
    is_superuser: int = Field()
    username: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    email: str = Field()
    is_staff: int = Field()
    is_active: int = Field()
    date_joined: str = Field()


class PetWeeklyHistoryCache(TableModel, table=True):
    __tablename__ = "pet_weekly_history_cache"

    pet_id: str = Field(primary_key=True)
    information: str = Field()


class PetExpressionsIdentification(TableModel, table=True):
    __tablename__ = "pet_expression_identification"

    id: int = Field(primary_key=True)
    expression_identification: str = Field()
    image_uri: str = Field()
    image_vec: Optional[List[float]] = image_embed.VectorField(
            distance_metric=DistanceMetric.L2,
            source_field="image_uri",
            source_type="image",
        )
    
class DogSkinDiseaseDetection(TableModel, table=True):
    __tablename__ = "dog_skin_disease_detection"

    id: int = Field(primary_key=True)
    skin_disease: str = Field()
    image_uri: str = Field()
    image_vec: Optional[List[float]] = image_embed.VectorField(
            distance_metric=DistanceMetric.L2,
            source_field="image_uri",
            source_type="image",
        )

class CatSkinDiseaseDetection(TableModel, table=True):
    __tablename__ = "cat_skin_disease_detection"

    id: int = Field(primary_key=True)
    skin_disease: str = Field()
    image_uri: str = Field()
    image_vec: Optional[List[float]] = image_embed.VectorField(
            distance_metric=DistanceMetric.L2,
            source_field="image_uri",
            source_type="image",
        )


search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="Specialist agent for web search",
    instruction="Use Google Search to fetch information for the given query.",
    tools=[google_search],
    output_key="search_results",
)


reranker_model = Reranker(
    model_name="jina_ai/jina-reranker-m0", api_key=JINA_AI_API_KEY,
    timeout=60
)


def get_table(table_name):
    try:
        current_table = db.open_table(table_name)
    except Exception as e:
        reconnect_db()
        current_table = db.open_table(table_name)
    return current_table


def save_pet_weekly_history_cache(callback_context:CallbackContext, info: str):
    table = get_table("pet_weekly_history_cache")
    pet_id = callback_context.state["pet_information"]["pet_id"]
    existing_row = table.get(pet_id)
    user_query = callback_context.user_content.parts[0].text
    if existing_row:
        existing_info = existing_row.information
        info = existing_info + "\n\n User Query: " + user_query + "\n Agent Response: " + info
        table.save({"pet_id": pet_id, "information": info})
        print("Updated data successfully!")
    else:
        table.insert({"pet_id": pet_id, "information": "User Query: " + user_query + "\n" + info})
        print("Inserted data successfully!")
    
    return "Saved data"

def query_db(query):
    try:
        res = db.query(query)
    except Exception as e:
        db = reconnect_db()
        res = db.query(query)
    return res

def reconnect_db():
    global db
    print("Refreshing database connection..")
    db = TiDBClient.connect(TIDB_DATABASE_URL)
    return db