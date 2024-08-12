from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp
import os
import logging
import urllib.parse

# Initialize the FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.get("/", response_class=HTMLResponse)
async def home():
    # Serve the index.html file
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/download")
async def download(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="No URL provided")

    # Ensure the downloads directory exists
    os.makedirs('downloads', exist_ok=True)

    # Using yt-dlp to download the file as an MP3
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            filename = filename.replace('.webm', '.mp3').replace('.opus', '.mp3')  # Ensure filename ends with .mp3
            logging.info(f"Downloaded file: {filename}")
        
        # Check if the file exists
        if not os.path.isfile(filename):
            logging.error(f"File not found: {filename}")
            raise HTTPException(status_code=404, detail="File not found")

        # Encode the filename for the Content-Disposition header
        utf8_filename = os.path.basename(filename)
        encoded_filename = urllib.parse.quote(utf8_filename)
        
        # Serve the file with the correct headers
        return FileResponse(
            path=filename,
            media_type='audio/mpeg',
            headers={
                'Content-Disposition': f'attachment; filename*=UTF-8\'\'{encoded_filename}'
            }
        )

    except Exception as e:
        logging.error(f"Error downloading or serving file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
