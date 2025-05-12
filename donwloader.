import os
import requests
from pytube import YouTube
from tiktok_downloader import TikTokDownloader
from instaloader import Instaloader
from facebook_scraper import get_posts

def download_youtube(url, output_path):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_audio=True).first()
        output_file = video_stream.download(output_path=output_path)
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)
        return new_file
    except Exception as e:
        raise Exception(f"Error downloading YouTube video: {str(e)}")

def download_tiktok(url, output_path):
    try:
        tiktok = TikTokDownloader()
        video_url = tiktok.get_video_url(url)
        response = requests.get(video_url)
        file_path = os.path.join(output_path, "tiktok.mp4")
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    except Exception as e:
        raise Exception(f"Error downloading TikTok video: {str(e)}")

def download_instagram(url, output_path):
    try:
        loader = Instaloader()
        post = loader.download_post(url, target=output_path)
        return post
    except Exception as e:
        raise Exception(f"Error downloading Instagram post: {str(e)}")

def download_facebook(url, output_path):
    try:
        for post in get_posts(post_urls=[url], options={"videos": True}):
            video_url = post['video']
            response = requests.get(video_url)
            file_path = os.path.join(output_path, "facebook.mp4")
            with open(file_path, "wb") as file:
                file.write(response.content)
            return file_path
    except Exception as e:
        raise Exception(f"Error downloading Facebook video: {str(e)}")
