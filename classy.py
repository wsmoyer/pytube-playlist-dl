import argparse
from pytube import Playlist, YouTube
import os


class PlaylistDL:
    def __init__(self):
        self.start_point = None
        self.end_point = None
        self.dl_list = None
        self.playlist = None
        self.download_dir = None
        self.parser = argparse.ArgumentParser(description='A program to download youtube playlists of audio')
        self.init_args()
        self.get_title()
        self.args = self.parser.parse_args()
        self.output_folder = self.args.output_folder
        self.download = None

    def init_args(self):
        self.parser.add_argument("--playlist", help="Playlist to download")
        self.parser.add_argument("--output_folder",default='', help="Folder to store playlist files")
        self.parser.add_argument("--start_point",default=None, help="Where in list to start download")
        self.parser.add_argument("--end_point",default=None, help="Where in list to end download")
        
    def get_start_end_point(self):
        if self.args.start_point is not None:
            self.start_point = int(self.args.start_point) - 1

        if self.args.end_point is not None:
            self.end_point = int(self.args.end_point) - 1
      
    def prompt_input(self):
        self.get_playlist()
        self.download = input(f'will download {len(self.dl_list)} tracks from this playlist. ok? (y/n) ')

    def get_playlist(self):
        self.playlist = Playlist(self.args.playlist)
        self.get_start_end_point()
        self.get_output_folder()
        self.get_dl_list()

    def convert_to_mb(self, size):
        return round(size/1000000, 2)

    def rm_spaces(self, string):
        return string.replace(" ", "")

    
    def get_title(self):
        print('''
        #########################
        music playlist downloader
        #########################
        ''')

    def get_output_folder(self):     
        if self.output_folder == '':
            self.output_folder = self.playlist.title
            self.download_dir = os.path.join(os.getcwd(), self.output_folder)

    def get_dl_list(self):
        if self.start_point is not None and self.end_point is not None:
            self.dl_list = self.playlist.video_urls[self.start_point:self.end_point]
        else:
            self.dl_list = self.playlist.video_urls

    def download_files(self):
        if self.download == 'y':
            for url in self.dl_list:
                video = YouTube(url)
                stream = video.streams.get_by_itag(140)
                filename = self.rm_spaces(stream.default_filename)
                print(f'Downloading {stream.title} {self.convert_to_mb(stream.filesize)} mb')
                stream.download(filename=filename, output_path=self.download_dir)

p = PlaylistDL()
p.prompt_input()
p.download_files()





    
