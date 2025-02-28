from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ensure 'uploads' directory exists
os.makedirs("uploads", exist_ok=True)

# ✅ Root endpoint to prevent 404 error
@app.get("/")
async def root():
    return {"message": "Welcome to the AI-powered Offensive Language Detection API!"}

@app.post("/analyze")
async def analyze(
    text: str = Form(None),
    voice_file: UploadFile = File(None),
    youtube_url: str = Form(None)
):
    print("\n🔹 Received Request at /analyze 🔹")  # ✅ Print when request is received
    print(f"Text: {text}")
    print(f"Voice File: {voice_file.filename if voice_file else 'No file'}")
    print(f"YouTube URL: {youtube_url}\n")

    # ✅ Ensure at least one input is provided
    if not text and not voice_file and not youtube_url:
        raise HTTPException(status_code=400, detail="Provide at least one input: text, voice file, or YouTube URL.")

    response_message = []

    if text:
        response_message.append(f"Received text: {text}")

    if voice_file:
        file_path = f"uploads/{voice_file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(voice_file.file, buffer)
        response_message.append(f"Voice file saved: {voice_file.filename}")

    if youtube_url:
        response_message.append(f"Received YouTube URL: {youtube_url}")

    print(f"🔹 Response Sent: {' | '.join(response_message)}\n")  # ✅ Print response before sending

    return {"message": " | ".join(response_message)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # ✅ Use Render's dynamic port
    uvicorn.run(app, host="0.0.0.0", port=port)
