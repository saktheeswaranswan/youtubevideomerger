import os
import yt_dlp
import shutil

# Create directories for downloads and output
os.makedirs("videos", exist_ok=True)
os.makedirs("converted", exist_ok=True)

# List of YouTube links (Replace these with your 100 links)
youtube_links = [
    "https://www.youtube.com/watch?v=your_video_id1",
    "https://www.youtube.com/watch?v=your_video_id2",
    # Add up to 100 links
]

# yt-dlp options for downloading 1080p 30fps
download_opts = {
    'format': 'bestvideo[height<=1080][fps<=30]+bestaudio/best',
    'outtmpl': 'videos/%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
}

# Download videos
print("Downloading videos...")
with yt_dlp.YoutubeDL(download_opts) as ydl:
    ydl.download(youtube_links)

# Convert videos to 1080p 30fps using CUDA acceleration
print("Converting videos to 1080p 30fps with CUDA...")
converted_videos = []
for file in os.listdir("videos"):
    if file.endswith(".mp4"):
        input_path = f"videos/{file}"
        output_path = f"converted/{file}"
        converted_videos.append(output_path)

        cmd = f"ffmpeg -hwaccel cuda -i \"{input_path}\" -vf \"scale=1920:1080,fps=30\" -c:v h264_nvenc -preset fast -b:v 5000k -c:a aac -strict experimental \"{output_path}\""
        os.system(cmd)

# Create a text file with all converted videos for merging
merge_list_path = "merge_list.txt"
with open(merge_list_path, "w") as f:
    for video in converted_videos:
        f.write(f"file '{video}'\n")

# Merge videos into one MP4 file
output_final = "final_merged_video.mp4"
cmd_merge = f"ffmpeg -hwaccel cuda -f concat -safe 0 -i {merge_list_path} -c:v h264_nvenc -preset fast -b:v 5000k -c:a aac -strict experimental {output_final}"
os.system(cmd_merge)

print("✅ Merging completed! Download 'final_merged_video.mp4'")
