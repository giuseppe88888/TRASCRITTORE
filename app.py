import streamlit as st
from groq import Groq
import os
import tempfile

# Titolo pulito e semplice
st.title("🎙️ Trascrittore Audio")
st.write("Carica il tuo file audio e ottieni subito la trascrizione perfetta.")

# L'app prende la chiave in automatico dal cassetto segreto
try:
    chiave = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("Attenzione: non hai configurato il 'cassetto segreto' (Secrets) su Streamlit!")
    chiave = None

audio_file = st.file_uploader("Scegli il file audio (.m4a, .mp3, .wav)", type=["m4a", "mp3", "wav"])

if audio_file is not None and chiave:
    # Mostra il lettore audio per riascoltarlo se vuoi
    st.audio(audio_file)
    
    if st.button("🚀 Avvia Trascrizione"):
        with st.spinner("Elaborazione in corso sul Super-Computer..."):
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
                
            try:
                client = Groq(api_key=chiave)
                
                with open(tmp_path, "rb") as file:
                    transcription = client.audio.transcriptions.create(
                      file=(os.path.basename(tmp_path), file.read()),
                      model="whisper-large-v3",
                      language="it",
                    )
                
                st.success("Fatto! Ecco il testo trascritto:")
                
                # Qui usiamo un riquadro speciale che ha già un tasto "Copia" in alto a destra
                st.code(transcription.text, language=None)
                
            except Exception as e:
                st.error(f"Si è verificato un errore: {e}")
                
            finally:
                os.remove(tmp_path)
