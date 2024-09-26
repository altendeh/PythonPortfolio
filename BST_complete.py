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
        #Gibt eine String-Repräsentation des Song-Objekts zurück
        return f"{self.title} von {self.artist} - Album: {self.album}, Genre: {self.genre}"

    def __lt__(self, other):
        #Vergleicht zwei Song-Objekte basierend auf ihrem Titel für die Sortierung
        return self.title < other.title

    def __eq__(self, other):
        #Überprüft, ob zwei Song-Objekte basierend auf ihrem Titel gleich sind
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
        #Initialisiert ein Playlist-Objekt mit einem Namen und einer leeren Liste von Songs
        self.name = name
        self.songs = []

    def add_song(self, song):
        #Fügt ein Song-Objekt zur Playlist hinzu
        self.songs.append(song)

    def remove_song(self, title):
        #Entfernt ein Song-Objekt aus der Playlist basierend auf dem Titel
        song_to_remove = next((s for s in self.songs if s.title == title), None)
        if song_to_remove:
            self.songs.remove(song_to_remove)
            print(f"'{song_to_remove}' wurde aus der Playlist '{self.name}' entfernt.")
        else:
            print(f"'{title}' nicht in der Playlist '{self.name}' gefunden.")

    def __str__(self):
        #Gibt eine String-Repräsentation des Playlist-Objekts zurück
        return f"Playlist: {self.name}, Songs: {len(self.songs)}"

    def to_dict(self):
        #Konvertiert das Playlist-Objekt in ein Wörterbuch
        return {
            "name": self.name,
            "songs": [song.to_dict() for song in self.songs]
        }

    @staticmethod
    def from_dict(data):
        #Erstellt ein Playlist-Objekt aus einem Wörterbuch
        playlist = Playlist(data['name'])
        playlist.songs = [Song.from_dict(song_data) for song_data in data['songs']]
        return playlist

class TreeNode:
    def __init__(self, song):
        #Initialisiert ein TreeNode-Objekt mit einem Song-Objekt und linken/rechten Kindern als None
        self.song = song
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        #Initialisiert einen BinarySearchTree mit der Wurzel als None
        self.root = None

    def insert(self, song):
        #Fügt ein Song-Objekt in den binären Suchbaum ein
        if self.root is None:
            self.root = TreeNode(song)
        else:
            self._insert_recursive(self.root, song)

    def _insert_recursive(self, node, song):
        #Hilfsmethode zum rekursiven Einfügen eines Song-Objekts in den Baum
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
                

    def search_binary_recursive(self, node, value, criteria):
        #Sucht rekursiv binär nach einem Song-Objekt im Baum basierend auf einem Kriterium
        if node is None:
            return None
        if getattr(node.song, criteria) == value:
            return node.song
        if value < getattr(node.song, criteria):
            return self.search_binary_recursive(node.left, value, criteria)
        else:
            return self.search_binary_recursive(node.right, value, criteria)

    def search_binary_iterative(self, value, criteria):
        #Sucht iterativ binär nach einem Song-Objekt im Baum basierend auf einem Kriterium
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
        #Führt eine Breitensuche nach einem Song-Objekt im Baum basierend auf einem Kriterium durch
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
        #Führt eine Tiefensuche nach einem Song-Objekt im Baum basierend auf einem Kriterium durch
        if node is None:
            return None
        if getattr(node.song, criteria) == value:
            return node.song
        left_search = self.dfs_search(node.left, value, criteria)
        if left_search is not None:
            return left_search
        return self.dfs_search(node.right, value, criteria)
    

    def delete(self, song):
        #Löscht ein Song-Objekt aus dem binären Suchbaum
        self.root = self._delete_recursive(self.root, song)

    def _delete_recursive(self, node, song):
        #Hilfsmethode zum rekursiven Löschen eines Song-Objekts aus dem Baum
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
        #Findet den Knoten mit dem minimalen Wert im Baum
        current = node
        while current.left is not None:
            current = current.left
        return current

class MusicApp:
    FILENAME = "music_data_BST.json"

    def __init__(self):
        #Initialisiert die MusicApp mit einer leeren Liste von Songs und Playlists sowie einem binären Suchbaum
        self.songs = []
        self.playlists = []
        self.bst = BinarySearchTree()
        self.load_data()

    def load_data(self):
        """
        Lädt Daten aus einer JSON-Datei in die MusicApp.

        Diese Methode überprüft, ob die JSON-Datei existiert. Wenn ja, werden die Daten
        geladen und die Songs sowie Playlists initialisiert. Falls die Datei nicht existiert
        oder ein Fehler beim Laden auftritt, wird eine entsprechende Nachricht ausgegeben.

        :return: None
        """
        if os.path.exists(self.FILENAME):
            try:
                with open(self.FILENAME, 'r') as f:
                    data = json.load(f)
                    self.songs = [Song.from_dict(song_data) for song_data in data.get('songs', [])]
                    self.playlists = [Playlist.from_dict(pl_data) for pl_data in data.get('playlists', [])]
                    for song in self.songs:
                        self.bst.insert(song)
                print("Daten erfolgreich geladen.")
            except json.JSONDecodeError:
                print("Fehler beim Laden der Daten. Die Datei ist möglicherweise beschädigt.")
        else:
            print("Keine Daten gefunden. Starte mit einer leeren Datenbank.")


    def save_data(self):
        """
        Speichert den aktuellen Zustand der MusicApp in einer JSON-Datei.

        Diese Methode konvertiert die aktuellen Songs und Playlists in Wörterbücher
        und speichert sie in einer JSON-Datei. Falls ein Fehler beim Speichern auftritt,
        wird eine entsprechende Nachricht ausgegeben.

        :return: None
        """
        data = {
            "songs": [song.to_dict() for song in self.songs],
            "playlists": [playlist.to_dict() for playlist in self.playlists]
        }
        try:
            with open(self.FILENAME, 'w') as f:
                json.dump(data, f, indent=4)
            print("Daten erfolgreich gespeichert.")
        except IOError as e:
            print(f"Fehler beim Speichern der Daten: {e}")


    def add_song(self, title, artist, album, genre):
        """
        Fügt ein neues Song-Objekt zur MusicApp hinzu und speichert die Daten.

        Diese Methode erstellt ein neues Song-Objekt mit den angegebenen Parametern,
        fügt es zur Liste der Songs und zum binären Suchbaum (BST) hinzu und speichert
        anschließend die aktualisierten Daten in einer JSON-Datei.

        :param title: Titel des Songs
        :param artist: Name des Künstlers
        :param album: Name des Albums
        :param genre: Genre des Songs
        """
        song = Song(title, artist, album, genre)
        self.songs.append(song)
        self.bst.insert(song)  #In den binären Suchbaum einfügen
        self.save_data()  #Nach dem Hinzufügen eines Songs speichern
        print(f"'{song}' wurde zur Musikbibliothek hinzugefügt.")
        
    def delete_song(self, title):
        """
        Löscht ein Song-Objekt aus der MusicApp und speichert die Daten.

        Diese Methode sucht nach einem Song-Objekt basierend auf dem Titel,
        entfernt es aus der Liste der Songs und dem binären Suchbaum (BST),
        entfernt es aus allen Playlists und speichert anschließend die
        aktualisierten Daten in einer JSON-Datei.

        :param title: Titel des Songs, der gelöscht werden soll
        """
        song_to_delete = next((s for s in self.songs if s.title == title), None)
        if song_to_delete:
            self.songs.remove(song_to_delete)
            self.bst.delete(song_to_delete)  #Aus dem binären Suchbaum löschen
            for playlist in self.playlists:
                playlist.remove_song(title)  #Entfernt den Song aus allen Playlists
            self.save_data()  #Nach dem Löschen eines Songs speichern
            print(f"'{song_to_delete}' wurde aus deiner Musikbibliothek entfernt.")
        else:
            print(f"'{title}' nicht in deiner Musikbibliothek gefunden.")

    def display_all_songs(self):
        #Zeigt alle Song-Objekte in der MusicApp an
        if not self.songs:
            print("Keine Songs verfügbar.")
        else:
            for song in self.songs:
                print(song)

    def search_song(self):
        """
        Sucht nach einem Song-Objekt in der MusicApp basierend auf Benutzereingaben.

        Diese Methode ermöglicht es dem Benutzer, nach einem Song, Künstler oder Genre
        zu suchen. Der Benutzer kann die Suchmethode (rekursiv, iterativ, Breitensuche,
        Tiefensuche) und das Suchkriterium (Titel, Künstler, Genre) auswählen. Die
        Suchergebnisse und die benötigte Zeit werden angezeigt.

        :return: None
        """
        print("Suche nach einem Song, Künstler oder Genre:")
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
        search_method = input("Wähle Suchmethode - (L)ineare Suche, (R)ekursive Binärsuche, (I)terative Binärsuche, (B)reitensuche oder (T)iefensuche: ").strip().lower()

        start_time = time.time()  #Startzeitmessung

        if search_method == 'l':
            result = self.bst.linear_search(value, criteria)
        elif search_method == 'r':
            result = self.bst.search_binary_recursive(self.bst.root, value, criteria)
        elif search_method == 'i':
            result = self.bst.search_binary_iterative(value, criteria)
        elif search_method == 'b':
            result = self.bst.bfs_search(value, criteria)
        elif search_method == 't':
            result = self.bst.dfs_search(self.bst.root, value, criteria)
        else:
            print("Ungültige Suchmethode ausgewählt.")
            return

        end_time = time.time()  #Endzeitmessung
        elapsed_time = end_time - start_time

        if result:
            print(f"'{result}' in deiner Musikbibliothek gefunden.")
        else:
            print(f"'{value}' nicht in deiner Musikbibliothek gefunden.")

        print(f"Benötigte Zeit: {elapsed_time:.6f} Sekunden.")

    def linear_search(self, value, criteria):
        """
        Sucht linear nach einem Song-Objekt in der Liste basierend auf einem Kriterium.

        Args:
            criteria (str): Das Suchkriterium (z.B. 'title', 'artist').

        Returns:
            Song: Der gefundene Song oder None, wenn kein Song gefunden wurde.
        """
        for index, song in enumerate(self.songs):
            if getattr(song, criteria) == value:
                return song
        return None
    
    def sort_songs(self):
        """
        Sortiert die Song-Objekte in der MusicApp basierend auf Benutzereingaben.

        Diese Methode ermöglicht es dem Benutzer, die Songs nach Titel, Künstler oder
        Genre zu sortieren. Der Benutzer kann die Sortierreihenfolge (aufsteigend oder
        absteigend) und den Sortieralgorithmus (Bubble Sort, Insertion Sort, Merge Sort,
        Quick Sort) auswählen. Die sortierten Songs werden gespeichert und die benötigte
        Zeit wird angezeigt.

        :return: None
        """
        print("Wähle Sortierreihenfolge:")
        print("1. Aufsteigend")
        print("2. Absteigend")

        order_choice = input("Gib deine Wahl ein: ").strip()
        if order_choice not in ['1', '2']:
            print("Ungültige Sortierreihenfolge. Bitte wähle '1' für aufsteigend oder '2' für absteigend.")
            return
        ascending = order_choice == '1'
        

        print("Wähle Sortierkriterium:")
        print("1. Titel")
        print("2. Künstler")
        print("3. Genre")

        criteria_choice = input("Gib deine Wahl ein: ").strip()
        if criteria_choice not in ['1', '2', '3']:
            print("Ungültiges Sortierkriterium. Bitte wähle '1' für Titel, '2' für Künstler oder '3' für Genre.")
            return
        
        print("Wähle Sortieralgorithmus:")
        print("1. Bubble Sort")
        print("2. Insertion Sort")
        print("3. Merge Sort")
        print("4. Quick Sort")

        choice = input("Gib deine Wahl ein: ").strip()

        #Zeitmessung für das Sortieren der Songs
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
            print("Ungültige Wahl.")
            return
        
        print(f"Benötigte Zeit: {time.time() - start_time:.6f} Sekunden.")
        self.save_data()  #Speichert die sortierte Liste in der Datei

    def bubble_sort(self, ascending, criteria):
        #Implementiert den Bubble Sort Algorithmus zum Sortieren der Songs
        n = len(self.songs)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.compare(self.songs[j], self.songs[j + 1], criteria, ascending):
                    self.songs[j], self.songs[j + 1] = self.songs[j + 1], self.songs[j]
                    swapped = True
            if not swapped:
                break

    def insertion_sort(self, ascending, criteria):
        #Implementiert den Insertion Sort Algorithmus zum Sortieren der Songs
        for i in range(1, len(self.songs)):
            key_song = self.songs[i]
            j = i - 1
            while j >= 0 and self.compare(self.songs[j], key_song, criteria, ascending):
                self.songs[j + 1] = self.songs[j]
                j -= 1
            self.songs[j + 1] = key_song

    def merge(self, left, right, ascending, criteria):
        #Hilfsmethode zum Mergen von zwei Listen beim Merge Sort
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
        #Implementiert den Merge Sort Algorithmus zum Sortieren der Songs
        if len(songs) <= 1:
            return songs

        mid = len(songs) // 2
        left = self.merge_sort(songs[:mid], ascending, criteria)
        right = self.merge_sort(songs[mid:], ascending, criteria)

        return self.merge(left, right, ascending, criteria)

    def quick_sort(self, low, high, ascending, criteria):
        #Implementiert den Quick Sort Algorithmus zum Sortieren der Songs
        if low < high:
            pi = self.partition(low, high, ascending, criteria)
            self.quick_sort(low, pi - 1, ascending, criteria)
            self.quick_sort(pi + 1, high, ascending, criteria)

    def partition(self, low, high, ascending, criteria):
        #Hilfsmethode zum Partitionieren der Liste beim Quick Sort
        pivot = self.songs[high]
        i = low - 1

        for j in range(low, high):
            if self.compare(self.songs[j], pivot, criteria, ascending):
                i += 1
                self.songs[i], self.songs[j] = self.songs[j], self.songs[i]

        self.songs[i + 1], self.songs[high] = self.songs[high], self.songs[i + 1]
        return i + 1

    def compare(self, song1, song2, criteria, ascending):
        #Vergleicht zwei Song-Objekte basierend auf einem Kriterium und der Sortierreihenfolge
        if criteria == '1':  #Titel
            comparison = song1.title > song2.title
        elif criteria == '2':  #Künstler
            comparison = song1.artist > song2.artist
        elif criteria == '3':  #Genre
            comparison = song1.genre > song2.genre
        else:
            comparison = song1.title > song2.title  #Standardmäßig nach Titel sortieren, wenn das Kriterium ungültig ist

        return comparison if ascending else not comparison
    

    def create_playlist(self):
        """
        Erstellt eine neue Playlist und speichert die Daten.

        Diese Methode fordert den Benutzer auf, einen Namen für die neue Playlist einzugeben.
        Wenn eine Playlist mit diesem Namen bereits existiert, wird eine entsprechende Nachricht
        ausgegeben. Andernfalls wird die neue Playlist erstellt, zur Liste der Playlists
        hinzugefügt und die Daten werden gespeichert.

        :return: None
        """
        name = input("Gib den Namen der Playlist ein: ").strip()
        if any(pl.name == name for pl in self.playlists):
            print(f"Eine Playlist mit dem Namen '{name}' existiert bereits. Bitte wähle einen anderen Namen.")
            return
        playlist = Playlist(name)
        self.playlists.append(playlist)
        self.save_data()
        print(f"Playlist erstellt: {playlist}")

    def add_song_to_playlist(self):
        """
        Fügt einen Song zu einer bestehenden Playlist hinzu und speichert die Daten.

        Diese Methode fordert den Benutzer auf, den Namen der Playlist und den Titel des
        hinzuzufügenden Songs einzugeben. Wenn die Playlist oder der Song nicht gefunden
        werden, wird eine entsprechende Nachricht ausgegeben. Andernfalls wird der Song
        zur Playlist hinzugefügt und die Daten werden gespeichert.

        :return: None
        """
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
        """
        Entfernt einen Song aus einer bestehenden Playlist und speichert die Daten.

        Diese Methode fordert den Benutzer auf, den Namen der Playlist und den Titel des
        zu entfernenden Songs einzugeben. Wenn die Playlist nicht gefunden wird, wird eine
        entsprechende Nachricht ausgegeben. Andernfalls wird der Song aus der Playlist
        entfernt und die Daten werden gespeichert.

        :return: None
        """
        playlist_name = input("Gib den Namen der Playlist ein: ")
        playlist = next((pl for pl in self.playlists if pl.name == playlist_name), None)
        if not playlist:
            print("Playlist nicht gefunden.")
            return

        song_title = input("Gib den Namen des Songs ein, der entfernt werden soll: ")
        playlist.remove_song(song_title)
        self.save_data()


    def display_playlists(self):
        #Zeigt alle Playlists in der MusicApp an
        if not self.playlists:
            print("Keine Playlists verfügbar.")
        else:
            for playlist in self.playlists:
                print(playlist)
                for song in playlist.songs:
                    print(f"  - {song}")

    def create_random_songs(self, count):
        #Erstellt eine bestimmte Anzahl zufälliger Songs und fügt sie zur MusicApp hinzu
        for _ in range(count):
            title = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            artist = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            album = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            genre = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            song = Song(title, artist, album, genre)
            self.songs.append(song)
            self.bst.insert(song)  # In den binären Suchbaum einfügen

        self.save_data()  # Daten nur einmal nach dem Hinzufügen aller Songs speichern
        print(f"{count} zufällige Songs wurden zur Musikbibliothek hinzugefügt.")


    def main_menu(self):
        """
        Hauptmenü der MusicApp, das verschiedene Optionen zur Verwaltung der Musikbibliothek bietet.

        Diese Methode zeigt ein Menü mit verschiedenen Optionen an, die der Benutzer auswählen kann,
        um Songs hinzuzufügen, Playlists zu erstellen, Songs zu suchen, zu sortieren und vieles mehr.
        Die Methode läuft in einer Schleife, bis der Benutzer die Option zum Beenden auswählt.

        :return: None
        """
        while True:
            print("\n--- Music App ---")
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
                print("Music App wird beendet. Auf Wiedersehen!")
                break
            elif choice == '11':
                count = int(input("Gib die Anzahl der zu erstellenden zufälligen Songs ein: "))
                self.create_random_songs(count)
            else:
                print("Ungültige Wahl. Bitte erneut auswählen.")

if __name__ == "__main__":
    app = MusicApp()
    app.main_menu()