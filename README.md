Music Application
Overview
This music application allows users to manage a library of songs, create and manage playlists, and perform various operations such as adding, removing, searching, and sorting songs. The application uses a Red-Black Tree for efficient song management.

Classes and Methods
1. Song Class
Represents a song with attributes such as title, artist, album, and genre.

Methods:
__init__(self, title, artist, album, genre): Initializes a song object.
__str__(self): Returns a readable representation of the song.
__lt__(self, other): Less than comparison based on the title.
__eq__(self, other): Equality comparison based on the title.
to_dict(self): Converts the song object to a dictionary.
from_dict(data): Creates a song object from a dictionary.
2. Playlist Class
Represents a playlist containing a list of songs.

Methods:
__init__(self, name): Initializes a playlist with a name and an empty song list.
add_song(self, song): Adds a song to the playlist.
remove_song(self, title): Removes a song from the playlist based on the title.
__str__(self): Returns a readable representation of the playlist.
to_dict(self): Converts the playlist to a dictionary.
from_dict(data): Creates a playlist from a dictionary.
3. RedBlackNode Class
Represents a node in the Red-Black Tree.

Methods:
__init__(self, song): Initializes a node with a song and sets the default color to red.
4. RedBlackTree Class
Represents a Red-Black Tree for efficient song management.

Methods:
__init__(self): Initializes the Red-Black Tree with a NIL node.
insert(self, song): Inserts a new song into the tree.
fix_insert(self, node): Fixes the tree after insertion to maintain Red-Black properties.
left_rotate(self, x): Performs a left rotation.
right_rotate(self, x): Performs a right rotation.
search_iterative(self, value, criteria): Iterative search for a song based on a criterion.
_search_recursive(self, node, value, criteria): Recursive search for a song based on a criterion.
bfs_search(self, value, criteria): Breadth-First Search for a song based on a criterion.
dfs_search(self, node, value, criteria): Depth-First Search for a song based on a criterion.
delete(self, song): Deletes a song from the tree.
_delete_recursive(self, node, song): Recursive method to delete a song.
_min_value_node(self, node): Finds the node with the minimum value.
5. MusicApp Class
Main class for the music application.

Methods:
__init__(self): Initializes the music app and loads songs.
load_songs(self): Loads songs from a file.
save_data(self): Saves all songs to a file.
add_song(self, title, artist, album, genre): Adds a new song to the library and saves the data.
delete_song(self, title): Deletes a song from the library and saves the data.
display_all_songs(self): Displays all songs in the library.
search_song(self): Searches for a song based on a criterion and search method.
sort_songs(self): Sorts the songs based on a criterion and sorting method.
bubble_sort(self, order, criteria): Implements the Bubble Sort algorithm.
insertion_sort(self, order, criteria): Implements the Insertion Sort algorithm.
merge_sort(self, array, order, criteria): Implements the Merge Sort algorithm.
merge(self, left, right, order, criteria): Helper method for Merge Sort.
quick_sort(self, low, high, order, criteria): Implements the Quick Sort algorithm.
partition(self, low, high, order, criteria): Helper method for Quick Sort.
compare(self, song1, song2, order, criteria): Compares two songs based on the criterion and order.
create_playlist(self): Creates a new playlist.
add_song_to_playlist(self): Adds a song to a playlist.
remove_song_from_playlist(self): Removes a song from a playlist.
display_playlists(self): Displays all playlists.
create_random_songs(self, count): Creates a specified number of random songs.
main_menu(self): Main menu of the music app.
Usage
To use the music application, run the script. The main menu provides options to add new songs, create playlists, add songs to playlists, remove songs from playlists, search songs, sort songs, display all songs, display playlists, delete songs from the library, and create random songs.

Example
Python

if __name__ == "__main__":
    app = MusicApp()
    app.main_menu()
AI-generated code. Review and use carefully. More info on FAQ.
This will start the music application and display the main menu for user interaction.
