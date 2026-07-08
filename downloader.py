import yt_dlp
import os


def download_video(url: str, path: str) -> str | None:
    os.makedirs(path, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmple': f'{path}%(title)s.%(ext)s',
        'quiet': True,
        'merge_output_forma': 'mp4',
    }
    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

    except Exception as e:
        print(f"Error downloading video : {e}")
        return None


def download_audio(url: str, paht: str) -> str | None:
    os.makedirs(paht, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{paht}%(title)s.%(ext)s',
        'quiet': True,
    }
    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            base, _ = os.path.splitext(filename)
            return base + ".mp3"
    except Exception as e:
        print(f'Error downloading audio')
        return None
