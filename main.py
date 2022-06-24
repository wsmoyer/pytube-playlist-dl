import argparse
from re import A
from pytube import Playlist, YouTube
import os

def convert_to_mb(size):
    return round(size/1000000, 2)


def rm_spaces(string):
    return string.replace(" ", "")


parser = argparse.ArgumentParser(description='A program to download youtube playlists of audio')
parser.add_argument("--playlist", help="Playlist to download")
parser.add_argument("--output_folder",default='', help="Folder to store playlist files")

parser.add_argument("--start_point",default=0, help="Where in list to start download")

parser.add_argument("--end_point",default=0, help="Where in list to end download")

args = parser.parse_args()

if args.start_point != 0:
    start_point = int(args.start_point) - 1
else:
    start_point = 0

if args.end_point != 0:
    end_point = int(args.end_point) - 1
else:
    end_point = 0

output_folder = args.output_folder

p = Playlist(args.playlist)


if output_folder == '':
    output_folder = p.title


download_dir = os.path.join(os.getcwd(), output_folder)

print('''
#########################
music playlist downloader
#########################
''')

download = input(f'will download {p.length} tracks fron this playlist. ok? (y/n) ')

print(p.video_urls)


if start_point != 0 and end_point != 0:
    dl_list = p.video_urls[start_point:end_point]
else:
    dl_list = p.video_urls
    

if download == 'y':

    for url in dl_list:
        video = YouTube(url)
        stream = video.streams.get_by_itag(140)
        filename = rm_spaces(stream.default_filename)
        print(f'Downloading {stream.title} {convert_to_mb(stream.filesize)} mb')
        stream.download(filename=filename, output_path=download_dir)

        