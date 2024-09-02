MusicApp
MusicApp ist eine Python-Anwendung zur Verwaltung einer Musikbibliothek und von Playlists. Die Anwendung ermöglicht das Hinzufügen, Löschen, Suchen und Sortieren von Songs sowie das Erstellen und Verwalten von Playlists.

Klassen
Klasse Song
Die Song Klasse repräsentiert ein Lied mit Attributen wie Titel, Künstler, Album und Genre.

Attribute:
title: Der Titel des Songs.
artist: Der Künstler des Songs.
album: Das Album, in dem der Song enthalten ist.
genre: Das Genre des Songs.
Methoden:
__init__(self, title, artist, album, genre): Initialisiert ein Song-Objekt mit den angegebenen Attributen.
__str__(self): Gibt eine lesbare Darstellung des Songs zurück.
__lt__(self, other): Vergleichsoperator für weniger als, basierend auf dem Titel.
__eq__(self, other): Vergleichsoperator für Gleichheit, basierend auf dem Titel.
to_dict(self): Konvertiert das Song-Objekt in ein Wörterbuch.
from_dict(data): Erstellt ein Song-Objekt aus einem Wörterbuch.
Klasse Playlist
Die Playlist Klasse repräsentiert eine Playlist, die eine Sammlung von Songs enthält.

Attribute:
name: Der Name der Playlist.
songs: Eine Liste von Songs in der Playlist.
Methoden:
__init__(self, name): Initialisiert eine Playlist mit einem Namen und einer leeren Songliste.
add_song(self, song): Fügt einen Song zur Playlist hinzu.
remove_song(self, title): Entfernt einen Song aus der Playlist basierend auf dem Titel.
__str__(self): Gibt eine lesbare Darstellung der Playlist zurück.
to_dict(self): Konvertiert die Playlist in ein Wörterbuch.
from_dict(data): Erstellt eine Playlist aus einem Wörterbuch.
Klasse RedBlackNode
Die RedBlackNode Klasse repräsentiert einen Knoten in einem Rot-Schwarz-Baum.

Attribute:
song: Der Song, der im Knoten gespeichert ist.
color: Die Farbe des Knotens (rot oder schwarz).
left: Der linke Kindknoten.
right: Der rechte Kindknoten.
parent: Der Elternknoten.
Methoden:
__init__(self, song): Initialisiert einen Knoten für den Rot-Schwarz-Baum.
Klasse RedBlackTree
Die RedBlackTree Klasse repräsentiert einen Rot-Schwarz-Baum, der Songs speichert und sortiert.

Attribute:
NIL: Ein spezieller Knoten, der als Platzhalter für leere Knoten dient.
root: Der Wurzelknoten des Baums.
Methoden:
__init__(self): Initialisiert einen Rot-Schwarz-Baum mit einem NIL-Knoten.
insert(self, song): Fügt einen neuen Song in den Rot-Schwarz-Baum ein.
fix_insert(self, node): Fixiert den Baum nach dem Einfügen, um die Rot-Schwarz-Eigenschaften zu bewahren.
left_rotate(self, x): Führt eine Linksrotation durch.
right_rotate(self, x): Führt eine Rechtsrotation durch.
search_iterative(self, value, criteria): Iterative Suche nach einem Song basierend auf einem Kriterium.
_search_recursive(self, node, value, criteria): Rekursive Suche nach einem Song basierend auf einem Kriterium.
bfs_search(self, value, criteria): Breitensuche nach einem Song basierend auf einem Kriterium.
dfs_search(self, node, value, criteria): Tiefensuche nach einem Song basierend auf einem Kriterium.
delete(self, song): Löscht einen Song aus dem Rot-Schwarz-Baum.
_delete_recursive(self, node, song): Rekursive Methode zum Löschen eines Songs.
_min_value_node(self, node): Findet den Knoten mit dem minimalen Wert.
Klasse MusicApp
Die MusicApp Klasse repräsentiert die Hauptanwendung, die die Musikbibliothek und Playlists verwaltet.

Attribute:
FILENAME: Der Dateiname, unter dem die Songs gespeichert werden.
songs: Eine Liste von Songs in der Bibliothek.
rbt: Ein Rot-Schwarz-Baum, der die Songs speichert und sortiert.
playlists: Eine Liste von Playlists.
Methoden:
__init__(self): Initialisiert die Musik-App und lädt Songs.
load_songs(self): Lädt Songs aus einer Datei beim Start der App.
save_data(self): Speichert alle Songs in einer Datei.
add_song(self, title, artist, album, genre): Fügt einen neuen Song zur Bibliothek hinzu und speichert die Daten.
delete_song(self, title): Löscht einen Song aus der Bibliothek und speichert die Daten.
display_all_songs(self): Zeigt alle Songs in der Bibliothek an.
search_song(self): Sucht nach einem Song basierend auf einem Kriterium und einer Suchmethode.
sort_songs(self): Sortiert die Songs basierend auf einem Kriterium und einer Sortiermethode.
bubble_sort(self, order, criteria): Implementiert den Bubble Sort Algorithmus.
insertion_sort(self, order, criteria): Implementiert den Insertion Sort Algorithmus.
merge_sort(self, array, order, criteria): Implementiert den Merge Sort Algorithmus.
merge(self, left, right, order, criteria): Hilfsmethode für Merge Sort.
quick_sort(self, low, high, order, criteria): Implementiert den Quick Sort Algorithmus.
partition(self, low, high, order, criteria): Hilfsmethode für Quick Sort.
compare(self, song1, song2, order, criteria): Vergleicht zwei Songs basierend auf dem Kriterium und der Reihenfolge.
create_playlist(self): Erstellt eine neue Playlist.
add_song_to_playlist(self): Fügt einen Song zu einer Playlist hinzu.
remove_song_from_playlist(self): Entfernt einen Song aus einer Playlist.
display_playlists(self): Zeigt alle Playlists an.
create_random_songs(self, count): Erstellt eine bestimmte Anzahl zufälliger Songs.
main_menu(self): Hauptmenü der Musik-App.
