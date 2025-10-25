import whisper


# load once
_model = whisper.load_model("small")




def transcribe_audio(path: str) -> str:
res = _model.transcribe(path)
return res.get("text", "")
