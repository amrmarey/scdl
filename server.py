from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp
import os
import logging
import urllib.parse
import tempfile
import shutil

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/download")
async def download(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="No URL provided")

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            filename = filename.replace('.webm', '.mp3').replace('.opus', '.mp3')
            logging.info(f"Downloaded file: {filename}")

        if not os.path.isfile(filename):
            logging.error(f"File not found: {filename}")
            raise HTTPException(status_code=404, detail="File not found")

        utf8_filename = os.path.basename(filename)
        encoded_filename = urllib.parse.quote(utf8_filename)

        # Serve the file
        response = FileResponse(
            path=filename,
            media_type='audio/mpeg',
            filename=utf8_filename,
            headers={
                'Content-Disposition': f'attachment; filename*=UTF-8\'\'{encoded_filename}'
            }
        )

        # Add a callback to delete the file after the response has been sent
        @response.background
        async def cleanup():
            os.remove(filename)
            shutil.rmtree(temp_dir)
            logging.info(f"Deleted file: {filename} and cleaned up directory: {temp_dir}")

        return response

    except Exception as e:
        logging.error(f"Error downloading or serving file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")