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