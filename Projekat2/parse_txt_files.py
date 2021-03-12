# import pdftotext
import os
import re
from trie import *
from graf import *
pg_num_dif = 0

class Page(object):
    def __init__(self, index, page_num, content, trie, reference):
        self.index = index
        self.page_num = page_num
        self.content = content
        self.trie = trie
        self.reference = reference


def read_results_from_files(root):
    filenames = os.listdir(root)
    graph = Graph(True)
    result = {}
    global pgnum_ind_dif
    for filename in filenames:
        index = int(filename.split(".")[0])
        content = read_results_from_file(os.path.join(root, filename)).decode('utf-8')
        content.lower()
        try:
            page_number = int(content[:content.index('\n')].split()[-1])
            pgnum_ind_dif = int(index) - page_number
        except:
            try:
                page_number = int(content[:content.index('\n')].split()[0])
                pgnum_ind_dif = int(index) - page_number
            except:
                page_number = None
        #index = filename.split(".")[0]
        trie, reference = create_structTrie(content)
        if len(reference) == 0:
            reference = None
            page = Page(index, page_number, content, trie, None)
        else:
            page = Page(index, page_number, content, trie, reference)
        result[index] = page
        graph.insert_vertex(index)
    # for key in result:
    #     print(key)
    for key in result:
        one_page = result[key]
        if one_page.reference == None:
            continue
        for ref in one_page.reference:
            ref += pgnum_ind_dif
            # print(ref)
            # nova = result[ref]
            graph.insert_edge(key, ref)
            # print(str(key) + "->" + str(ref))
    # print(graph._incoming[664])
    return graph, result

def create_structTrie(content):
    trie = Trie()
    see_on = ["see on page", "see pages", "see page", "on page"]
    ref_exists = False
    indeks = 0
    ok = 0
    reference = []
    list_words = [x.lower() for x in re.sub("[^\w]", " ", content).split()]
    for phrase in see_on:
        if phrase in content:
            text = content.split(phrase)
            brojac = 0
            for part in text:
                if brojac == 0:
                    brojac +=1
                    continue
                i = 0
                part_list =[y.lower() for y in re.sub("[^\w]", " ", part).split()]

                while ok != 2:
                    try:
                        pg_ref_ind = int(part_list[i])
                        i += 1
                        reference.append(pg_ref_ind)
                    except:
                        ok += 1
                        i += 1

    for word in list_words:
        word = word.lower()
        trie.insert(word, indeks)
        indeks += 1

    return trie, reference


def read_results_from_file(path):
    with open(path, 'rb') as file:
        return file.read()


def print_dict(dict):
    for key in dict:
        page = dict[key]
        print('Index: %s' % key)
        print('Page number: %s' % page['page_number'])
        print('Content:\n\n' + page['content'])
        print('\n\n\n')

def load():
    in_path = 'Data Structures and Algorithms in Python.pdf'
    out_path = 'Data Structures and Algorithms in Python'
    # content = get_pdf_content(in_path, out_path)
    # results = read_results_from_files(out_path)
    # print_dict(results)
    global pg_num_dif
    graph, result = read_results_from_files(out_path)
    return graph, result, pg_num_dif

if __name__ == '__main__':
    load()

    # in_path = 'Data Structures and Algorithms in Python.pdf'
    # out_path = 'Data Structures and Algorithms in Python'
    # #content = get_pdf_content(in_path, out_path)
    # results = read_results_from_files(out_path)
    # print_dict(results)
    # recnik = {}
    # word = input("Unesi rec: ")
    # for key, value in results.items():
    #     node = value["trie"].search(word)
    #     if node != None:
    #         recnik[key] = [node.counter, node.index]
    #         print(recnik[key])