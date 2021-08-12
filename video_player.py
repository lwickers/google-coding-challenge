"""A video player class."""

from .video_library import VideoLibrary
import random

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._currently_playing = None #stores the video being played
        self._paused = None #stores a paused video
        self._playlists = {}
        self._flagged = {}

    def number_of_videos(self):
        """Returns number of videos"""
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")


    def show_all_videos(self):
        """Returns all videos."""
        videos_list = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")
        for x in videos_list:
            if x.video_id in self._flagged.keys():
                print(" ", x, "- FLAGGED (reason:", self._flagged[x.video_id] + ")")
            else:
                print(" ", x)

    def play_video(self, video_id): #come back to this for currently playing video
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        video_to_watch = self._video_library.get_video(video_id)
        if video_to_watch == None:
            print("Cannot play video: Video does not exist")
        elif video_to_watch.video_id in self._flagged.keys():
            print("Cannot play video: Video is currently flagged (reason:",
                  self._flagged[video_to_watch.video_id] + ")")
        else:
            if self._currently_playing != None:
                self.stop_video()
            elif self._paused != None:
                self.stop_video()
            video_playing = video_to_watch
            print("Playing video:", video_playing.title)
            self._currently_playing = video_playing.video_id
            self._paused = None


    def stop_video(self):
        """Stops the current video."""
        if self._currently_playing != None:
            video_playing = self._video_library.get_video(self._currently_playing)
            print("Stopping video:", video_playing.title)
            self._currently_playing = None
        elif self._paused != None:
            video_paused = self._video_library.get_video(self._paused)
            print("Stopping video:", video_paused.title)
            self._paused = None
        else:
            print("Cannot stop video: No video is currently playing")


    def play_random_video(self):
        """Plays a random video from the video library."""

        video_id = random.choice(self._video_library.get_ids())
        video_to_watch = self._video_library.get_video(video_id)

        num_videos = len(self._video_library.get_all_videos())

        if video_to_watch == None or len(self._flagged) == num_videos:
            print("No videos available")
        elif video_to_watch.video_id in self._flagged.keys():
            print("Cannot play video: Video is currently flagged (reason:",
                  self._flagged[video_to_watch.video_id] + ")")
        else:
            if self._currently_playing != None:
                self.stop_video()
            video_playing = video_to_watch
            print("Playing video:", video_playing.title)
            self._currently_playing = video_playing.video_id
            self._paused = None

    def pause_video(self):
        """Pauses the current video."""
        video_playing = self._video_library.get_video(self._currently_playing)
        video_paused = self._video_library.get_video(self._paused)
        if self._currently_playing != None:
            print("Pausing video:", video_playing.title)
            self._currently_playing = None
            self._paused = video_playing.video_id
        elif self._paused != None:
            print("Video already paused:", video_paused.title)
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""

        if self._paused != None:
            video_paused = self._video_library.get_video(self._paused)
            print("Continuing video:", video_paused.title)
            self._currently_playing = video_paused.video_id
            self._paused = None
        elif self._currently_playing != None:
            print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")


    def show_playing(self):
        """Displays video currently playing."""

        video_playing = self._video_library.get_video(self._currently_playing)
        video_paused = self._video_library.get_video(self._paused)
        if video_playing != None:
            print("Currently playing:", video_playing)
        elif video_paused != None:
            print("Currently playing:", video_paused, "- PAUSED")
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in (name.upper() for name in self._playlists):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            print("Successfully created new playlist:", playlist_name)
            self._playlists[playlist_name] = []

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.upper() not in (x.upper() for x in self._playlists.keys()):
            print("Cannot add video to", playlist_name + ":", "Playlist does not exist")
            return

        for x in self._playlists:
            if playlist_name.upper() == x.upper():
                playlist_to_add = x
                break

        video_to_add = self._video_library.get_video(video_id)

        if video_to_add == None:
            print("Cannot add video to", playlist_name + ":", "Video does not exist")
        elif video_to_add.video_id in self._flagged.keys():
            print("Cannot add video to", playlist_name + ":", "Video is currently flagged (reason:",
                  self._flagged[video_to_add.video_id] + ")")
        elif video_to_add.video_id in self._playlists[playlist_to_add]:
            print("Cannot add video to", playlist_name + ":", "Video already added")
        else:
            print("Added video to", playlist_name + ":", video_to_add.title)
            self._playlists[playlist_to_add].append(video_to_add.video_id)


    def show_all_playlists(self):
        """Display all playlists."""

        if self._playlists == {}:  # have to deal with empty list of playlists separately here
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            playlist_list = sorted(list(self._playlists.keys()))
            for x in playlist_list:
                print("  " + x)


    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.upper() not in (x.upper() for x in self._playlists.keys()):
            print("Cannot show playlist", playlist_name + ":", "Playlist does not exist")
            return

        for x in self._playlists:
            if playlist_name.upper() == x.upper():
                playlist_to_show = x
                break

        print("Showing playlist:", playlist_name)
        video_ids = self._playlists[playlist_to_show]
        if video_ids == []:
            print("  No videos here yet")
        else:
            for y in video_ids:
                if y in self._flagged.keys():
                    print(" ", self._video_library.get_video(y), "- FLAGGED (reason:",
                          self._flagged[y] + ")")
                else:
                    print(" ", self._video_library.get_video(y))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.upper() not in (x.upper() for x in self._playlists.keys()):
            print("Cannot remove video from", playlist_name + ":", "Playlist does not exist")
            return

        for x in self._playlists:
            if playlist_name.upper() == x.upper():
                playlist_to_remove = x
                break

        video_to_remove = self._video_library.get_video(video_id)

        if video_to_remove == None:
            print("Cannot remove video from", playlist_name + ":", "Video does not exist")
        elif video_to_remove.video_id in self._playlists[playlist_to_remove]:
            self._playlists[playlist_to_remove].remove(video_to_remove.video_id)
            print("Removed video from", playlist_name + ":", video_to_remove.title)
        else:
            print("Cannot remove video from", playlist_name + ":", "Video is not in playlist")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.upper() not in (x.upper() for x in self._playlists.keys()):
            print("Cannot clear playlist", playlist_name + ":", "Playlist does not exist")
            return

        for x in self._playlists:
            if playlist_name.upper() == x.upper():
                playlist_to_clear = x
                break

        print("Successfully removed all videos from", playlist_name)
        self._playlists[playlist_to_clear] = []

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in (x.upper() for x in self._playlists.keys()):
            print("Cannot delete playlist", playlist_name + ":", "Playlist does not exist")
            return

        for x in self._playlists:
            if playlist_name.upper() == x.upper():
                playlist_to_delete = x
                break

        modified_playlists = {}

        for y in self._playlists:
            if playlist_name.upper() == y.upper():
                continue
            else:
                modified_playlists[y] = self._playlists[y]
        print("Deleted playlist:", playlist_name)
        self._playlists = modified_playlists


    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos_list = self._video_library.get_all_videos()
        search_match = []
        for x in videos_list:
            if x.video_id in self._flagged.keys():
                continue
            title = x.title
            if search_term.upper() in title.upper():
                search_match.append(x)

        if len(search_match) == 0:
            print("No search results for", search_term)
            return
        else:
            print("Here are the results for", search_term + ":")
            for y in search_match:
                print(" ", str(search_match.index(y)+1) + ")", y)
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        try:
            play_from_search = int(input())
        except ValueError:
            return
        try:
            video_to_watch = search_match[play_from_search - 1]
        except IndexError:
            return

        video_id = video_to_watch.video_id
        self.play_video(video_id)


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos_list = self._video_library.get_all_videos()
        search_match = []
        for x in videos_list:
            if x.video_id in self._flagged.keys():
                continue
            tags_tuple = x.tags
            for v in tags_tuple:
                if video_tag.upper() == v.upper():
                    search_match.append(x)
                    break

        if len(search_match) == 0:
            print("No search results for", video_tag)
            return
        else:
            print("Here are the results for", video_tag + ":")
            for y in search_match:
                print(" ", str(search_match.index(y) + 1) + ")", y)
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        try:
            play_from_search = int(input())
        except ValueError:
            return
        try:
            video_to_watch = search_match[play_from_search - 1]
        except IndexError:
            return

        video_id = video_to_watch.video_id
        self.play_video(video_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video_to_flag = self._video_library.get_video(video_id)
        if video_to_flag == None:
            print("Cannot flag video: Video does not exist")
        elif video_id in self._flagged.keys():
            print("Cannot flag video: Video is already flagged")
        else:
            if flag_reason == "":
                flag_reason = "Not supplied"
            if self._currently_playing == video_to_flag.video_id or self._paused == video_to_flag.video_id:
                self.stop_video()
            print("Successfully flagged video:", video_to_flag.title, "(reason:", flag_reason + ")")
            self._flagged[video_id] = flag_reason


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video_to_unflag = self._video_library.get_video(video_id)

        if video_to_unflag == None:
            print("Cannot remove flag from video: Video does not exist")
            return
        elif video_to_unflag.video_id not in self._flagged:
            print("Cannot remove flag from video: Video is not flagged")
            return
        else:
            modified_flagged = {}
            for y in self._flagged:
                if video_to_unflag.video_id == y:
                    continue
                else:
                    modified_flagged[y] = self._flagged[y]
            print("Successfully removed flag from video:", video_to_unflag.title)
            self._flagged = modified_flagged
