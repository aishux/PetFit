import tensorflow_hub as hub
import numpy as np
import librosa
import soundfile as sf

from pytidb import TiDBClient
from pytidb.schema import TableModel, Field, VectorField, DistanceMetric
import os
from dotenv import load_dotenv

load_dotenv()


# ── CONFIG ────────────────────────────────────────────────────────────────
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASS = os.getenv("TIDB_PASS")
TIDB_PORT = os.getenv("TIDB_PORT")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")
# ── END CONFIG ────────────────────────────────────────────────────────────


TIDB_DATABASE_URL=f"mysql+pymysql://{TIDB_USER}:{TIDB_PASS}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DATABASE}?ssl_ca=/etc/ssl/cert.pem"

db = TiDBClient.connect(TIDB_DATABASE_URL)


class DogSoundIdentification(TableModel, table=True):
    __tablename__ = "dog_sound_identification"

    id: int = Field(primary_key=True)
    sound_identification: str = Field()
    audio_vector: list[float] = VectorField(dimensions=1024, distance_metric=DistanceMetric.L2)

table = db.create_table(schema=DogSoundIdentification)

print("Connected to TiDB database and created table!")

# Load YAMNet
yamnet_model_handle = '../Model/yamnet'
yamnet_model = hub.load(yamnet_model_handle)

print("Loaded the Yamnet Model..")

def extract_yamnet_embedding(audio_path):
    # Load audio
    wav, sr = sf.read(audio_path)
    if wav.ndim > 1:  # Convert stereo to mono
        wav = np.mean(wav, axis=1)
    if sr != 16000:  # YAMNet expects 16kHz
        wav = librosa.resample(wav, orig_sr=sr, target_sr=16000)

    # Run YAMNet
    scores, embeddings, spectrogram = yamnet_model(wav)
    # Average over time frames to get a single vector
    clip_embedding = np.mean(embeddings.numpy(), axis=0)
    return clip_embedding


def process_audio_dataset(dataset_dir="../Datasets/AudioData/Dogs"):
    audio_object_list = []
    count = 1213
    for root, dirs, files in os.walk(dataset_dir):
        if "test" not in root:
            for file in files:
                if file.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
                    audio_path = os.path.join(root, file)
                    dir_name = os.path.basename(root)
                    print(f"Processing file: {audio_path} in directory: {dir_name}")
                    embedding = extract_yamnet_embedding(audio_path)
                    audio_object_list.append(DogSoundIdentification(
                        id=count,
                        sound_identification=dir_name,
                        audio_vector=embedding
                    ))
                    count += 1
    return audio_object_list


object_list_for_audios = process_audio_dataset()

table.bulk_insert(object_list_for_audios)

print("Inserted the data into the table!")


table = db.open_table("dog_sound_identification")

kennel_cough_test_embedding = extract_yamnet_embedding("../Datasets/AudioData/Dogs/test/KennelCough/kennel_cough_5.wav").tolist()

reverse_sneezing_test_embedding = extract_yamnet_embedding("../Datasets/AudioData/Dogs/test/ReverseSneezing/dog_reverse_sneezing_3.wav").tolist()

results1 = (
    table.search(kennel_cough_test_embedding, search_type="vector")
        .distance_metric(DistanceMetric.COSINE)
        .limit(1)
        .to_list()
)

results2 = (
    table.search(reverse_sneezing_test_embedding, search_type="vector")
        .distance_metric(DistanceMetric.COSINE)
        .limit(1)
        .to_list()
)

print("===============================")
print("Result 1:")
print(results1)
print("===============================")

print("===============================")
print("Result 2:")
print(results2)
print("===============================")