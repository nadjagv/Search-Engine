from parse_txt_files import *
from search import *
import os
difference = 0
rec = ""
import sys


def print_results(list, pg_dict, diff, words, avoid):
    global rec
    i = 1
    if len(list) == 0:
        print("No matches.")
        return
    print("Found " + str(len(list)) + " matches.")
    for tuple in list:
        pg_index = tuple[0]
        page = pg_dict[pg_index]
        pg_num = page.page_num
        content = page.content
        content = [x.lower() for x in re.sub("[^\w]", " ", content).split()]
        trie = page.trie
        for rec in words:
            if rec == "and" or rec == "or" or rec == "not":
                continue

            elif rec in avoid:
                continue
            node = trie.search(rec)
            if node == None:
                continue
            text_index = node.index
            break

        if text_index < 10:
            begin = 0
            end = text_index + 10
        elif len(content) - text_index < 10:
            end = len(content) - 1
            begin = text_index - 10
        else:
            begin = text_index - 10
            end = text_index + 10
        pre = ""
        aft = ""
        mid = 0
        for position in range(begin, end):
            if position == text_index:
                mid += 1
                continue
            if mid == 1:
                aft = aft + content[position] + " "
                continue
            pre = pre + content[position] + " "

        # print(str(i) + ".   " + str(pg_num) + "\n" + text + "\n\n")
        print(str(i) + ".   " + "Page number: " + str(pg_num) + "\n" + pre + '\x1b[6;30;42m' + rec + '\x1b[0m' + " " + aft + "\n\n")

        nastavi = 0
        if i % 15 == 0:
            answer = input("Show next 15 results? (y - yes, n - no)")
            answer.lower()
            if answer == "y" or answer == "yes":
                nastavi = 0
            else:
                nastavi = 1

        if nastavi != 0:
            break
        i += 1

def sort_results(results_dict):
    sorted_dict = sorted(results_dict.items(), key=lambda x:x[1])
    sorted_dict.reverse()
    return sorted_dict

def begin_search(graph, pg_dict, words, contains_quote):
    i = 0
    results_index = []
    results_dict = {}
    final = set()
    final_set = set()
    brojac = -1
    remove = []
    avoid = []

        # if " " in current:
        #     QUOTEsearch(graph, pg_dict, current, next)
        # if next == "and":
        #     next = words[i + 2]
        #     ANDsearch(graph, pg_dict, current, next)
        #     i += 2
        # elif next == "or":
        #     next = words[i + 2]
        #     ORsearch(graph, pg_dict, current, next)
        #     i += 2
        # elif next == "not":
        #     next = words[i + 2]
        #     NORMALsearch(graph, pg_dict, current)
        #     NOTsearch(graph, pg_dict, next)
        #     i += 2
        # else:
        #     NORMALsearch(graph, pg_dict, current)
        #     i += 1
    while i < len(words):
        both = []
        final_set.clear()
        current = words[i]
        # next = words[i + 1]
        if current == "and" or current == "or" or current == "not":
            i += 1
            continue
        brojac += 1
        found_pages_dict, found_pages_index = NORMALsearch(graph, pg_dict, current) #return dict index: score
        global rec
        if len(found_pages_index) != 0 and rec == "":
            rec = current
        if i > 0:
            previous = words[i - 1]
            if previous == "and":
                try:
                    set1 = final
                    set2 = set(found_pages_index)
                    final = set1.intersection(set2)
                    results_index.append(final)
                    remove = remove + list(set1.difference(final))
                except:
                    final_set = set(found_pages_index)
                    results_index.append(final_set)
                    final = final.union(final_set)
            elif previous == "or":
                try:
                    set1 = final
                    set2 = set(found_pages_index)
                    final = set1.union(set2)
                    results_index.append(final)
                    # both = set1.intersection(set2)

                except:
                    final_set = set(found_pages_index)
                    results_index.append(final_set)
                    final = final.union(final_set)
            elif previous == "not":
                try:
                    avoid.append(current)
                    set1 = final
                    set2 = set(found_pages_index)
                    final = set1.difference(set2)
                    results_index.append(final)
                    remove = remove + found_pages_index
                except:
                    final_set = set(found_pages_index)
                    results_index.append(final_set)
                    final = final.union(final_set)
            else:
                final_set = set(found_pages_index)
                results_index.append(final_set)
                final = final.union(final_set)
        else:
            final_set = set(found_pages_index)
            results_index.append(final_set)
            final = final.union(final_set)
            # both = set1.intersection(set2)

        for k, v in found_pages_dict.items():
            if k not in final:
                continue
            if k not in results_dict.keys():
                results_dict[k] = 0
                results_dict[k] += v
            else:
                results_dict[k] += v + 20
            if k in remove:
                del results_dict[k]
                continue

        if len(remove) > 0:
            for key in remove:
                if key not in results_dict.keys():
                    continue
                del results_dict[key]
        i += 1

    return results_dict, avoid

def searching(graph, pg_dict, diff):
    string = input("Search input: ")
    string = string.lower()
    string = string.strip()
    # quote_index = [0]
    contains_quote = False
    # for char_index in range(len(string)):
    #     if string[char_index] == "\"":
    #         contains_quote = True
    #         quote_index.append(char_index)
    #
    # i = 0
    # words = []
    # if len(quote_index) > 0:
    #     while i < len(quote_index):
    #         beginning = quote_index[i] + 1
    #         if string[beginning] == "\"":
    #             beginning += 1
    #         if i+1 < len(quote_index):
    #             end = quote_index[i + 1]
    #             words.append(string[beginning:end])
    #         else:
    #             words.append(string[beginning:])
    #
    #         i += 1
    #
    # else:
    #     words = [y.lower() for y in re.sub("[^\w]", " ", string).split()]

    words = [y.lower() for y in re.sub("[^\w]", " ", string).split()]
    # words = string.split()
    results_dict, avoid = begin_search(graph, pg_dict, words, contains_quote)
    ranked_results = sort_results(results_dict)
    print_results(ranked_results, pg_dict, diff, words, avoid)


if __name__ == '__main__':
    graph, pg_dict, diff = load()
    while True:
        searching(graph, pg_dict, diff)
        answer = input("\nAnother search? (y - yes, n - no)")
        answer.lower()
        if answer == "y" or answer == "yes":
            continue
        else:
            print("\nBye bye")
            sys.exit()