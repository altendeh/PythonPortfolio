import os
import json
import time

class Song:
    def __init__(self, title, artist, album, genre):
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre

    def __str__(self):
        return f"{self.title} by {self.artist} - Album: {self.album}, Genre: {self.genre}"

    def __lt__(self, other):
        return self.title < other.title

    def __eq__(self, other):
        return self.title == other.title

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "genre": self.genre
        }

    @staticmethod
    def from_dict(data):
        return Song(data['title'], data['artist'], data['album'], data['genre'])

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, title):
        song_to_remove = next((s for s in self.songs if s.title == title), None)
        if song_to_remove:
            self.songs.remove(song_to_remove)
            print(f"'{song_to_remove}' removed from playlist '{self.name}'.")
        else:
            print(f"'{title}' not found in playlist '{self.name}'.")

    def __str__(self):
        return f"Playlist: {self.name}, Songs: {len(self.songs)}"

    def to_dict(self):
        return {
            "name": self.name,
            "songs": [song.to_dict() for song in self.songs]
        }

    @staticmethod
    def from_dict(data):
        playlist = Playlist(data['name'])
        playlist.songs = [Song.from_dict(song_data) for song_data in data['songs']]
        return playlist

class TreeNode:
    def __init__(self, song):
        self.song = song
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, song):
        if self.root is None:
            self.root = TreeNode(song)
        else:
            self._insert_recursive(self.root, song)

    def _insert_recursive(self, node, song):
        if song < node.song:
            if node.left is None:
                node.left = TreeNode(song)
            else:
                self._insert_recursive(node.left, song)
        else:
            if node.right is None:
                node.right = TreeNode(song)
            else:
                self._insert_recursive(node.right, song)

    def search_recursive(self, node, value, criteria):
        if node is None:
            return None
        if getattr(node.song, criteria) == value:
            return node.song
        if value < getattr(node.song, criteria):
            return self.search_recursive(node.left, value, criteria)
        else:
            return self.search_recursive(node.right, value, criteria)

    def search_iterative(self, value, criteria):
        current = self.root
        while current is not None:
            if getattr(current.song, criteria) == value:
                return current.song
            if value < getattr(current.song, criteria):
                current = current.left
            else:
                current = current.right
        return None

    def bfs_search(self, value, criteria):
        if self.root is None:
            return None
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if getattr(node.song, criteria) == value:
                return node.song
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return None

    def dfs_search(self, node, value, criteria):
        if node is None:
            return None
        if getattr(node.song, criteria) == value:
            return node.song
        left_search = self.dfs_search(node.left, value, criteria)
        if left_search is not None:
            return left_search
        return self.dfs_search(node.right, value, criteria)

    def delete(self, song):
        self.root = self._delete_recursive(self.root, song)

    def _delete_recursive(self, node, song):
        if node is None:
            return node

        if song < node.song:
            node.left = self._delete_recursive(node.left, song)
        elif song > node.song:
            node.right = self._delete_recursive(node.right, song)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._min_value_node(node.right)
            node.song = temp.song
            node.right = self._delete_recursive(node.right, temp.song)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

class MusicApp:
    FILENAME = "music_data_BST.json"

    def __init__(self):
        self.songs = []
        self.playlists = []
        self.bst = BinarySearchTree()
        self.load_data()

    def load_data(self):
        if os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'r') as f:
                data = json.load(f)
                self.songs = [Song.from_dict(song_data) for song_data in data.get('songs', [])]
                self.playlists = [Playlist.from_dict(pl_data) for pl_data in data.get('playlists', [])]
                for song in self.songs:
                    self.bst.insert(song)
            print("Data loaded successfully.")
        else:
            print("No data file found. Starting with an empty database.")

    def save_data(self):
        data = {
            "songs": [song.to_dict() for song in self.songs],
            "playlists": [playlist.to_dict() for playlist in self.playlists]
        }
        with open(self.FILENAME, 'w') as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")

    def add_song(self, title, artist, album, genre):
        song = Song(title, artist, album, genre)
        self.songs.append(song)
        self.bst.insert(song)  # Insert into the Binary Search Tree
        self.save_data()  # Save after adding a song
        print(f"'{song}' added to your music library.")

    def delete_song(self, title):
        song_to_delete = next((s for s in self.songs if s.title == title), None)
        if song_to_delete:
            self.songs.remove(song_to_delete)
            self.bst.delete(song_to_delete)  # Delete from the Binary Search Tree
            for playlist in self.playlists:
                playlist.remove_song(title)  # Remove song from all playlists
            self.save_data()  # Save after deleting a song
            print(f"'{song_to_delete}' removed from your music library.")
        else:
            print(f"'{title}' not found in your music library.")

    def display_all_songs(self):
        if not self.songs:
            print("No songs available.")
        else:
            for song in self.songs:
                print(song)

    def search_song(self):
        print("Search for a song, artist or genre:")
        criteria = input("Search by (T)itle, (A)rtist, or (G)enre: ").strip().lower()
        if criteria == 't':
            criteria = 'title'
        elif criteria == 'a':
            criteria = 'artist'
        elif criteria == 'g':
            criteria = 'genre'
        else:
            print("Invalid criteria selected.")
            return
    
        value = input(f"Enter {criteria}: ").strip()
        search_method = input("Choose search method - (R)ecursive, (I)terative, (B)readth-First Search, or (D)epth-FirstS: ").strip().lower()

        start_time = time.time()  # Start time measurement

        if search_method == 'r':
            result = self.bst.search_recursive(self.bst.root, value, criteria)
        elif search_method == 'i':
            result = self.bst.search_iterative(value, criteria)
        elif search_method == 'b':
            result = self.bst.bfs_search(value, criteria)
        elif search_method == 'd':
            result = self.bst.dfs_search(self.bst.root, value, criteria)
        else:
            print("Invalid search method selected.")
            return

        end_time = time.time()  # End time measurement
        elapsed_time = end_time - start_time

        if result:
            print(f"'{result}' found in your music library.")
        else:
            print(f"'{value}' not found in your music library.")

        print(f"Time taken: {elapsed_time:.6f} seconds.")


    def sort_songs(self):
        print("Choose sorting order:")
        print("1. Ascending")
        print("2. Descending")

        order_choice = input("Enter your choice: ").strip()
        ascending = order_choice == '1'

        print("Choose sorting criteria:")
        print("1. Title")
        print("2. Artist")
        print("3. Genre")

        criteria_choice = input("Enter your choice: ").strip()
        
        print("Choose sorting algorithm:")
        print("1. Bubble Sort")
        print("2. Insertion Sort")
        print("3. Merge Sort")
        print("4. Quick Sort")

        choice = input("Enter your choice: ").strip()

        # Measuring the time taken to sort the songs
        import time
        start_time = time.time()
        if choice == '1':
            self.bubble_sort(ascending, criteria_choice)
        elif choice == '2':
            self.insertion_sort(ascending, criteria_choice)
        elif choice == '3':
            self.songs = self.merge_sort(self.songs, ascending, criteria_choice)
        elif choice == '4':
            self.quick_sort(0, len(self.songs) - 1, ascending, criteria_choice)
        else:
            print("Invalid choice.")
        
        print(f"Time taken: {time.time() - start_time:.6f} seconds.")
        self.save_data()  # Save the sorted list to file

    def bubble_sort(self, ascending, criteria):
        n = len(self.songs)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.compare(self.songs[j], self.songs[j + 1], criteria, ascending):
                    self.songs[j], self.songs[j + 1] = self.songs[j + 1], self.songs[j]
                    swapped = True
            if not swapped:
                break
        #print("Sorted using Bubble Sort.")
        #self.save_data()  # Save changes


    def insertion_sort(self, ascending, criteria):
        for i in range(1, len(self.songs)):
            key_song = self.songs[i]
            j = i - 1
            while j >= 0 and self.compare(self.songs[j], key_song, criteria, ascending):
                self.songs[j + 1] = self.songs[j]
                j -= 1
            self.songs[j + 1] = key_song
        #print("Sorted using Insertion Sort.")
        #self.save_data()  # Save changes


    def merge(self, left, right, ascending, criteria):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if self.compare(left[i], right[j], criteria, ascending):
                result.append(right[j])
                j += 1
            else:
                result.append(left[i])
                i += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result
    

    def merge_sort(self, songs, ascending, criteria):
        if len(songs) <= 1:
            return songs

        mid = len(songs) // 2
        left = self.merge_sort(songs[:mid], ascending, criteria)
        right = self.merge_sort(songs[mid:], ascending, criteria)

        return self.merge(left, right, ascending, criteria)

    def quick_sort(self, low, high, ascending, criteria):
        if low < high:
            pi = self.partition(low, high, ascending, criteria)
            self.quick_sort(low, pi - 1, ascending, criteria)
            self.quick_sort(pi + 1, high, ascending, criteria)
        #print("Sorted using Quick Sort.")
        #self.save_data()  # Save changes

    def partition(self, low, high, ascending, criteria):
        pivot = self.songs[high]
        i = low - 1

        for j in range(low, high):
            if self.compare(self.songs[j], pivot, criteria, ascending):
                i += 1
                self.songs[i], self.songs[j] = self.songs[j], self.songs[i]

        self.songs[i + 1], self.songs[high] = self.songs[high], self.songs[i + 1]
        return i + 1

    def compare(self, song1, song2, criteria, ascending):
        if criteria == '1':  # Title
            comparison = song1.title > song2.title
        elif criteria == '2':  # Artist
            comparison = song1.artist > song2.artist
        elif criteria == '3':  # Genre
            comparison = song1.genre > song2.genre
        else:
            comparison = song1.title > song2.title  # Default to title if invalid criteria

        return comparison if ascending else not comparison

    def create_playlist(self):
        name = input("Enter playlist name: ").strip()
        if any(pl.name == name for pl in self.playlists):
            print(f"A playlist with the name '{name}' already exists. Please choose a different name.")
            return
        playlist = Playlist(name)
        self.playlists.append(playlist)
        self.save_data()
        print(f"Created playlist: {playlist}")

    def add_song_to_playlist(self):
        playlist_name = input("Enter the name of the playlist: ")
        playlist = next((pl for pl in self.playlists if pl.name == playlist_name), None)
        if not playlist:
            print("Playlist not found.")
            return
        
        song_title = input("Enter the name of the song to add: ")
        song = next((s for s in self.songs if s.title == song_title), None)
        if not song:
            print("Song not found.")
            return

        playlist.add_song(song)
        self.save_data()
        print(f"Added {song.title} to playlist {playlist.name}")

    def remove_song_from_playlist(self):
        playlist_name = input("Enter the name of the playlist: ")
        playlist = next((pl for pl in self.playlists if pl.name == playlist_name), None)
        if not playlist:
            print("Playlist not found.")
            return
        
        song_title = input("Enter the name of the song to remove: ")
        playlist.remove_song(song_title)
        self.save_data()

    def display_playlists(self):
        if not self.playlists:
            print("No playlists available.")
        else:
            for playlist in self.playlists:
                print(playlist)
                for song in playlist.songs:
                    print(f"  - {song}")

    def create_random_songs(self, count):
        import random
        import string

        for _ in range(count):
            title = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            artist = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            album = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            genre = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            self.add_song(title, artist, album, genre)


    def main_menu(self):
        while True:
            print("\n--- Music App ---")
            print("1. Add New Song")
            print("2. Create Playlist")
            print("3. Add Song to Playlist")
            print("4. Remove Song from Playlist")
            print("5. Search Songs")
            print("6. Sort Songs")
            print("7. Display All Songs")
            print("8. Display Playlists")
            print("9. Delete Song from Library") 
            print("10. Exit")
            print("11. Create Random Songs")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                title = input("Enter song title: ").strip()
                artist = input("Enter artist name: ").strip()
                album = input("Enter album name: ").strip()
                genre = input("Enter genre: ").strip()
                self.add_song(title, artist, album, genre)
            elif choice == '2':
                self.create_playlist()
            elif choice == '3':
                self.add_song_to_playlist()
            elif choice == '4':
                self.remove_song_from_playlist()
            elif choice == '5':
                self.search_song()
            elif choice == '6':
                self.sort_songs()
            elif choice == '7':
                self.display_all_songs()
            elif choice == '8':
                self.display_playlists()
            elif choice == '9':  
                title = input("Enter the title of the song to delete: ").strip()
                self.delete_song(title)
            elif choice == '10':
                print("Exiting Music App. Goodbye!")
                break
            elif choice == '11':
                count = int(input("Enter number of random songs to create: "))
                self.create_random_songs(count)
            else:
                print("Invalid choice. Please select again.")
                
if __name__ == "__main__":
    app = MusicApp()
    app.main_menu()