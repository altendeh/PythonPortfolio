import os
import json
import time
import random
import string


class Song:
    def __init__(self, title, artist, album, genre):
        #Initialisiert ein Song-Objekt mit Titel, Künstler, Album und Genre
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        

    def __str__(self):
        #Gibt eine lesbare Darstellung des Songs zurück
        return f"{self.title} by {self.artist} - Album: {self.album}, Genre: {self.genre}, "

    def __lt__(self, other):
        #Vergleichsoperator für weniger als, basierend auf dem Titel
        return self.title < other.title

    def __eq__(self, other):
        #Vergleichsoperator für Gleichheit, basierend auf dem Titel
        return self.title == other.title
    def to_dict(self):
        #Konvertiert das Song-Objekt in ein Wörterbuch
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "genre": self.genre
        }

    @staticmethod
    def from_dict(data):
        #Erstellt ein Song-Objekt aus einem Wörterbuch
        return Song(data['title'], data['artist'], data['album'], data['genre'])

class Playlist:
    def __init__(self, name):
        #Initialisiert eine Playlist mit einem Namen und einer leeren Songliste
        self.name = name
        self.songs = []

    def add_song(self, song):
        #Fügt einen Song zur Playlist hinzu
        self.songs.append(song)
    
    def remove_song(self, title):
        #Entfernt einen Song aus der Playlist basierend auf dem Titel
        self.songs = [song for song in self.songs if song.title != title]

    def __str__(self):
        #Gibt eine lesbare Darstellung der Playlist zurück
        return f"Playlist: {self.name}, Songs: {len(self.songs)}"

    def to_dict(self):
        #Konvertiert die Playlist in ein Wörterbuch
        return {
            "name": self.name,
            "songs": [song.to_dict() for song in self.songs]
        }

    @staticmethod
    def from_dict(data):
        #Erstellt eine Playlist aus einem Wörterbuch
        playlist = Playlist(data['name'])
        playlist.songs = [Song.from_dict(song_data) for song_data in data['songs']]
        return playlist


class RedBlackNode:
    def __init__(self, song):
        #Initialisiert einen Knoten für den Rot-Scwarz-Baum
        self.song = song
        self.color = "RED"  #Alle neu eingefügten Knoten sind standardmäßig rot
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        #Initialisiert einen Rot-Schwarz-Baum mit einem NIL-Knoten
        self.NIL = RedBlackNode(None)
        self.NIL.color = "BLACK"
        self.root = self.NIL

    def insert(self, song):
        #Fügt einen neuen Song in den Rot-Schwarz-Baum ein
        new_node = RedBlackNode(song)
        new_node.left = self.NIL
        new_node.right = self.NIL

        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if new_node.song < current.song:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.song < parent.song:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = "RED"
        self.fix_insert(new_node)

    def fix_insert(self, node):
        #Fixiert den Baum nach dem Einfügen, um die Rot-Schwarz-Eigenschaften zu bewahren
        while node != self.root and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.left_rotate(node.parent.parent)

        self.root.color = "BLACK"

    def left_rotate(self, x):
        #Führt eine Linksrotation durch
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        #Führt eine Rechtsrotation durch
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x.parent.right == x:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def search_iterative(self, value, criteria):
        #Iterative Suche nach einem Song basierend auf einem Kriterium
        current = self.root
        while current != self.NIL:
            if getattr(current.song, criteria) == value:
                return current.song
            elif value < getattr(current.song, criteria):
                current = current.left
            else:
                current = current.right
        return None


    def _search_recursive(self, node, value, criteria):
        #Rekursive Suche nach einem Song basierend auf einem Kriterium
        if node == self.NIL:
            return None
        if getattr(node.song, criteria) == value:
            return node.song
        if value < getattr(node.song, criteria):
            return self._search_recursive(node.left, value, criteria)
        else:
            return self._search_recursive(node.right, value, criteria)


    def bfs_search(self, value, criteria):
        #Breitensuche nach einem Song basierend auf einem Kriterium
        if self.root == self.NIL:
            return None
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if getattr(node.song, criteria) == value:
                return node.song
            if node.left != self.NIL:
                queue.append(node.left)
            if node.right != self.NIL:
                queue.append(node.right)
        return None


    def dfs_search(self, node, value, criteria):
        #Tiefensuche nach einem Song basierend auf einem Kriterium
        if node == self.NIL:
            return None
        if getattr(node.song, criteria) == value:
            return node.song
        left_search = self.dfs_search(node.left, value, criteria)
        if left_search is not None:
            return left_search
        return self.dfs_search(node.right, value, criteria)


    def delete(self, song):
        #Löscht einen Song aus dem Rot-Schwarz-Baum
        self.root = self._delete_recursive(self.root, song)

    def _delete_recursive(self, node, song):
        #Rekursive Methode zum Löschen eines Songs
        if node == self.NIL:
            return node

        if song < node.song:
            node.left = self._delete_recursive(node.left, song)
        elif song > node.song:
            node.right = self._delete_recursive(node.right, song)
        else:
            if node.left == self.NIL:
                return node.right
            elif node.right == self.NIL:
                return node.left

            temp = self._min_value_node(node.right)
            node.song = temp.song
            node.right = self._delete_recursive(node.right, temp.song)

        return node

    def _min_value_node(self, node):
        #Findet den Knoten mit dem minimalen Wert
        current = node
        while current.left != self.NIL:
            current = current.left
        return current

class MusicApp:
    FILENAME = "songs_RBT.csv"

    def __init__(self):
        #Initialisiert die Musik-App und lädt Songs
        self.songs = []
        self.rbt = RedBlackTree()
        self.load_songs()

    def load_songs(self):
        #Lädt Songs aus einer Datei beim Start der App
        """Load songs from a file when the app starts."""
        if os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'r') as file:
                for line in file:
                    title, artist, album, genre = line.strip().split(',')
                    song = Song(title, artist, album, genre)
                    self.songs.append(song)
                    self.rbt.insert(song)  #Fügt den Song in den Rot-Schwarz-Baum ein
            print(f"{len(self.songs)} songs loaded from {self.FILENAME}.")
        else:
            print("No songs found. Starting with an empty music library.")

    def save_data(self):
        #Speichert alle Songs in einer Datei
        """Save all songs to a file."""
        with open(self.FILENAME, 'w') as file:
            for song in self.songs:
                file.write(f"{song.title},{song.artist},{song.album},{song.genre}\n")
        print(f"{len(self.songs)} songs saved to {self.FILENAME}.")
    
    def add_song(self, title, artist, album, genre):
        #Fügt einen neuen Song zur Bibliothek hinzu und speichert die Daten
        song = Song(title, artist, album, genre)
        self.songs.append(song)
        self.rbt.insert(song)  #Fügt den Song in den Rot-Schwarz-Baum ein
        self.save_data()  #Speichert die Daten nach dem Hinzufügen eines Songs
        print(f"'{song}' added to your music library.")

    def delete_song(self, title):
        #Löscht einen Song aus der Bibliothek und speichert die Daten
        song_to_delete = next((s for s in self.songs if s.title == title), None)
        if song_to_delete:
            self.songs.remove(song_to_delete)
            self.rbt.delete(song_to_delete)  #Löscht den Song aus dem Rot-Schwarz-Baum
            for playlist in self.playlists:
                playlist.remove_song(title)  #Entfernt den Song aus allen Playlists
            self.save_data()  #Speichert die Daten nach dem Löschen eines Songs
            print(f"'{song_to_delete}' removed from your music library.")
        else:
            print(f"'{title}' not found in your music library.")

    def display_all_songs(self):
        #Zeigt alle Songs in der Bibliothek an
        if not self.songs:
            print("No songs available.")
        else:
            for song in self.songs:
                print(song)

    def search_song(self):
        #Sucht nach einem Song basierend auf einem Kriterium und einer Suchmethode
        print("Search for a song:")
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
        search_method = input("Choose search method - (R)ecursive, (I)terative, (B)readth-First Search, or (D)epth-First Search: ").strip().lower()

        start_time = time.time()  # Beginn der Zeitmessung

        if search_method == 'r':
            result = self.rbt._search_recursive(self.rbt.root, value, criteria)
        elif search_method == 'i':
            result = self.rbt.search_iterative(value, criteria)
        elif search_method == 'b':
            result = self.rbt.bfs_search(value, criteria)
        elif search_method == 'd':
            result = self.rbt.dfs_search(self.rbt.root, value, criteria)
        else:
            print("Invalid search method selected.")
            return

        end_time = time.time()  # Ende der Zeitmessung
        elapsed_time = end_time - start_time

        if result:
            print(f"'{result}' found in your music library.")
        else:
            print(f"'{value}' not found in your music library.")

        print(f"Time taken: {elapsed_time:.6f} seconds.")

    
    def sort_songs(self): 
        #Sortiert die Songs basierend auf einem Kriterium und einer Sortiermethode       
        print("Choose sorting order:")
        print("1. Ascending")
        print("2. Descending")

        order = input("Enter your choice: ").strip()

        print("Choose sorting criteria:")
        print("1. Song Title")
        print("2. Artist")
        print("3. Genre")

        criteria = input("Enter your choice: ").strip()
        
        print("Choose sorting algorithm:")
        print("1. Bubble Sort")
        print("2. Insertion Sort")
        print("3. Merge Sort")
        print("4. Quick Sort")

        choice = input("Enter your choice: ").strip()

        # Messen der Zeit, die zum Sortieren benötigt wird
        start_time = time.time()
        if choice == '1':
            self.bubble_sort(order, criteria)
        elif choice == '2':
            self.insertion_sort(order, criteria)
        elif choice == '3':
            self.songs = self.merge_sort(self.songs, order, criteria)
        elif choice == '4':
            self.quick_sort(0, len(self.songs) - 1, order, criteria)
        else:
            print("Invalid choice.")
        
        print(f"Time taken: {time.time() - start_time:.6f} seconds.")
        self.save_data()  # Speichern der sortierten Liste in der Datei

    def bubble_sort(self, order, criteria):
        #Implementiert den Bubble Sort Algorithmus
        n = len(self.songs)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.compare(self.songs[j], self.songs[j + 1], order, criteria):
                    self.songs[j], self.songs[j + 1] = self.songs[j + 1], self.songs[j]
                    swapped = True
            if not swapped:
                break
        print("Sorted using Bubble Sort.")

    def insertion_sort(self, order, criteria):
        #Implementiert den Insertion Sort Algorithmus
        for i in range(1, len(self.songs)):
            key_song = self.songs[i]
            j = i - 1
            while j >= 0 and self.compare(self.songs[j], key_song, order, criteria):
                self.songs[j + 1] = self.songs[j]
                j -= 1
            self.songs[j + 1] = key_song
        print("Sorted using Insertion Sort.")

    def merge_sort(self, array, order, criteria):
        #Implementiert den Merge Sort Algorithmus
        if len(array) <= 1:
            return array

        mid = len(array) // 2
        left_half = self.merge_sort(array[:mid], order, criteria)
        right_half = self.merge_sort(array[mid:], order, criteria)

        return self.merge(left_half, right_half, order, criteria)

    def merge(self, left, right, order, criteria):
        #Hilfsmethode für Merge Sort
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if self.compare(left[i], right[j], order, criteria):
                result.append(right[j])
                j += 1
            else:
                result.append(left[i])
                i += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def quick_sort(self, low, high, order, criteria):
        #Implementiert den Quick Sort Algorithmus
        if low < high:
            pi = self.partition(low, high, order, criteria)
            self.quick_sort(low, pi - 1, order, criteria)
            self.quick_sort(pi + 1, high, order, criteria)

    def partition(self, low, high, order, criteria):
        #Hilfsmethode für Quick Sort
        pivot = self.songs[high]
        i = low - 1

        for j in range(low, high):
            if not self.compare(pivot, self.songs[j], order, criteria):
                i += 1
                self.songs[i], self.songs[j] = self.songs[j], self.songs[i]

        self.songs[i + 1], self.songs[high] = self.songs[high], self.songs[i + 1]
        return i + 1

    def compare(self, song1, song2, order, criteria):
        #Vergleicht zwei Songs basierend auf dem Kriterium und der Reihenfolge
        if criteria == '1':  # Song Title
            if order == '1':  # Ascending
                return song1.title > song2.title
            else:  # Descending
                return song1.title < song2.title
        elif criteria == '2':  # Artist
            if order == '1':  # Ascending
                return song1.artist > song2.artist
            else:  # Descending
                return song1.artist < song2.artist
        elif criteria == '3':  # Genre
            if order == '1':  # Ascending
                return song1.genre > song2.genre
            else:  # Descending
                return song1.genre < song2.genre
    

    def create_playlist(self):
        #Erstellt eine neue Playlist
        name = input("Enter playlist name: ").strip()
        if any(pl.name == name for pl in self.playlists):
            print(f"A playlist with the name '{name}' already exists. Please choose a different name.")
            return
        playlist = Playlist(name)
        self.playlists.append(playlist)
        self.save_data()
        print(f"Created playlist: {playlist}")


    def add_song_to_playlist(self):
        #Fügt einen Song einer Playlist hinzu
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
        #Entfernt einen Song aus einer Playlist
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
        #Erstellt eine bestimmte Anzahl zufälliger Songs
        import random
        import string

        for _ in range(count):
            title = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            artist = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            album = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            genre = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            self.add_song(title, artist, album, genre)
 

    def main_menu(self):
        #Hauptmenü der Musik-App
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
    #Startet die Musik-App, wenn das Skript direkt ausgeführt wird
    app = MusicApp()
    app.main_menu()

    