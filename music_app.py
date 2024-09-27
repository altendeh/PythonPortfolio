import os
import time
import random
import string
import sys
import tracemalloc
import copy
from song import Song
from playlist import Playlist
from red_black_tree import RedBlackTree

class MusicApp:
    FILENAME = "songs_RBT.csv"

    def __init__(self):
        #Initialisiert die Musik-App und lädt Songs
        self.songs = []
        self.sorted_songs_by_title = []
        self.sorted_songs_by_artist = []
        self.sorted_songs_by_genre = []
        self.playlists = []
        self.rbt = RedBlackTree()
        self.load_songs()

    def load_songs(self):
        if os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'r') as file:
                for line in file:
                    title, artist, album, genre = line.strip().split(',')
                    song = Song(title, artist, album, genre)
                    self.songs.append(song)
                    self.rbt.insert(song)
            self.sorted_songs_by_title = sorted(self.songs, key=lambda song: song.title)
            self.sorted_songs_by_artist = sorted(self.songs, key=lambda song: song.artist)
            self.sorted_songs_by_genre = sorted(self.songs, key=lambda song: song.genre)
            print(f"{len(self.songs)} Songs aus {self.FILENAME} geladen.")
            # Überprüfe die ersten paar Songs in jeder Liste
            print("Erste paar Songs nach Titel sortiert:", [song.title for song in self.sorted_songs_by_title[:5]])
            print("Erste paar Songs nach Künstler sortiert:", [song.artist for song in self.sorted_songs_by_artist[:5]])
            print("Erste paar Songs nach Genre sortiert:", [song.genre for song in self.sorted_songs_by_genre[:5]])
        else:
            print("Keine Songs gefunden. Starte mit einer leeren Musikbibliothek.")


    def save_data(self):
        print("save_data wurde aufgerufen.")  # Debug-Ausgabe
        # Ausgabe der Songs vor dem Speichern zur Überprüfung (zum Debuggen genutzt)
        #print("Songs vor dem Speichern:")
        #for song in self.songs:
        #    print(f"{song.title} - {song.artist} - {song.album} - {song.genre}")

        # Speichert alle Songs in einer Datei
        try:
            with open(self.FILENAME, 'w') as file:
                for song in self.songs:
                    file.write(f"{song.title},{song.artist},{song.album},{song.genre}\n")
            print(f"{len(self.songs)} Songs in {self.FILENAME} gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern der Datei: {e}")

        # Überprüfe die Datei nach dem Speichern (zum Debuggen genutzt)
        #self.verify_saved_data() 

    def verify_saved_data(self):
        try:
            with open(self.FILENAME, 'r') as file:
                lines = file.readlines()
                print("Gespeicherte Songs:")
                for line in lines:
                    print(line.strip())
        except Exception as e:
            print(f"Fehler beim Lesen der Datei: {e}")


    def add_song(self, title, artist, album, genre):
        #Fügt einen neuen Song zur Bibliothek hinzu und speichert die Daten
        song = Song(title, artist, album, genre)
        self.songs.append(song)
        self.sorted_songs_by_title = sorted(self.songs, key=lambda song: song.title)
        self.sorted_songs_by_artist = sorted(self.songs, key=lambda song: song.artist)
        self.sorted_songs_by_genre = sorted(self.songs, key=lambda song: song.genre)
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

    def measure_memory_and_time(self, method, *args):
        # Starten der Speicherverfolgung
        tracemalloc.start()

        # Messen der Speicherkapazität vor der Suche
        initial_snapshot = tracemalloc.take_snapshot()

        # Startzeit messen
        start_time = time.time()

        # Ausführen der Suchmethode
        result = method(*args)
        
        # Endzeit messen
        end_time = time.time()

        # Messen der Speicherkapazität nach der Suche
        final_snapshot = tracemalloc.take_snapshot()

        # Benötigte Zeit berechnen
        elapsed_time = end_time - start_time

        # Verwendete Speicherkapazität berechnen
        stats = final_snapshot.compare_to(initial_snapshot, 'lineno')
        used_memory = sum(stat.size_diff for stat in stats)

        # Speicherverfolgung stoppen
        tracemalloc.stop()

        return result, elapsed_time, used_memory
    
    

    def search_song(self):
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
        search_method_input = input("Wähle Suchmethode - (L)ineare Suche, (Bi)närsuche, (J)ump-Suche, (I)nterpolationssuche, (Br)eitensuche, (T)iefensuche oder (A)lle: ").strip().lower()

        search_methods_map = {
            'l': ('Lineare Suche', self.linear_search),
            'bi': ('Binärsuche', self.binary_search),
            'j': ('Jump-Suche', self.jump_search),
            'i': ('Interpolationssuche', self.interpolation_search),
            'br': ('Breitensuche', lambda v, c: self.rbt.bfs_search(v, c)),
            't': ('Tiefensuche', lambda v, c: self.rbt.dfs_search(self.rbt.root, v, c))
        }

        if search_method_input == 'a':
            results = []
            for method_key, (method_name, method) in search_methods_map.items():
                print(f"{method_name} wird ausgeführt...")  # Anzeige, dass der Algorithmus läuft
                result, elapsed_time, used_memory = self.measure_memory_and_time(method, value, criteria)
                results.append((method_name, result, elapsed_time, used_memory))
                print(f"{method_name}: '{result}' in der Musikbibliothek gefunden. Benötigte Zeit: {elapsed_time:.6f} Sekunden. Verwendete Speicherkapazität: {used_memory} Bytes.")

            # Übersicht über alle Suchalgorithmen
            print("\nÜbersicht über alle Suchalgorithmen:")
            for method_name, result, elapsed_time, used_memory in results:
                print(f"{method_name}: Benötigte Zeit: {elapsed_time:.6f} Sekunden. Verwendete Speicherkapazität: {used_memory} Bytes.")

        elif search_method_input in search_methods_map:
            method_name, method = search_methods_map[search_method_input]
            print(f"{method_name} wird ausgeführt...")  # Anzeige, dass der Algorithmus läuft
            result, elapsed_time, used_memory = self.measure_memory_and_time(method, value, criteria)
            if result:
                print(f"'{result}' in der Musikbibliothek gefunden.")
            else:
                print(f"'{value}' nicht in der Musikbibliothek gefunden.")

            print(f"Benötigte Zeit: {elapsed_time:.6f} Sekunden. Verwendete Speicherkapazität: {used_memory} Bytes.")
    
    def measure_memory_and_time(self, search_method, *args):
        tracemalloc.start()
        start_time = time.time()
    
        # Aufruf des Suchalgorithmus
        result = search_method(*args)
    
        elapsed_time = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    
        return result, elapsed_time, peak

        
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
    
    def binary_search(self, value, criteria):
        if criteria == 'title':
            sorted_songs = self.sorted_songs_by_title
        elif criteria == 'artist':
            sorted_songs = self.sorted_songs_by_artist
        elif criteria == 'genre':
            sorted_songs = self.sorted_songs_by_genre
        else:
            return None

        low = 0
        high = len(sorted_songs) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_value = getattr(sorted_songs[mid], criteria)

            if mid_value == value:
                return sorted_songs[mid]
            elif mid_value < value:
                low = mid + 1
            else:
                high = mid - 1

        return None


    
    def jump_search(self, value, criteria):
        """
        Führt eine Jump-Suche nach einem Song-Objekt in der sortierten Liste basierend auf einem Kriterium durch.

        Args:
            value (str): Der Wert des Suchkriteriums.
            criteria (str): Das Suchkriterium (z.B. 'title', 'artist', 'genre').

        Returns:
            Song: Der gefundene Song oder None, wenn kein Song gefunden wurde.
        """
        if criteria == 'title':
            sorted_songs = self.sorted_songs_by_title
        elif criteria == 'artist':
            sorted_songs = self.sorted_songs_by_artist
        elif criteria == 'genre':
            sorted_songs = self.sorted_songs_by_genre
        else:
            return None

        n = len(sorted_songs)
        step = int(n ** 0.5)  # Die Blockgröße für den Jump Search
        prev = 0

        # Springe durch die Liste in Schritten von 'step'
        while prev < n and getattr(sorted_songs[min(step, n) - 1], criteria) < value:
            prev = step
            step += int(n ** 0.5)
            if prev >= n:
                return None

        # Lineare Suche innerhalb des Blocks
        for i in range(prev, min(step, n)):
            if getattr(sorted_songs[i], criteria) == value:
                return sorted_songs[i]

        return None


    def interpolation_search(self, value, criteria):
        """
        Führt eine Interpolationssuche nach einem Song-Objekt in der sortierten Liste basierend auf einem Kriterium durch.

        Args:
            value (str): Der Wert des Suchkriteriums.
            criteria (str): Das Suchkriterium (z.B. 'title', 'artist', 'genre').

        Returns:
            Song: Der gefundene Song oder None, wenn kein Song gefunden wurde.
        """
        if criteria == 'title':
            sorted_songs = self.sorted_songs_by_title
        elif criteria == 'artist':
            sorted_songs = self.sorted_songs_by_artist
        elif criteria == 'genre':
            sorted_songs = self.sorted_songs_by_genre
        else:
            return None

        low = 0
        high = len(sorted_songs) - 1

        while low <= high:
            mid = low + (high - low) // 2
            mid_value = getattr(sorted_songs[mid], criteria)

            if mid_value == value:
                return sorted_songs[mid]
            elif mid_value < value:
                low = mid + 1
            else:
                high = mid - 1

        return None
    
    def search_all_methods(self, value, criteria):
        """
        Führt alle Suchmethoden nacheinander aus und gibt die Ergebnisse aus.

        Args:
            value (str): Der Wert des Suchkriteriums.
            criteria (str): Das Suchkriterium (z.B. 'title', 'artist', 'album').

        Returns:
            None
        """
        search_methods = {
            'Lineare Suche': self.linear_search,
            'Binärsuche': self.binary_search,
            'Jump-Suche': self.jump_search,
            'Interpolationssuche': self.interpolation_search,
            'Breitensuche': lambda v, c: self.rbt.bfs_search(v, c),
    'Tiefensuche': lambda v, c: self.rbt.dfs_search(self.rbt.root, v, c)
        }

        for method_name, method in search_methods.items():
            start_time = time.time()
            result = method(value, criteria)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if result:
                print(f"{method_name}: '{result}' in der Musikbibliothek gefunden. Benötigte Zeit: {elapsed_time:.6f} Sekunden.")
            else:
                print(f"{method_name}: '{value}' nicht in der Musikbibliothek gefunden. Benötigte Zeit: {elapsed_time:.6f} Sekunden.")
                
    def measure_memory_and_time_sort(self, sort_method, *args):
    
        tracemalloc.start()
        start_time = time.time()

        # Aufruf des Sortieralgorithmus
        sort_method(*args)

        elapsed_time = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return  elapsed_time, peak

    def print_songs(self, message):
        print(message)
        for song in self.songs:
            print(f"{song.title} - {song.artist} - {song.album} - {song.genre}")


    def sort_songs(self):
       print("Wähle Sortieralgorithmus:")
       print("1. Bubble Sort")
       print("2. Insertion Sort")
       print("3. Merge Sort")
       print("4. Quick Sort")
       print("5. Alle")

       choice = input("Gib deine Wahl ein: ").strip()

       sort_methods_map = {
           '1': ('Bubble Sort', self.bubble_sort),
           '2': ('Insertion Sort', self.insertion_sort),
           '3': ('Merge Sort', self.merge_sort),
           '4': ('Quick Sort', self.quick_sort)
       }

       criteria_map = {
           '1': 'Titel',
           '2': 'Künstler',
           '3': 'Genre'
       }

       if choice == '5':
           order, criteria = self.get_sort_order_and_criteria("alle Algorithmen")
           if not order or not criteria:
               return

           criteria_name = criteria_map[criteria]
           results = []
           original_songs = copy.deepcopy(self.songs)  # Originaldatenstruktur kopieren

           for method_key, (method_name, method) in sort_methods_map.items():
               #print(f"{method_name} wird ausgeführt.")  # Debug-Ausgabe
               self.songs = copy.deepcopy(original_songs)  # Datenstruktur für jeden Algorithmus zurücksetzen

               if method_key == '4':  # Quick Sort
                   print("quick_sort wurde aufgerufen.")  # Debug-Ausgabe
                   elapsed_time, used_memory = self.measure_memory_and_time_sort(method, 0, len(self.songs) - 1, order, criteria)
               else:
                   elapsed_time, used_memory = self.measure_memory_and_time_sort(method, order, criteria)


            
               print(f"{method_name} (Sortierung nach {criteria_name}, {'aufsteigend' if order == '1' else 'absteigend'}): Sortierung abgeschlossen. Benötigte Zeit: {elapsed_time:.6f} Sekunden. Verwendete Speicherkapazität: {used_memory} Bytes.")
               results.append((method_name, elapsed_time, used_memory))

           # Übersicht über alle Laufzeiten und Speicherverbräuche
           print("\nÜbersicht über alle Sortieralgorithmen:")
           for method_name, elapsed_time, used_memory in results:
               print(f"{method_name}: Benötigte Zeit: {elapsed_time:.6f} Sekunden. Verwendete Speicherkapazität: {used_memory} Bytes.")

           self.save_data()  # Speichern der Daten nach Abschluss aller Sortierungen

       else:
           method_name, method = sort_methods_map.get(choice, (None, None))
           if method:
               order, criteria = self.get_sort_order_and_criteria(method_name)
               if order and criteria:
                   criteria_name = criteria_map[criteria]
                   #print(f"{method_name} wird ausgeführt.")  # Debug-Ausgabe
                   if method_name == 'Quick Sort':
                       print("quick_sort wurde aufgerufen.")  # Debug-Ausgabe
                       elapsed_time, used_memory = self.measure_memory_and_time_sort(method, 0, len(self.songs) - 1, order, criteria)
                   else:
                       elapsed_time, used_memory = self.measure_memory_and_time_sort(method, order, criteria)

                   
                   print(f"{method_name} (Sortierung nach {criteria_name}, {'aufsteigend' if order == '1' else 'absteigend'}): Sortierung abgeschlossen. Benötigte Zeit: {elapsed_time:.6f} Sekunden. Verwendete Speicherkapazität: {used_memory} Bytes.")
                   self.save_data()  # Speichern der Daten nach Abschluss der Sortierung
           else:
               print("Ungültige Wahl. Bitte versuche es erneut.")
    



    def get_sort_order_and_criteria(self, method_name):
        print(f"Wähle Sortierreihenfolge für {method_name}:")
        print("1. Aufsteigend")
        print("2. Absteigend")

        order = input("Gib deine Wahl ein: ").strip()
        if order not in ['1', '2']:
            print("Ungültige Sortierreihenfolge. Bitte wähle '1' für aufsteigend oder '2' für absteigend.")
            return None, None

        print(f"Wähle Sortierkriterium für {method_name}:")
        print("1. Titel")
        print("2. Künstler")
        print("3. Genre")

        criteria = input("Gib deine Wahl ein: ").strip()
        if criteria not in ['1', '2', '3']:
            print("Ungültiges Sortierkriterium. Bitte wähle '1' für Titel, '2' für Künstler oder '3' für Genre.")
            return None, None

        return order, criteria

            
    def bubble_sort(self, order, criteria):
        """
        Implementiert den Bubble Sort Algorithmus.

        Args:
            order (str): Die Sortierreihenfolge ('1' für aufsteigend, '2' für absteigend).
            criteria (str): Das Sortierkriterium ('1' für Titel, '2' für Künstler, '3' für Genre).

        Returns:
            None
        """
        print("bubble_sort wurde aufgerufen.")  # Debug-Ausgabe
        n = len(self.songs)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.compare(self.songs[j], self.songs[j + 1], order, criteria):
                    #print(f"Tausche {self.songs[j].title} mit {self.songs[j + 1].title}")  # Debug-Ausgabe
                    self.songs[j], self.songs[j + 1] = self.songs[j + 1], self.songs[j]
                    swapped = True
            if not swapped:
                break
        #self.print_songs("Songs nach dem Sortieren:")  # Debug-Ausgabe
        

    def insertion_sort(self, order, criteria):
        #Implementiert den Insertion Sort Algorithmus
        print("insertion_sort wurde aufgerufen.")  # Debug-Ausgabe
        for i in range(1, len(self.songs)):
            key_song = self.songs[i]
            j = i - 1
            while j >= 0 and self.compare(self.songs[j], key_song, order, criteria):
                self.songs[j + 1] = self.songs[j]
                j -= 1
            self.songs[j + 1] = key_song
    

    def merge_sort(self, order, criteria):
        print("merge_sort wurde aufgerufen.")  # Debug-Ausgabe
        self.songs = self._merge_sort(self.songs, order, criteria)
        

    def _merge_sort(self, array, order, criteria):
        if len(array) <= 1:
            return array

        mid = len(array) // 2
        left_half = self._merge_sort(array[:mid], order, criteria)
        right_half = self._merge_sort(array[mid:], order, criteria)

        return self.merge(left_half, right_half, order, criteria)

    def merge(self, left, right, order, criteria):
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
        #print("quick_sort wurde aufgerufen.")  #an andere Stelle verschoben, da nur einmal gezeigt werden soll
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

    def compare(self, song1, song2, ascending, criteria):
        #Vergleicht zwei Song-Objekte basierend auf einem Kriterium und der Sortierreihenfolge
        if criteria == '1':  #Titel
            comparison = song1.title > song2.title
        elif criteria == '2':  #Künstler
            comparison = song1.artist > song2.artist
        elif criteria == '3':  #Genre
            comparison = song1.genre > song2.genre
        #else:
        #    comparison = song1.title > song2.title  #Standardmäßig nach Titel sortieren, wenn das Kriterium ungültig ist

        result = comparison if ascending == '1' else not comparison
        #print(f"Vergleiche {song1.title} mit {song2.title} nach {criteria}: {result}")  # Debug-Ausgabe
        return result
    

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
        # Startzeit messen
        start_time = time.time()
    
        #Erstellt eine bestimmte Anzahl zufälliger Songs und speichert sie auf einmal
        for _ in range(count):
            title = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            artist = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            album = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            genre = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 10)))
            song = Song(title, artist, album, genre)
            self.songs.append(song)
            self.rbt.insert(song)  #Fügt den Song in den Rot-Schwarz-Baum ein

    # Sortiere die Listen nach dem Hinzufügen der zufälligen Songs
        self.sorted_songs_by_title = sorted(self.songs, key=lambda song: song.title)
        self.sorted_songs_by_artist = sorted(self.songs, key=lambda song: song.artist)
        self.sorted_songs_by_genre = sorted(self.songs, key=lambda song: song.genre)
        
        self.save_data()
        
        # Endzeit messen
        end_time = time.time()
        
        # Benötigte Zeit berechnen
        elapsed_time = end_time - start_time
        
        # Größe des RBT berechnen
        rbt_size = self.rbt.get_size()
        
        # Größe der Listen berechnen
        lists_size = (sys.getsizeof(self.sorted_songs_by_title) +
                      sys.getsizeof(self.sorted_songs_by_artist) +
                      sys.getsizeof(self.sorted_songs_by_genre))
        
        total_size = rbt_size + lists_size
        
        print(f"{count} zufällige Songs erstellt, in einem Rot-Schwarz-Baum gespeichert und die Listen sortiert.")
        print(f"Benötigte Zeit: {elapsed_time:.6f} Sekunden.")
        print(f"Speicherkapazität des RBT: {rbt_size} Bytes.")
        print(f"Speicherkapazität der Listen: {lists_size} Bytes.")
        print(f"Gesamte Speicherkapazität: {total_size} Bytes.")


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

    