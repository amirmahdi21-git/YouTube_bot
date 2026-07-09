import yt_dlp
import os


def download_video(url: str, path: str = "downloads/") -> str | None:
    os.makedirs(path, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{path}%(title)s.%(ext)s',
        'quiet': True,
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            final_path = base + ".mp4"
            return final_path if os.path.exists(final_path) else filename
    except Exception as e:
        print(f"Error downloading video : {e}")
        return None


def download_audio(url: str, path: str = "downloads/") -> str | None:
    os.makedirs(path, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{path}%(title)s.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            return base + ".mp3"
    except Exception as e:
        print(f'Error downloading audio: {e}')
        return None
