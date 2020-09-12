# Youtuber

This script downloads mp3s from youtube to a directory from a csv list.

It uses the python package youtube-dl
https://github.com/ytdl-org/youtube-dl/


## Install Instructions

1. Clone Repo to directory

2. Create Conda Env
   1. Install packages requirements.txt


3. Generate CSV
- Format should be 3 columns No Headers
- TITLE, ARTIST, YOUTUBE LINK

```csv
Star,Bazzi,https://www.youtube.com/watch?v=7gAzkZGuCgE
The Box,Roddy Ricch,https://www.youtube.com/watch?v=uLHqpjW3aDs
Dreams,Bazzi,https://www.youtube.com/watch?v=X-0yVxcb__M
I Mean It,G-Eazy (ft. Remo),https://www.youtube.com/watch?v=4MjSoquXAZ4
```

4. Execute Script
   - Will auto generate destination directory
   > python downloader.py [CSV_PATH].csv [DIR_PATH]
