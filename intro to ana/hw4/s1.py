from collections import defaultdict
import utility as U
import sys

class Webpage:
    def __init__(self):
        self.url = ""
        self.num_links = 0
        self.num_words = 0
        self.links = set()
        self.words = []
        self.weight = 1.0

class Word:
    def __init__(self):
        self.text = ""
        self.pages = set()
        self.num_pages = 0

class SearchEngine:

    def __init__(self):
        self.webpages_list = []
        self.links_map = {}
        self.words_map = {}
        self.load_data()
        self.clean_data()

    def load_data(self):
        with open('asu-domain.txt', 'r') as f:
        # with open('test.txt', 'r') as f:
            content = f.read().splitlines()

            temp_url = ""
            temp_page = Webpage()
            for line in content:
                if "URL:" in line:
                    url = line.split()[1].strip()
                    page = Webpage()
                    page.url = url
                    temp_url = url
                    temp_page = page
                    self.webpages_list.append(page)
                    self.links_map[url] = len(self.webpages_list) - 1

                elif "CONTENT:" in line:
                    words = line.split()[1:]
                    temp_page.words = words

                    for word in words:
                        if word not in self.words_map:
                            word_obj = Word()
                            word_obj.text = word
                            word_obj.pages.add(self.links_map[temp_url])
                            word_obj.num_pages = len(word_obj.pages)
                            self.words_map[word] = word_obj
                        else:
                            self.words_map[word].pages.add(self.links_map[temp_url])
                            self.words_map[word].num_pages = len(self.words_map[word].pages)

                if "LINKS:" in line:
                    links = line.split()[1:]
                    page.links.update(set(links))
                    page.num_links = len(page.links)

                line = f.readline()

    def clean_data(self):
        for url in self.webpages_list:
            new_links = []
            for i, link in enumerate(url.links):
                if link in self.links_map:
                    new_links.append(self.links_map[link])
            url.links.clear
            url.links = set(new_links)
            url.num_links = len(url.links)

        for url in self.webpages_list[:5]:
            print('page: {} \n \t links {}\n'.format(url.url, url.links))
    

    def calculate_pagerank(self, iterations=50):
        def debug(self):
            n = 0
            for link in self.webpages_list:
                n += link.weight
            print(n)
            print(len(self.webpages_list))

        
        N = len(self.webpages_list)
        d = 0.9  # Probability of following a link

        for _ in range(iterations):
            new_weight = [0.1 for _ in range(N)]  # Start with teleportation factor for each page

            for i, page in enumerate(self.webpages_list):
                if page.num_links > 0:
                    for link in page.links:
                        new_weight[link] += d * page.weight / page.num_links
                else:
                    # Redistribute the page's own weight if it has no outgoing links
                    new_weight[i] += page.weight * d

            # Update the weights after redistribution
            for i, page in enumerate(self.webpages_list):
                page.weight = new_weight[i]

        debug(self)


    def search(self, query):

        def getKey(map, value):
            return str( (list(map.keys())[list(map.values()).index(value)]) )
        
        def getContext(target, words):
            spacing = 5

            word_idx = words.index(target)
            start_idx = word_idx - spacing
            end_idx = word_idx + (spacing + 1)

            start_idx = 0 if start_idx < 0 else start_idx
            end_idx = len(words) - 1 if end_idx > len(words) - 1 else end_idx
            return ' '.join(words[start_idx:end_idx])
        
        clear_screen = "\x1b[2J\x1b[H"
        color_black = "\u001b[30m"
        color_red = "\u001b[31m"
        color_green = "\u001b[32m"
        sys.stdout.write(clear_screen)
        sys.stdout.write(color_green + "XABLAUU: ")

        if query in self.words_map:
            result = []

            word_data = self.words_map[query]

            result.append('{} pages match\n'.format(word_data.num_pages))
            
            pages = list(word_data.pages)
            sorted_pages = sorted(pages, key=lambda x: self.webpages_list[x].weight, reverse=True)

            if word_data.num_pages > 0:

                for page in sorted_pages[:5]:
                    t = self.webpages_list[page].words
                    weight = self.webpages_list[page].weight
                    result.append('[{}] {}'.format('%.3f' %weight, getKey(self.links_map, page)))
                    result.append(getContext(query,t))

            

            return result
        


def main():
    engine = SearchEngine()
    # engine.calculate_pagerank()
    

    # def search_function(query):
    #     return engine.search(query)
    
    # U.process_keystrokes(search_function)
    
main()


