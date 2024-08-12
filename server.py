import os
import shutil
import tempfile
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
import yt_dlp as youtube_dl
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

def purge_temp_folder(temp_dir):
    """Delete all files in the temporary downloads directory."""
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error(f'Failed to delete {file_path}. Reason: {e}')

@app.get("/download")
async def download_file(request: Request, url: str):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Purge temp directory before starting a new download
        purge_temp_folder(temp_dir)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                mp3_filename = os.path.splitext(filename)[0] + '.mp3'
                if not os.path.exists(mp3_filename):
                    raise HTTPException(status_code=404, detail="File not found")
                logging.info(f'Downloaded file: {mp3_filename}')
                return FileResponse(mp3_filename, filename=os.path.basename(mp3_filename))
            except Exception as e:
                logging.error(f"Error downloading or serving file: {e}")
                raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
