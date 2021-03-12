from typing import Tuple


# class TrieNode(object):
#     """
#    Our trie node implementation. Very basic. but does the job
#    """
#
#     def __init__(self, char: str):
#         self.char = char
#         self.children = []
#         # Is it the last character of the word.`
#         self.word_finished = False
#         # How many times this character appeared in the addition process
#         self.counter = 1
#         self.index = None


from typing import Tuple


# class TrieNode(object):
#     """
#    Our trie node implementation. Very basic. but does the job
#    """
#
#     def __init__(self, char: str):
#         self.char = char
#         self.children = []
#         # Is it the last character of the word.`
#         self.word_finished = False
#         # How many times this character appeared in the addition process
#         self.counter = 1
#
#
# class Trie(object):
#     def __init__(self):
#         self.root = TrieNode("*")
#
#     def add(self, word: str, index):
#         """
#        Adding a word in the trie structure
#        """
#         node = self.root
#         word = word.lower()
#         for char in word:
#             found_in_child = False
#             # Search for the character in the children of the present node
#             for child in node.children:
#                 if child.char == char:
#                     # We found it, increase the counter by 1 to keep track that another
#                     # word has it as well
#                     child.counter += 1
#                     # And point the node to the child that contains this char
#                     node = child
#                     found_in_child = True
#                     break
#             # We did not find it so add a new chlid
#             if not found_in_child:
#                 new_node = TrieNode(char)
#                 node.children.append(new_node)
#                 # And then point node to the new child
#                 node = new_node
#         # Everything finished. Mark it as the end of a word.
#         node.word_finished = True
#         node.index = index
#
#     def find_prefix(self, prefix: str) -> Tuple[bool, int]:
#         """
#        Check and return
#          1. If the prefix exsists in any of the words we added so far
#          2. If yes then how may words actually have the prefix
#        """
#         node = self.root
#         # If the root node has no children, then return False.
#         # Because it means we are trying to search in an empty trie
#         if not self.root.children:
#             return False, 0
#         for char in prefix:
#             char_not_found = True
#             # Search through all the children of the present node
#             for child in node.children:
#                 if child.char == char:
#                     # We found the char existing in the child.
#                     char_not_found = False
#                     # Assign node as the child containing the char and break
#                     node = child
#                     break
#             # Return False anyway when we did not find a char.
#             if char_not_found:
#                 return False, 0
#         # Well, we are here means we have found the prefix. Return true to indicate that
#         # And also the counter of the last node. This indicates how many words have this
#         # prefix
#         return True, node





class TrieNode():

    def __init__(self):
        self.children = {}
        self.terminating = False
        self.counter = 0
        self.index = -1
        self.first = 0


class Trie():

    def __init__(self):
        self.root = self.get_node()

    def get_node(self):
        return TrieNode()

    def get_index(self, ch):
        return ord(ch)

    def insert(self, word, content_index):

        root = self.root
        len1 = len(word)

        for i in range(len1):
            index = self.get_index(word[i])

            if index not in root.children:
                root.children[index] = self.get_node()
            root = root.children.get(index)

        root.terminating = True
        root.index = content_index
        root.counter += 1

    def search(self, word):
        root = self.root
        len1 = len(word)
        first = 0
        for i in range(len1):
            index = self.get_index(word[i])
            if first == 0:
                first = index
                root.first = first
            if not root:
                return None
            root = root.children.get(index)

        if root and root.terminating:
            return root
        else:
            return None


if __name__ == '__main__':


    strings = ["pqrs", "pprt", "psst", "qqrs", "pqrs"]

    t = Trie()
    index = 0
    for word in strings:
        t.insert(word, index)
        index += 1

    print(t.search("pqrs").index, t.search("pqrs").counter)


    # dict = {"w" : 2, "r" : 5}
    # dict["r"] += 3
    # print(dict["r"])


