import sys
import heapq

alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

'''
This function is called by get_tokens function to process individual words.
A word could consist of many tokens. This function identifies individual
tokens from the beginning and end of words.
For example, the word ***Hobbit!! is broken into tokens *, *, *, Hobbit, ! and !.
This list of tokens is returned. Punctuations inbetween a word are ignored and treated as a single token.
This function is called by get_tokens.
'''
def process_word(word):
    frontlist = list()
    i = 0
    while i < len(word) and word[i] not in alphabets:
        frontlist = frontlist + list(word[i])
        i += 1
    
    endlist = list()
    start = i
    j = len(word) - 1
    while j >= i and word[j] not in alphabets:
        endlist = list(word[j])	+ endlist
        j -= 1

    wrd = ''
    if i <= j:
        wrd = word[i:j+1]
    
    wordlist = list()
    if frontlist != list():
        wordlist = wordlist + frontlist
    if wrd != '':
        wordlist = wordlist + [wrd]
    if endlist != list():
        wordlist= wordlist + endlist

    return wordlist

'''
Takes in a name of a file, and returns a list of tokens.
The list of tokens includes whitespaces (spaces, tabs and newlines) as separate tokens.
Makes use of process_word function.
'''
def get_tokens(filename):
    tokens = list()
    f = open(filename, 'r')

    for line in f:
        line = line.split(' ')
        
        for word in line:
            if word == '':
                # Caution! Some empty strings '' from the split method should not be turned into spaces.
                tokens.extend([' '])
                continue

            wordlist = process_word(word)
            tokens.extend(wordlist)
            if wordlist[-1] != '\n':
                tokens.extend(list(' '))
            
    f.close()
    return tokens

'''
Converts a binary codestring into a bytearray.
This function is called by huffman_encode, which is called
by write_file_output.
'''
def binarystring_to_bytearray(codestring):
    return int(codestring, 2).to_bytes(len(codestring) // 8, byteorder = 'big')

'''
This function takes a codestring, adds extra 0 bits if the length of codestring is not divisble by 8,
then converts the codestring into a string of byte characters. The returned string includes the # extra bits
followed by the encoded string on the next line.
This function is called by write_file_output.
'''



def huffman_encode(codestring):
    # Find the number of extra 0 bits to add if codestring length is not a multiple of 8.
    extrabits = 8 - (len(codestring) % 8)
    global number
    number = extrabits
    
    extras = ''
    # Add 0s in the end.
    for i in range(extrabits):
        extras = extras + '0'
    codestring = codestring + extras
    

    # Encode the codestring 
    encode_bytearray = binarystring_to_bytearray(codestring)
    return encode_bytearray

'''
Takes the filename (without the .enc extension, the treestring which is the
    encoding of the Huffman tree, and codestring which is the binary string
    encoding of the text. This function converts the codestring into a byte array
    and writes everything into the output file. The output file is a byte file.
'''
def write_file_output(filename, treestring, codestring):
    encodestring = huffman_encode(codestring)
    treestring = treestring.encode('utf-8')
    # x = treestring.decode('utf-8')
    
    g = open(filename + ".enc", 'wb')
    g.write(treestring)
    g.write(encodestring)
    g.close()

# You can put your Huffman encoding algorithm here.

class Node:
    def __init__(self, token, freq):
        self.token = token
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(tokens):
    # calculate freq
    freq = {}
    for token in tokens:
        if token not in freq:
            freq[token] = 0
        freq[token] += 1

    priority_queue = [Node(token, freq) for token, freq in freq.items()]
    heapq.heapify(priority_queue)

    # combine nodes
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    return priority_queue[0] 

def generate_code_map(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node.token is not None:
        code_map[node.token] = prefix
    else:
        if node.left is not None:
            generate_code_map(node.left, prefix + "0", code_map)
        if node.right is not None:
            generate_code_map(node.right, prefix + "1", code_map)
    return code_map

def encode_input(tokens, code_map):
    encoded_string = ''
    for token in tokens:
        if token in code_map:
            encoded_string += code_map[token]
    return encoded_string

internal_counter = 1
special_symbols = {'\r': '˜1', ' ': '˜2', '\t': '˜3', '\n': '˜4'}

def encode_huffman_tree(node):
    global internal_counter
    if node is None:
        return ""
    
    # leaf
    if node.left is None and node.right is None:
        if node.token in special_symbols:
            return special_symbols[node.token]
        return node.token
    
    # internal
    left_encoding = encode_huffman_tree(node.left)
    right_encoding = encode_huffman_tree(node.right)
    current_label = f"#{internal_counter}"
    internal_counter += 1 
    
    return f"{current_label} {left_encoding} {right_encoding}"


def format_enc_tree(enc_tree_list, n):
    encoded_tree = enc_tree_list.pop(0).replace("#", "") + "\n"
    while len(enc_tree_list) >= 2:
        encoded_tree += f"{enc_tree_list.pop(0)} {enc_tree_list.pop(0)}\n"
    
    if len(enc_tree_list) != 0:
        encoded_tree += f"{enc_tree_list.pop(0)}\n"
    return encoded_tree + f"{n}\n"

if __name__ == "__main__":

    tokens = get_tokens(sys.argv[1])
    tree = build_huffman_tree(tokens)

    code_map = generate_code_map(tree)
    code_string = encode_input(tokens, code_map)

    encoded_tree = encode_huffman_tree(tree)
    fixed_enc_tree = encoded_tree.split()
    huffman_encode(code_string)
    padding = str(number)
    tree_string = format_enc_tree(fixed_enc_tree, padding)

    # not working :(
    write_file_output(sys.argv[1], tree_string, code_string)

    print(tree_string + code_string)
