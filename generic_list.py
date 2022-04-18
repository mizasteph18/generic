# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:01:35 2021

@author: MIZA

@ description : genric list functions
@ version : 1.1 
            
1.0 : filter_from_list
1.1 : transfer list_intersection from generic function to generic list

"""
# =============================================================================
# FILTER_FROM_LIST (list) : filter items from a list acording to a value position
#   
# @ list_to_filter: list of items
# @ value : value to filter from list_to_filter
# @ config (str - contains / startswith / endswith): 3 values possible
# =============================================================================
def filter_from_list(list_to_filter,value,config='contains'):
    
    if config == 'contains':
        result_list = [s for s in list_to_filter if value in s] # contains
    elif config == 'startswith':
        result_list = [s for s in list_to_filter if s.startswith(value)] # startswith
    elif config == 'endswith':
        result_list = [s for s in list_to_filter if s.endswith(value)] # endswith
    elif config == 'out':
        result_list = [s for s in list_to_filter if value not in s] # not in
    else:
        result_list = list_to_filter
    return(result_list)

# value ='obv_ema'
# list_to_filter = some_list
# config ='startswith'

# =============================================================================
# LIST_INTERSECTION : retrieve commom value between 2 list
# =============================================================================
def list_intersection(lst1, lst2, config = 'common'): 
    if config == 'common':
        result = list(set(lst1) & set(lst2))
    elif config == 'diff_1':
        result = list(set(lst1) - set(lst2))
    elif config == 'diff_2':
        result = list(set(lst2) - set(lst1))
    elif config == 'diff_all':
        result = list(set(lst1) - set(lst2))
        result = result + list(set(lst2) - set(lst1))
    return(result)  

# =============================================================================
# FIND_OCCURENCE: return index(s) and count the number of occurenec of a defined value
# @ lst (list): list to analyse
# @ value (variant) value to search
# =============================================================================
def find_occurence(lst, value):
    index = [i for i, x in enumerate(lst) if x == value]
    count = lst.count(value)
    return index, count

# =============================================================================
# UNIQUE : return unqiue value of a list 
# @ lst (list): list to analyse
# =============================================================================
def unique(lst, result_type='list'):
    result = list(dict.fromkeys(lst))
    
    if result_type == 'bool':
        if len(lst) - len(result) == 0:
            result = True
        else:
            result= False
   
    return result
  
# unique([1, 5, 2, 1, 4, 5, 1], result_type='bool')
   
# =============================================================================
# DUPLICATE : identify each duplicate of a list
# =============================================================================
def duplicate(lst, result_type='list'):
 
    visited = set()
    lst = [x for x in lst if x in visited or (visited.add(x) or False)]
    lst = unique(lst)
    
    if result_type == 'bool':
        if len(lst)>0:
            lst = True
        else:
            lst= False
    
    return lst   

# duplicate([1, 5, 2, 1, 4, 5, 1], result_type='bool')

