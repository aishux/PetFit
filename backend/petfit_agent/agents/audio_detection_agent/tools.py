from google.adk.tools import ToolContext
from petfit_agent.setup import *
import numpy as np
import librosa
import soundfile as sf
import io


def extract_yamnet_embedding(audio_bytes):
    # Load audio
    wav, sr = sf.read(io.BytesIO(audio_bytes))
    if wav.ndim > 1:  # Convert stereo to mono
        wav = np.mean(wav, axis=1)
    if sr != 16000:  # YAMNet expects 16kHz
        wav = librosa.resample(wav, orig_sr=sr, target_sr=16000)

    # Run YAMNet
    _, embeddings, _ = yamnet_model(wav)
    # Average over time frames to get a single vector
    clip_embedding = np.mean(embeddings.numpy(), axis=0)
    return clip_embedding


def identify_sound_meaning(tool_context: ToolContext):
    """Tool identify the meaning of the sount."""
    try:
        for part in tool_context.user_content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                blob = part.inline_data
                file_bytes = blob.data

                table = get_table("dog_sound_identification")

                embedding = extract_yamnet_embedding(file_bytes).tolist()

                result = (
                    table.search(embedding, search_type="vector")
                        .distance_metric(DistanceMetric.L2)
                        .limit(1)
                        .to_list()
                )

                return f"Condition Identified is: {result[0]['sound_identification']}"


    except Exception as e:
        print("Exception is: " + str(e))
        return "Couldn't parse your audio file"
    
def get_info_dog_behaviour(query: str):
    table = get_table("dog_behaviour_data")
    df = (
      table.search(query, search_type="hybrid")
        .rerank(reranker_model, "content")
        .limit(5)
        .text_column("content")
        .to_list()
    )

    merged_content = "\n\n".join(data["content"] for data in df)
    return merged_content