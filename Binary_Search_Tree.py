import os
import json

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

    def search(self, song):
        return self._search_recursive(self.root, song)

    def _search_recursive(self, node, song):
        if node is None or node.song == song:
            return node is not None
        if song < node.song:
            return self._search_recursive(node.left, song)
        else:
            return self._search_recursive(node.right, song)

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

    def linear_search(self, title):
        for index, song in enumerate(self.songs):
            if song.title == title:
                return index
        return -1

    def binary_search(self, title):
        song_to_search = Song(title, "", "", "")
        return self.bst.search(song_to_search)

    def search_song(self):
        print("Search for a song:")
        search_method = input("Choose search method - (L)inear or (B)inary: ").strip().lower()
        title = input("Enter song title: ").strip()

        if search_method == 'l':
            result = self.linear_search(title)
            if result != -1:
                print(f"'{self.songs[result]}' found in your music library at position {result + 1}.")
            else:
                print(f"'{title}' not found in your music library.")
        elif search_method == 'b':
            found = self.binary_search(title)
            if found:
                print(f"'{title}' found in your music library.")
            else:
                print(f"'{title}' not found in your music library.")
        else:
            print("Invalid search method selected.")

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
        print("Sorted using Bubble Sort.")

    def insertion_sort(self, ascending, criteria):
        for i in range(1, len(self.songs)):
            key_song = self.songs[i]
            j = i - 1
            while j >= 0 and self.compare(self.songs[j], key_song, criteria, ascending):
                self.songs[j + 1] = self.songs[j]
                j -= 1
            self.songs[j + 1] = key_song
        print("Sorted using Insertion Sort.")

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

    def quick_sort(self, low, high, ascending, criteria):
        if low < high:
            pi = self.partition(low, high, ascending, criteria)
            self.quick_sort(low, pi - 1, ascending, criteria)
            self.quick_sort(pi + 1, high, ascending, criteria)

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
        name = input("Enter playlist name: ")
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
            print("4. Search Songs")
            print("5. Sort Songs")
            print("6. Display All Songs")
            print("7. Display Playlists")
            print("8. Exit")
            print("9. Create Random Songs")

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
                self.search_song()
            elif choice == '5':
                self.sort_songs()
            elif choice == '6':
                self.display_all_songs()
            elif choice == '7':
                self.display_playlists()
            elif choice == '8':
                print("Exiting Music App. Goodbye!")
                break
            elif choice == '9':
                count = int(input("Enter number of random songs to create: "))
                self.create_random_songs(count)
            else:
                print("Invalid choice. Please select again.")

if __name__ == "__main__":
    app = MusicApp()
    app.main_menu()
    
    
    Hinzufügen von delete song und delete playlist für beide Arten von Trees
    Search and Sort Playlist for both trees
