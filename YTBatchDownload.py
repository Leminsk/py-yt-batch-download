import youtube_dl

file_name = "links.txt"
output_folder = "output"

error_urls = []

def downloadMP3(video_url):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url, download=False
    )
    
    options={
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': f"{output_folder}/%(title)s.mp3",
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])


def isValidURLList(error_url_list):
    invalid_errors = ['DownloadError']

    for error_url in error_url_list:
        if(error_url[0] not in invalid_errors):
            return True
        
    return False

# download from "links.txt"
with open(file_name) as file:
    for line in file:
        if(line.startswith("https")):
            video_url = line.rstrip()
            
            try:
                downloadMP3(video_url)

            except Exception as e:
                print("--------------------------------------------------")
                print("Error with URL: ", video_url)
                print(e)
                print("--------------------------------------------------")
                error_urls.append([type(e).__name__, video_url])

if(len(error_urls) > 0):
    print("SOME URL's FAILED!")
    print("RETRYING...")

    # retry downloading
    while(len(error_urls) > 0 and isValidURLList(error_urls)):

        itemsToDelete = []

        for i in range(len(error_urls)):
            video_url = error_urls[i][1]
            try:
                downloadMP3(video_url)
                itemsToDelete.append(i)
            except Exception as e:
                    print("--------------------------------------------------")
                    print("Error with URL: ", video_url)
                    print(e)
                    print("--------------------------------------------------")
            
        for i in itemsToDelete:
            del error_urls[i]

        
    if(len(error_urls) > 0):
        print("These URL's are troublesome:")
        for e in error_urls:
            print(e)