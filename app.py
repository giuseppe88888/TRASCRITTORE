import streamlit as st
import whisper
import tempfile
import os

st.title("Il mio Trascrittore Audio 🎙️")
st.write("Carica il tuo file audio e io lo scriverò per te!")

# Carica il "cervello" dell'IA (usiamo la versione 'tiny' che è la più veloce per iniziare)
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

model = load_model()

audio_file = st.file_uploader("Carica l'audio qui", type=["m4a", "mp3", "wav"])

if audio_file is not None:
    if st.button("Trascrivi!"):
        st.write("Sto ascoltando e scrivendo... attendi!")
        
        # Salviamo il file momentaneamente sul computer per farlo leggere all'IA
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        
        # L'IA fa la magia
        result = model.transcribe(tmp_path, language="it")
        
        st.success("Finito!")
        st.write(result["text"])
        
        # Puliamo il file temporaneo
        os.remove(tmp_path)