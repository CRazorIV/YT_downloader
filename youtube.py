from pytubefix import YouTube
def download_vid(save_path, url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        highest_resolution = streams.get_highest_resolution()
        highest_resolution.download(output_path=save_path)
        print("Video download complete!")
    except Exception as e:
        print(e)

url = "https://www.youtube.com/watch?v=74WOClL8t-o"
save_path ='C:/Users/yurik/Documents/GitHub/YT_downloader'

download_vid(save_path, url)

