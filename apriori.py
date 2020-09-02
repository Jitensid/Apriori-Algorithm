import numpy as np
import pandas as pd 
from itertools import combinations 
from collections import OrderedDict 

def fetch_dataset(filename):
    
    dataset = pd.read_excel(filename)
    
    return dataset


def list_to_dict(input_list):
    
    output_dict = dict()
    
    for x in input_list:
        
        if x not in output_dict:
            output_dict[x] = 1
        
        else:
            output_dict[x] += 1
    
    output_dict = OrderedDict(sorted(output_dict.items())) 
    
    return output_dict



def keep_required_elements(input_dict,min_support):
        
    output_dict = {}    
    
    for key in input_dict.keys() :
        
        if input_dict[key] >= min_support:
            
            output_dict[key] =  input_dict[key]
            
    return output_dict



def combination_list(dataset, k):

    y = list()

    for i in range(len(dataset)):

        x = combinations(dataset["items"][i].split(","),k)

        y = y + [','.join(i) for i in x]
        
    return list_to_dict(y)


def create_final_itemset_table(dataset):

    k = 1

    store_combinations = dict()

    final_itemset_table = None

    while k :

        res_dict = keep_required_elements(combination_list(dataset, k), min_support)

        store_combinations[k] = res_dict.copy()

        if(len(res_dict) == 0):
            break

        k += 1
        
    return k, store_combinations


def generate_rules(k, store_combinations):

    rules_dict = dict()
    
    for data in list(store_combinations[k-1].keys()):

        for i in range(1,k-1):

            original_start = data

            start = original_start.split(",")

            total = len(start)

            x = combinations(start,i)

            y = [','.join(i) for i in x]

            z = [sorted(list(set(start) - set(i.split(",")))) for i in y]

            for i,j in zip(y,z):

                temp = ','.join(j)

                value = store_combinations[total].get(original_start) / store_combinations[len(j)].get(temp)
                
                rules_dict[(temp,i)] = value * 100
                            
    return rules_dict


def print_all_rules(rules_dict):
    
    for key in rules_dict.keys():
        
        a,b = key
        
        print(a," ==> ",b," == ",str(rules_dict[key]))


def print_final_rules(rules_dict,min_confidence_percent):
    print("")
    print("Association Rules for the Itemset are as follows :")
    print("")
    for key in rules_dict.keys():
        
        if rules_dict[key] >= min_confidence_percent:
            
            a,b = key
            
            print(a," ====> ",b, " == ",str(rules_dict[key]))


def display_final_itemset(final_itemset):
    
    print("Itemset" ," "," Count")
    
    for key in final_itemset.keys():
        
        print(key, " ",final_itemset[key])

min_support = int(input("Enter Minimum Support : "))

min_confidence_percent = int(input("Enter Minimum Confidence : "))

filename = input("Name of file should be present in the same folder : ")

dataset = fetch_dataset(filename)

dataset.head(10)


k , store_combinations = create_final_itemset_table(dataset)

display_final_itemset(store_combinations[k-1])

rules_dict = generate_rules(k, store_combinations)

print_final_rules(rules_dict, min_confidence_percent)

