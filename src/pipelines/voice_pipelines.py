import streamlit as st
from resemblyzer import VoiceEncoder, preprocess_wav
import io
import librosa
import numpy as np

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr = 16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error('Voice Recognition Error')
        return None
    
def indentify_results(new_embed, candidate_dict, threshold = 0.65):
    if new_embed is None or not candidate_dict:
        return None, 0.0
    
    best_id = None
    best_score = -1.0

    for sid, stored_embedding in candidate_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embed, stored_embedding)
            if similarity> best_score:
                best_score = similarity
                best_id = sid

    if best_score >= threshold:
        return best_id, best_score
    return None, best_score

def process_bulk_audio(audio_bytes, candidates_dict, threshold = 0.65):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr = 16000)
        segments = librosa.effects.split(audio, top_db = 30)

        identified_results = {}

        for start, end in segments:
            if(end-start)<sr *0.5:
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = indentify_results(embedding, candidates_dict, threshold)

            if sid:
                if sid not in indentify_results or score> identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except Exception as e:
        st.error('Bulk Process Error')
        return {}




    