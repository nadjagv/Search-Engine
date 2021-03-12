from  parse_txt_files import *

def QUOTEsearch(graph, pg_dict, phrase):
    words = [y.lower() for y in re.sub("[^\w]", " ", phrase).split()]
    i = 0
    results_index = []
    results_dict = {}
    final = set()
    final_set = set()
    brojac = -1
    remove = []
    avoid = []

    while i < len(words):
        found_pages_index = []
        found_pages_dict = {}
        current = words[i]
        brojac = 0
        for key in pg_dict:
            score = 0
            page = pg_dict[key]
            trie = page.trie
            node = trie.search(current)
            if node == None:
                continue
            if brojac == 0:
                pos_index = node.index
                brojac += 1
            else:
                new_index = node.index
                if new_index - pos_index != 1:
                    continue
            score += node.counter
            incoming = graph._incoming[key]
            for k, v in incoming.items():
                score += 1
                page2 = pg_dict[v]
                trie2 = page2.trie
                node2 = trie2.search(current)
                if node2 == None:
                    continue
                score += node2.counter
            if score != 0:
                found_pages_index.append(key)
                found_pages_dict[key] = score

        return found_pages_dict, found_pages_index

    return results_dict, avoid

def ANDsearch(graph, pg_dict, current, next):
    pass


def ORsearch(graph, pg_dict, current, next):
    pass


def NOTsearch(graph, pg_dict, current, next):
    pass


def NORMALsearch(graph, pg_dict, current):
    found_pages_index = []
    found_pages_dict = {}
    for key in pg_dict:
        score = 0
        page = pg_dict[key]
        trie = page.trie
        node = trie.search(current)
        if node == None:
            continue
        score += node.counter
        incoming = graph._incoming[key]
        for k, v in incoming.items():
            score += 1
            page2 = pg_dict[v]
            trie2 = page2.trie
            node2 = trie2.search(current)
            if node2 == None:
                continue
            score += node2.counter
        if score != 0:
            found_pages_index.append(key)
            found_pages_dict[key] = score

    return found_pages_dict, found_pages_index



if __name__ == '__main__':
    pass