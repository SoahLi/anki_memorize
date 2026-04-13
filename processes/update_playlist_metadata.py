import subprocess


def update_playlist_metadata():
    command = 'yt-dlp --cookies-from-browser chrome --playlist-end 5 --print "%(title)s" :ythistory -v'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout.strip()
        lines = output.split("\n")
        for line in lines:
            print(line)
    else:
        print(f"Error: {result.stderr.strip()}")
