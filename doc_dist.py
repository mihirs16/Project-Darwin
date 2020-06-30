import math 
import string 
  
# counts frequency of each word 
# returns a dictionary which maps 
# the words to their frequency. 
def count_frequency(word_list):  
    D = {} 
    for new_word in word_list: 
        if new_word in D: 
            D[new_word] = D[new_word] + 1 
        else:
            D[new_word] = 1
    return D 
  
# returns dictionary of (word, frequency) 
# pairs from the previous dictionary. 
def word_frequencies_for_file(text):  
    word_list = text.split(' ')
    freq_mapping = count_frequency(word_list) 
    return freq_mapping 
  
# returns the dot product of two documents 
def dotProduct(D1, D2):  
    Sum = 0.0    
    for key in D1: 
        if key in D2: 
            Sum += (D1[key] * D2[key]) 
    return Sum
  
# returns the angle in radians  
# between document vectors 
def vector_angle(D1, D2):  
    numerator = dotProduct(D1, D2) 
    denominator = math.sqrt(dotProduct(D1, D1)*dotProduct(D2, D2)) 
    return math.acos(numerator / denominator) 
  
# function for calculating document distance between two text
def documentSimilarity(text1, text2): 
    sorted_word_list_1 = word_frequencies_for_file(text1) 
    sorted_word_list_2 = word_frequencies_for_file(text2) 
    distance = vector_angle(sorted_word_list_1, sorted_word_list_2) 
      
    return distance 
      