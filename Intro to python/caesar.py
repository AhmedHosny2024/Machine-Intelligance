from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    # utils.NotImplemented()
    min_count : int =len(ciphered)
    index : int =0
    original_string : str =""
    splited : list[str]=ciphered.split(" ")

    dictionary : dict = {ele : ele for ele in dictionary}

    for idx in range(26):
        count : int =0
        x : list[str] = [''.join([(chr((ord(w) - 97 - idx) % 26 + 97)) for w in word]) for word in splited]
        x : str = ' '.join(x)
        c : list[int] = [1 for word in x.split(" ") if word not in dictionary]
        count =len(c)
        if(count<min_count):
            index=idx
            min_count=count
    original_string : list[str] = [''.join([(chr((ord(w) - 97 - index) % 26 + 97)) for w in word]) for word in splited]
    original_string : str = ' '.join(original_string)
    return (original_string,index,min_count)


