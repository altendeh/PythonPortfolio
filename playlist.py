from song import Song

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
