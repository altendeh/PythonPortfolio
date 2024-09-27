import sys

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
    
    def get_size(self):
        def node_size(node):
            if node == self.NIL:
                return 0
            return (sys.getsizeof(node) + sys.getsizeof(node.song) +
                    node_size(node.left) + node_size(node.right))

        return node_size(self.root)
    

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
        """
        Führt eine Tiefensuche (DFS) nach einem Song-Objekt im Rot-Schwarz-Baum basierend auf einem Kriterium durch.

        Args:
            node (RedBlackNode): Der aktuelle Knoten im Baum.
            value (str): Der Wert des Suchkriteriums.
            criteria (str): Das Suchkriterium (z.B. 'title', 'artist').

        Returns:
            Song: Der gefundene Song oder None, wenn kein Song gefunden wurde.
        """
        if node == self.NIL:
            return None
        if getattr(node.song, criteria) == value:
            return node.song
        left_search = self.dfs_search(node.left, value, criteria)
        if left_search is not None:
            return left_search
        return self.dfs_search(node.right, value, criteria)

    def search(self, value, criteria):
        return self._search_recursive(self.root, value, criteria)

    def _search_recursive(self, node, value, criteria):
        if node == self.NIL:
            return None
        if getattr(node.song, criteria) == value:
            return node.song
        if value < getattr(node.song, criteria):
            return self._search_recursive(node.left, value, criteria)
        else:
            return self._search_recursive(node.right, value, criteria)
        
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