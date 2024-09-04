import os
import json
import time
import random
import string

class Song:
    def __init__(self, title, artist, album, genre):
        """
        Initialisiert ein Song-Objekt.

        Args:
            title (str): Der Titel des Songs.
            artist (str): Der Künstler des Songs.
            album (str): Das Album, zu dem der Song gehört.
            genre (str): Das Genre des Songs.
        """
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre

    def __str__(self):
        #Gibt eine lesbare Darstellung des Songs zurück
        return f"{self.title} von {self.artist} - Album: {self.album}, Genre: {self.genre}"

    def __lt__(self, other):
        #Vergleichsoperator für weniger als, basierend auf dem Titel
        return self.title < other.title

    def __eq__(self, other):
        #Vergleichsoperator für Gleichheit, basierend auf dem Titel
        return self.title == other.title

    def to_dict(self):
        """
        Konvertiert das Song-Objekt in ein Wörterbuch.

        Returns:
            dict: Ein Wörterbuch, das die Song-Attribute enthält.
        """
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "genre": self.genre
        }

    @staticmethod
    def from_dict(data):
        """
        Erstellt ein Song-Objekt aus einem Wörterbuch.

        Args:
            data (dict): Ein Wörterbuch mit Song-Attributen.

        Returns:
            Song: Ein Song-Objekt.
        """
        return Song(data['title'], data['artist'], data['album'], data['genre'])

class Playlist:
    def __init__(self, name):
        """
        Initialisiert eine Playlist mit einem Namen und einer leeren Songliste.

        Args:
            name (str): Der Name der Playlist.
        """
        self.name = name
        self.songs = []

    def add_song(self, song):
        """
        Fügt einen Song zur Playlist hinzu.

        Args:
            song (Song): Das hinzuzufügende Song-Objekt.
            
        Returns:
            None
        """
        self.songs.append(song)
    
    def remove_song(self, title):
        """
        Entfernt einen Song aus der Playlist basierend auf dem Titel.

        Args:
            title (str): Der Titel des Songs, der entfernt werden soll.

        Returns:
            None
        """
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
        # Erstellt eine Playlist aus einem Wörterbuch
        playlist = Playlist(data['name'])
        playlist.songs = [Song.from_dict(song_data) for song_data in data['songs']]
        return playlist

class RedBlackNode:
    def __init__(self, song):
        #Initialisiert einen Knoten für den Rot-Schwarz-Baum
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
        """
        Fügt einen neuen Song in den Rot-Schwarz-Baum ein.

        Args:
            song (Song): Das Song-Objekt, das in den Baum eingefügt werden soll.

        Returns:
            None
        """
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
        """
        Fixiert den Baum nach dem Einfügen, um die Rot-Schwarz-Eigenschaften zu bewahren.

        Args:
            node (RedBlackNode): Der neu eingefügte Knoten, der fixiert werden muss.

        Returns:
            None
        """
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
        """
        Führt eine Linksrotation durch.

        Args:
            x (RedBlackNode): Der Knoten, um den die Linksrotation durchgeführt wird.

        Returns:
            None
        """
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
        """
        Führt eine Rechtsrotation durch.

        Args:
            x (RedBlackNode): Der Knoten, um den die Rechtsrotation durchgeführt wird.

        Returns:
            None
        """
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
        """
        Breitensuche nach einem Song basierend auf einem Kriterium.

        Args:
            value (str): Der Wert des Suchkriteriums.
            criteria (str): Das Suchkriterium (z.B. 'title', 'artist').

        Returns:
            Song: Der gefundene Song oder None, wenn kein Song gefunden wurde.
        """
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
        self.playlists = []
        self.rbt = RedBlackTree()
        self.load_songs()

    def load_songs(self):
        #Lädt Songs aus einer Datei beim Start der App
        if os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'r') as file:
                for line in file:
                    title, artist, album, genre = line.strip().split(',')
                    song = Song(title, artist, album, genre)
                    self.songs.append(song)
                    self.rbt.insert(song)  #Fügt den Song in den Rot-Schwarz-Baum ein
            print(f"{len(self.songs)} Songs aus {self.FILENAME} geladen.")
        else:
            print("Keine Songs gefunden. Starte mit einer leeren Musikbibliothek.")

    def save_data(self):
        #Speichert alle Songs in einer Datei
        with open(self.FILENAME, 'w') as file:
            for song in self.songs:
                file.write(f"{song.title},{song.artist},{song.album},{song.genre}\n")
        print(f"{len(self.songs)} Songs in {self.FILENAME} gespeichert.")

    def add_song(self, title, artist, album, genre):
        #Fügt einen neuen Song zur Bibliothek hinzu und speichert die Daten
        song = Song(title, artist, album, genre)
        self.songs.append(song)
        self.rbt.insert(song)  #Fügt den Song in den Rot-Schwarz-Baum ein
        self.save_data()  #Speichert die Daten nach dem Hinzufügen eines Songs
        print(f"'{song}' zur Musikbibliothek hinzugefügt.")

    def delete_song(self, title):
        #Löscht einen Song aus der Bibliothek und speichert die Daten
        song_to_delete = next((s for s in self.songs if s.title == title), None)
        if song_to_delete:
            self.songs.remove(song_to_delete)
            self.rbt.delete(song_to_delete)  #Löscht den Song aus dem Rot-Schwarz-Baum
            for playlist in self.playlists:
                playlist.remove_song(title)  #Entfernt den Song aus allen Playlists
            self.save_data()  #Speichert die Daten nach dem Löschen eines Songs
            print(f"'{song_to_delete}' aus der Musikbibliothek entfernt.")
        else:
            print(f"'{title}' nicht in der Musikbibliothek gefunden.")

    def display_all_songs(self):
        #Zeigt alle Songs in der Bibliothek an
        if not self.songs:
            print("Keine Songs verfügbar.")
        else:
            for song in self.songs:
                print(song)

    def search_song(self):
        #Sucht nach einem Song basierend auf einem Kriterium und einer Suchmethode
        print("Suche nach einem Song:")
        criteria = input("Suche nach (T)itel, (K)ünstler oder (G)enre: ").strip().lower()
        if criteria == 't':
            criteria = 'title'
        elif criteria == 'k':
            criteria = 'artist'
        elif criteria == 'g':
            criteria = 'genre'
        else:
            print("Ungültiges Suchkriterium ausgewählt.")
            return

        value = input(f"Gib {criteria} ein: ").strip()
        search_method = input("Wähle Suchmethode - (R)ekursiv, (I)terativ, (B)reitensuche oder (T)iefensuche: ").strip().lower()

        start_time = time.time()  #Beginn der Zeitmessung

        if search_method == 'r':
            result = self.rbt._search_recursive(self.rbt.root, value, criteria)
        elif search_method == 'i':
            result = self.rbt.search_iterative(value, criteria)
        elif search_method == 'b':
            result = self.rbt.bfs_search(value, criteria)
        elif search_method == 't':
            result = self.rbt.dfs_search(self.rbt.root, value, criteria)
        else:
            print("Ungültige Suchmethode ausgewählt.")
            return

        end_time = time.time()  #Ende der Zeitmessung
        elapsed_time = end_time - start_time

        if result:
            print(f"'{result}' in der Musikbibliothek gefunden.")
        else:
            print(f"'{value}' nicht in der Musikbibliothek gefunden.")

        print(f"Benötigte Zeit: {elapsed_time:.6f} Sekunden.")

    def sort_songs(self):
        """
        Sortiert die Songs basierend auf einem Kriterium und einer Sortiermethode.

        Returns:
            None
        """
        print("Wähle Sortierreihenfolge:")
        print("1. Aufsteigend")
        print("2. Absteigend")

        order = input("Gib deine Wahl ein: ").strip()

        print("Wähle Sortierkriterium:")
        print("1. Titel")
        print("2. Künstler")
        print("3. Genre")

        criteria = input("Gib deine Wahl ein: ").strip()
        
        print("Wähle Sortieralgorithmus:")
        print("1. Bubble Sort")
        print("2. Insertion Sort")
        print("3. Merge Sort")
        print("4. Quick Sort")

        choice = input("Gib deine Wahl ein: ").strip()

        #Messen der Zeit, die zum Sortieren benötigt wird
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
            print("Ungültige Wahl.")
        
        print(f"Benötigte Zeit: {time.time() - start_time:.6f} Sekunden.")
        self.save_data()  #Speichern der sortierten Liste in der Datei

    def bubble_sort(self, order, criteria):
        """
        Implementiert den Bubble Sort Algorithmus.

        Args:
            order (str): Die Sortierreihenfolge ('1' für aufsteigend, '2' für absteigend).
            criteria (str): Das Sortierkriterium ('1' für Titel, '2' für Künstler, '3' für Genre).

        Returns:
            None
        """
        n = len(self.songs)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.compare(self.songs[j], self.songs[j + 1], order, criteria):
                    self.songs[j], self.songs[j + 1] = self.songs[j + 1], self.songs[j]
                    swapped = True
            if not swapped:
                break
        print("Sortiert mit Bubble Sort.")

    def insertion_sort(self, order, criteria):
        #Implementiert den Insertion Sort Algorithmus
        for i in range(1, len(self.songs)):
            key_song = self.songs[i]
            j = i - 1
            while j >= 0 and self.compare(self.songs[j], key_song, order, criteria):
                self.songs[j + 1] = self.songs[j]
                j -= 1
            self.songs[j + 1] = key_song
        print("Sortiert mit Insertion Sort.")

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
        """
        Implementiert den Quick Sort Algorithmus.

        Args:
            low (int): Der Startindex.
            high (int): Der Endindex.
            order (str): Die Sortierreihenfolge ('1' für aufsteigend, '2' für absteigend).
            criteria (str): Das Sortierkriterium ('1' für Titel, '2' für Künstler, '3' für Genre).

        Returns:
            None
        """
        if low < high:
            pi = self.partition(low, high, order, criteria)
            self.quick_sort(low, pi - 1, order, criteria)
            self.quick_sort(pi + 1, high, order, criteria)

    def partition(self, low, high, order, criteria):
        """
        Hilfsmethode für Quick Sort.

        Args:
            low (int): Der Startindex.
            high (int): Der Endindex.
            order (str): Die Sortierreihenfolge ('1' für aufsteigend, '2' für absteigend).
            criteria (str): Das Sortierkriterium ('1' für Titel, '2' für Künstler, '3' für Genre).

        Returns:
            int: Der Index des Pivotelements.
        """
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
        if criteria == '1':  #Titel
            if order == '1':  #Aufsteigend
                return song1.title > song2.title
            else:  #Absteigend
                return song1.title < song2.title
        elif criteria == '2':  #Künstler
            if order == '1':  #Aufsteigend
                return song1.artist > song2.artist
            else:  #Absteigend
                return song1.artist < song2.artist
        elif criteria == '3':  #Genre
            if order == '1':  #Aufsteigend
                return song1.genre > song2.genre
            else:  #Absteigend
                return song1.genre < song2.genre

    def create_playlist(self):
        #Erstellt eine neue Playlist
        name = input("Gib den Namen der Playlist ein: ").strip()
        if any(pl.name == name for pl in self.playlists):
            print(f"Eine Playlist mit dem Namen '{name}' existiert bereits. Bitte wähle einen anderen Namen.")
            return
        playlist = Playlist(name)
        self.playlists.append(playlist)
        self.save_data()
        print(f"Playlist erstellt: {playlist}")

    def add_song_to_playlist(self):
        #Fügt einen Song einer Playlist hinzu
        playlist_name = input("Gib den Namen der Playlist ein: ")
        playlist = next((pl for pl in self.playlists if pl.name == playlist_name), None)
        if not playlist:
            print("Playlist nicht gefunden.")
            return

        song_title = input("Gib den Namen des Songs ein, der hinzugefügt werden soll: ")
        song = next((s for s in self.songs if s.title == song_title), None)
        if not song:
            print("Song nicht gefunden.")
            return

        playlist.add_song(song)
        self.save_data()
        print(f"{song.title} zur Playlist {playlist.name} hinzugefügt.")

    def remove_song_from_playlist(self):
        #Entfernt einen Song aus einer Playlist
        playlist_name = input("Gib den Namen der Playlist ein: ")
        playlist = next((pl for pl in self.playlists if pl.name == playlist_name), None)
        if not playlist:
            print("Playlist nicht gefunden.")
            return

        song_title = input("Gib den Namen des Songs ein, der entfernt werden soll: ")
        playlist.remove_song(song_title)
        self.save_data()

    def display_playlists(self):
        #Zeigt alle Playlists an
        if not self.playlists:
            print("Keine Playlists verfügbar.")
        else:
            for playlist in self.playlists:
                print(playlist)
                for song in playlist.songs:
                    print(f"  - {song}")

    def create_random_songs(self, count):
        #Erstellt eine bestimmte Anzahl zufälliger Songs
        for _ in range(count):
            title = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            artist = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            album = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            genre = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            self.add_song(title, artist, album, genre)

    def main_menu(self):
        #Hauptmenü der Musik-App
        while True:
            print("\n--- Musik-App ---")
            print("1. Neuen Song hinzufügen")
            print("2. Playlist erstellen")
            print("3. Song zur Playlist hinzufügen")
            print("4. Song aus Playlist entfernen")
            print("5. Songs suchen")
            print("6. Songs sortieren")
            print("7. Alle Songs anzeigen")
            print("8. Playlists anzeigen")
            print("9. Song aus Bibliothek löschen")
            print("10. Beenden")
            print("11. Zufällige Songs erstellen")

            choice = input("Gib deine Wahl ein: ").strip()

            if choice == '1':
                title = input("Gib den Titel des Songs ein: ").strip()
                artist = input("Gib den Namen des Künstlers ein: ").strip()
                album = input("Gib den Namen des Albums ein: ").strip()
                genre = input("Gib das Genre ein: ").strip()
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
                title = input("Gib den Titel des Songs ein, der gelöscht werden soll: ").strip()
                self.delete_song(title)
            elif choice == '10':
                print("Musik-App wird beendet. Auf Wiedersehen!")
                break
            elif choice == '11':
                count = int(input("Gib die Anzahl der zu erstellenden zufälligen Songs ein: "))
                self.create_random_songs(count)
            else:
                print("Ungültige Wahl. Bitte erneut auswählen.")

if __name__ == "__main__":
    #Startet die Musik-App, wenn das Skript direkt ausgeführt wird
    app = MusicApp()
    app.main_menu()

    