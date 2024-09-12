# Musik-Anwendung

## Übersicht
Diese Musik-Anwendung ermöglicht es Benutzern, eine Bibliothek von Liedern zu verwalten, Playlists zu erstellen und zu verwalten sowie verschiedene Operationen wie Hinzufügen, Entfernen, Suchen und Sortieren von Liedern durchzuführen. Die Anwendung verwendet einen Rot-Schwarz-Baum bzw. einen Binären Suchbaum für eine effiziente Verwaltung der Lieder.

## Anleitung
Um die Musik-Anwendung zu verwenden, führen Sie das Skript aus. Das Hauptmenü bietet Optionen zum Hinzufügen neuer Lieder, Erstellen von Playlists, Hinzufügen von Liedern zu Playlists, Entfernen von Liedern aus Playlists, Suchen von Liedern, Sortieren von Liedern, Anzeigen aller Lieder, Anzeigen von Playlists, Löschen von Liedern aus der Bibliothek und Erstellen zufälliger Lieder.

## Beispiel

```python
if __name__ == "__main__":
    app = MusicApp()
    app.main_menu()
```




## Vorgehen

1. **Anforderungen analysiert**:
   - Die grundlegenden Funktionen der Anwendung wurden definiert, einschließlich Hinzufügen, Entfernen, Suchen und Sortieren von Liedern.
   - Die zu verwendenden Datenstrukturen wurden bestimmt, Rot-Schwarz-Baum und Binärer Suchbaum.

2. **Design der Anwendung abgeschlossen**:
   - Die Klassen und ihre Methoden wurden entworfen, um die Anforderungen zu erfüllen.
   - Ein Klassendiagramm wurde erstellt, um die Beziehungen zwischen den Klassen zu visualisieren. (siehe Klassen und Methoden)

3. **Implementierung durchgeführt**:
   - Die `Song`-Klasse und ihre Methoden wurden implementiert.
   - Die `Playlist`-Klasse und ihre Methoden wurden implementiert.
   - Die `RedBlackTree`- und `BinarySearchTree`-Klassen sowie deren Knotenklassen (`RedBlackNode` und `TreeNode`) wurden implementiert.
   - Die `MusicApp`-Klasse und ihre Methoden wurden implementiert.

4. **Tests durchgeführt**:
   - Unit-Tests für jede Klasse und Methode wurden geschrieben, um deren korrekte Funktion sicherzustellen.
   - Die Anwendung wurde als Ganzes getestet, um sicherzustellen, dass alle Komponenten zusammenarbeiten.

5. **Dokumentation erstellt**:
   - Der Code wurde mit Kommentaren und Docstrings dokumentiert.
   - Eine Benutzeranleitung wurde erstellt, die erklärt, wie die Anwendung verwendet wird.

6. **Optimierung durchgeführt**:
   - Die Leistung der Such- und Sortieralgorithmen wurde analysiert.
   - Der Code wurde optimiert, um die Effizienz zu verbessern.

## Klassen und Methoden

### 1. Song-Klasse
Repräsentiert ein Lied mit Attributen wie Titel, Künstler, Album und Genre.

#### Methoden:
- `__init__(self, title, artist, album, genre)`: Initialisiert ein Song-Objekt.
- `__str__(self)`: Gibt eine lesbare Darstellung des Liedes zurück.
- `__lt__(self, other)`: Vergleichsoperator für "kleiner als" basierend auf dem Titel.
- `__eq__(self, other)`: Vergleichsoperator für Gleichheit basierend auf dem Titel.
- `to_dict(self)`: Konvertiert das Song-Objekt in ein Wörterbuch.
- `from_dict(data)`: Erstellt ein Song-Objekt aus einem Wörterbuch.

### 2. Playlist-Klasse
Repräsentiert eine Playlist, die eine Liste von Liedern enthält.

#### Methoden:
- `__init__(self, name)`: Initialisiert eine Playlist mit einem Namen und einer leeren Liedliste.
- `add_song(self, song)`: Fügt ein Lied zur Playlist hinzu.
- `remove_song(self, title)`: Entfernt ein Lied aus der Playlist basierend auf dem Titel.
- `__str__(self)`: Gibt eine lesbare Darstellung der Playlist zurück.
- `to_dict(self)`: Konvertiert die Playlist in ein Wörterbuch.
- `from_dict(data)`: Erstellt eine Playlist aus einem Wörterbuch.

### 3.1 RedBlackNode-Klasse
Repräsentiert einen Knoten im Rot-Schwarz-Baum.

#### Methoden:
- `__init__(self, song)`: Initialisiert einen Knoten mit einem Lied und setzt die Standardfarbe auf Rot.

### 3.2 TreeNode-Klasse
Repräsentiert einen Knoten im binären Suchbaum.

#### Methoden:
- `__init__(self, song)`: Initialisiert einen Knoten mit einem Lied und setzt die linken und rechten Kinder auf None.

### 4.1 RedBlackTree-Klasse 
Repräsentiert einen Rot-Schwarz-Baum für eine effiziente Verwaltung der Lieder.

#### Methoden:
- `__init__(self)`: Initialisiert den Rot-Schwarz-Baum mit einem NIL-Knoten.
- `insert(self, song)`: Fügt ein neues Lied in den Baum ein.
- `fix_insert(self, node)`: Korrigiert den Baum nach dem Einfügen, um die Rot-Schwarz-Eigenschaften zu erhalten.
- `left_rotate(self, x)`: Führt eine Linksrotation durch.
- `right_rotate(self, x)`: Führt eine Rechtsrotation durch.
- `search_iterative(self, value, criteria)`: Iterative Suche nach einem Lied basierend auf einem Kriterium.
- `_search_recursive(self, node, value, criteria)`: Rekursive Suche nach einem Lied basierend auf einem Kriterium.
- `bfs_search(self, value, criteria)`: Breitensuche nach einem Lied basierend auf einem Kriterium.
- `dfs_search(self, node, value, criteria)`: Tiefensuche nach einem Lied basierend auf einem Kriterium.
- `delete(self, song)`: Löscht ein Lied aus dem Baum.
- `_delete_recursive(self, node, song)`: Rekursive Methode zum Löschen eines Liedes.
- `_min_value_node(self, node)`: Findet den Knoten mit dem minimalen Wert.

### 4.2 BinarySearchTree-Klasse
Repräsentiert einen binären Suchbaum für eine effiziente Verwaltung der Lieder.

#### Methoden:
- `__init__(self)`: Initialisiert den binären Suchbaum mit der Wurzel als None.
- `insert(self, song)`: Fügt ein neues Lied in den Baum ein.
- `_insert_recursive(self, node, song)`: Hilfsmethode zum rekursiven Einfügen eines Liedes in den Baum.
- `search_recursive(self, node, value, criteria)`: Rekursive Suche nach einem Lied basierend auf einem Kriterium.
- `search_iterative(self, value, criteria)`: Iterative Suche nach einem Lied basierend auf einem Kriterium.
- `bfs_search(self, value, criteria)`: Breitensuche nach einem Lied basierend auf einem Kriterium.
- `dfs_search(self, node, value, criteria)`: Tiefensuche nach einem Lied basierend auf einem Kriterium.
- `delete(self, song)`: Löscht ein Lied aus dem Baum.
- `_delete_recursive(self, node, song)`: Rekursive Methode zum Löschen eines Liedes.
- `_min_value_node(self, node)`: Findet den Knoten mit dem minimalen Wert.

### 5. MusicApp-Klasse
Hauptklasse für die Musik-Anwendung.

#### Methoden:
- `__init__(self)`: Initialisiert die Musik-App und lädt Lieder.
- `load_data(self)`: Lädt Lieder aus einer Datei.
- `save_data(self)`: Speichert alle Lieder in einer Datei.
- `add_song(self, title, artist, album, genre)`: Fügt ein neues Lied zur Bibliothek hinzu und speichert die Daten.
- `delete_song(self, title)`: Löscht ein Lied aus der Bibliothek und speichert die Daten.
- `display_all_songs(self)`: Zeigt alle Lieder in der Bibliothek an.
- `search_song(self)`: Sucht nach einem Lied basierend auf einem Kriterium und einer Suchmethode.
- `sort_songs(self)`: Sortiert die Lieder basierend auf einem Kriterium und einer Sortiermethode.
- `bubble_sort(self, ascending, criteria)`: Implementiert den Bubble-Sort-Algorithmus.
- `insertion_sort(self, ascending, criteria)`: Implementiert den Insertion-Sort-Algorithmus.
- `merge_sort(self, songs, ascending, criteria)`: Implementiert den Merge-Sort-Algorithmus.
- `merge(self, left, right, ascending, criteria)`: Hilfsmethode für Merge Sort.
- `quick_sort(self, low, high, ascending, criteria)`: Implementiert den Quick-Sort-Algorithmus.
- `partition(self, low, high, ascending, criteria)`: Hilfsmethode für Quick Sort.
- `compare(self, song1, song2, criteria, ascending)`: Vergleicht zwei Lieder basierend auf dem Kriterium und der Reihenfolge.
- `create_playlist(self)`: Erstellt eine neue Playlist.
- `add_song_to_playlist(self)`: Fügt ein Lied zu einer Playlist hinzu.
- `remove_song_from_playlist(self)`: Entfernt ein Lied aus einer Playlist.
- `display_playlists(self)`: Zeigt alle Playlists an.
- `create_random_songs(self, count)`: Erstellt eine bestimmte Anzahl zufälliger Lieder.
- `main_menu(self)`: Hauptmenü der Musik-App.

## Suchalgorithmen

### Iterative Suche
- **Big O Notation**: $$O(n)$$
- **Funktionsweise**: Diese Methode durchsucht die Elemente der Datenstruktur nacheinander, bis das gesuchte Element gefunden wird oder alle Elemente durchsucht wurden.

### Rekursive Suche
- **Big O Notation**: $$O(n)$$
- **Funktionsweise**: Ähnlich wie die iterative Suche, aber sie verwendet Rekursion, um die Elemente zu durchsuchen. Dies kann zu einer höheren Speicherbelastung führen.

### Breitensuche (BFS)
- **Big O Notation**: $$O(V + E)$$, wobei V die Anzahl der Knoten und E die Anzahl der Kanten ist.
- **Funktionsweise**: BFS durchsucht die Knoten eines Graphen schichtweise, beginnend bei einem Startknoten und erkundet alle Nachbarn, bevor es zu den Nachbarn der Nachbarn übergeht.

### Tiefensuche (DFS)
- **Big O Notation**: $$O(V + E)$$
- **Funktionsweise**: DFS durchsucht die Knoten eines Graphen, indem es so tief wie möglich in einen Zweig des Graphen geht, bevor es zurückkehrt und andere Zweige erkundet.

## Sortieralgorithmen

### Bubble Sort
- **Big O Notation**: $$O(n^2)$$
- **Funktionsweise**: Vergleicht benachbarte Elemente und vertauscht sie, wenn sie in der falschen Reihenfolge sind. Dieser Vorgang wird wiederholt, bis die Liste sortiert ist.

### Insertion Sort
- **Big O Notation**: $$O(n^2)$$
- **Funktionsweise**: Baut die sortierte Liste schrittweise auf, indem es jedes neue Element an die richtige Position in der bereits sortierten Liste einfügt.

### Merge Sort
- **Big O Notation**: $$O(n \log n)$$
- **Funktionsweise**: Teilt die Liste wiederholt in zwei Hälften, sortiert jede Hälfte rekursiv und fügt die sortierten Hälften dann zusammen.

### Quick Sort
- **Big O Notation**: $$O(n \log n)$$ im Durchschnitt, $$O(n^2)$$ im schlimmsten Fall
- **Funktionsweise**: Wählt ein "Pivot"-Element und partitioniert die Liste so, dass alle Elemente kleiner als das Pivot links und alle größeren rechts sind. Sortiert dann rekursiv die Teillisten.

