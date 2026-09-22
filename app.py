import streamlit as st
from faster_whisper import WhisperModel
import tempfile
import os

st.title("Il mio Trascrittore Audio 🎙️")
st.write("Carica il tuo file audio e io lo scriverò per te!")

# Carica il motore Turbo (velocissimo!)
@st.cache_resource
def load_model():
    return WhisperModel("tiny", device="cpu", compute_type="int8")

model = load_model()

audio_file = st.file_uploader("Carica l'audio qui", type=["m4a", "mp3", "wav"])

if audio_file is not None:
    if st.button("Trascrivi!"):
        st.write("Sto ascoltando... vedrai le parole apparire qui sotto man mano che le capisco!")
        
        # Salviamo il file momentaneamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        
        # Creiamo una scatola vuota dove far apparire il testo in diretta
        scatola_testo = st.empty()
        testo_completo = ""
        
        try:
            # L'IA inizia ad ascoltare
            segments, info = model.transcribe(tmp_path, language="it")
            
            # Scriviamo ogni frase appena la sente!
            for segment in segments:
                testo_completo += segment.text + " "
                scatola_testo.info(testo_completo)
            
            st.success("Finito!")
            
        except Exception as e:
            st.error(f"Errore: {e}")
            
        finally:
            os.remove(tmp_path)
