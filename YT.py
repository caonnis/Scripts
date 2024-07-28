import os
import yt_dlp

def download_youtube_video(url, output_dir='downloads'):
    """
    Downloads a YouTube video from the given URL and saves it to the specified output directory.

    Args:
        url (str): The URL of the YouTube video to download.
        output_dir (str, optional): The directory to save the downloaded video. Defaults to 'downloads'.

    Raises:
        Exception: If an error occurs during the download process.
    """
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Set up the yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        }

        # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"Video downloaded successfully!")
    except Exception as e:
        print(f"Error downloading video: {e}")

# Example usage
video_url = "https://www.youtube.com/shorts/D2VWwUsc79I"
download_youtube_video(video_url)