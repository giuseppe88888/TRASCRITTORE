import streamlit as st
from groq import Groq
import os
import tempfile

st.title("Il mio Trascrittore Audio 🎙️")
st.write("Versione Super-Veloce e Perfetta 🚀")

# Chiediamo la chiave magica
chiave = st.text_input("Incolla qui il tuo Pass Speciale (API Key) di Groq:", type="password")

audio_file = st.file_uploader("Carica l'audio qui", type=["m4a", "mp3", "wav"])

if audio_file is not None and chiave:
    if st.button("Trascrivi!"):
        st.write("Sto spedendo l'audio al Super-Computer... aspetta pochi secondi!")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name

        try:
            # Svegliamo il Super-Computer con la nostra chiave
            client = Groq(api_key=chiave)

            # Spediamo l'audio
            with open(tmp_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                  file=(os.path.basename(tmp_path), file.read()),
                  model="whisper-large-v3", # Il cervello più intelligente del mondo
                  language="it",
                )

            st.success("Finito!")
            # Mostriamo il testo perfetto!
            st.text_area("Testo Trascritto:", transcription.text, height=350)

        except Exception as e:
            st.error(f"C'è stato un problema: {e}")

        finally:
            os.remove(tmp_path)
