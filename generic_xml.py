# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 14:10:09 2022

@author: MIZA
"""
import source.generic_list as my_gl
import os
import pandas
import xml.etree.ElementTree as ET

run_options = {'log_deactivate' : False, # Set to True for test purpose
               'log_dir': '/Log/instruments_{timestamp}.log',
               'env_path' : os.environ['PYTHONPATH'].split(os.pathsep)[0],
               'script': 'instruments'}

directory = run_options['env_path']+'\\test2.xml'
tree = ET.parse('test2.xml')
root = tree.getroot()

# =============================================================================
# 20220417
# =============================================================================

# i = -1
# result_dict = {}
# for item in all_descendants:
#     i += 1
#     print(item.tag)
#     print(all_tags.count(item.tag))
#     if i == 0:
#         result_dict['master'] = pandas.DataFrame()
    


# # step 1: level up the data
# all_descendants = list(root.iter())
# all_tags = [x.tag for x in all_descendants]
# level = 0
# levels = {}
# already_handled = []
# for i in range(0,len(all_descendants)): 
#     # i = 3
#     tag = all_descendants[i].tag
#     index, count = my_gl.find_occurence(all_tags, tag)
#     if tag not in already_handled:
#         already_handled.append(tag)
#         level += 1
#         level_df = pandas.DataFrame()
#         for ident in index:
#             text = all_descendants[ident].text
#             attrib = all_descendants[ident].attrib
#             level_df = level_df.append(layout_attrib(tag, attrib, text,ident),
#                             ignore_index=True)
#         levels['level_' + str(level)] = level_df


# len(all_descendants[0])

# # step 2: analyse data level by level

# levels['data'] = levels['level_1']
# for i in range(2, len(levels)):
#     print(i)
#     i = 6
#     levels['data'] = pandas.merge(levels['data'] ,levels['level_' + str(i)], on=['key'])
#     levels['data'].rename(columns={'index_y': 'index'}, inplace=True)
#     levels['data'] = levels['data'][levels['data']['index'] > levels['data']['index_x']]
#     levels['data'].drop('index_x', inplace=True, axis=1)

# # test 2 - Recursive function

# by_index_df = pandas.DataFrame()
# by_index_dict = {}
# for i in range(0,len(all_descendants)):
#     # tag = all_descendants[i].tag
#     # attrib = all_descendants[i].attrib 
#     # text = all_descendants[i].text
#     count_child = len(list(all_descendants[i]))
#     by_index_df = by_index_df.append({'count_child':count_child},
#                     ignore_index=True)
#     # by_index_dict[i] = layout_attrib(tag, attrib, text)

# for i in by_index_df[by_index_df['count_child']>0].index:
#     i = 0
#     count_child = by_index_df.at[i,'count_child']
#     while count_child > 0:
#         count_child -= 1
#         for element in list(all_descendants[i]):
#             print(element)
#             layout_attrib(element.tag, element.attrib, element.text)
    
        
# def layout_attrib(tag, attrib, text):

#     result_dict = {'key': [1]}
#     result_df = pandas.DataFrame()
#     # handling text
#     if text == '\n\t':
#         result_dict[tag] = [None]
#     else:
#         result_dict[tag] = [text]
    
#     # Handling attribute
#     if len(attrib) > 0:
#         for key, value in attrib.items():
#             result_dict[tag+'_'+key] = [value]
    
#     result_df = pandas.DataFrame(data=result_dict) 
    
#     return(result_df)


# =============================================================================
# test 3
# =============================================================================

def layout_attrib(tag, attrib, text):
    result_dict = {}
    result_df = pandas.DataFrame()

    result_dict['key'] = int(1)
    result_dict[tag] = text
    if len(attrib) > 0:
        for key, value in attrib.items():
            result_dict[tag+'_'+key] = value
    
    result_df = result_df.append(result_dict, ignore_index=True)
    
    return(result_df)



all_descendants = list(root.iter())
by_index_df = pandas.DataFrame()
result_dict = {}
for element in all_descendants:
    count_child = len(list(element))
    by_index_df = by_index_df.append({'element' : element,
                                      'count_child':count_child,
                                      'tag':element.tag,
                                      'attrib':element.attrib,
                                      'text': element.text},
                    ignore_index=True)    
        
result_df = pandas.DataFrame()
for i in by_index_df[by_index_df['count_child']>0].index:
    # i = 11
    master_data = layout_attrib(tag = by_index_df.at[i,'tag'], 
                                attrib = by_index_df.at[i,'attrib'],
                                text = by_index_df.at[i,'text'])
    master_data['prv_index'] = i

    master_element = by_index_df.at[i,'element'] 
    loop_df = by_index_df[(by_index_df['element'].isin(list(master_element))) &
                          (by_index_df['count_child']==0)]
    for j in loop_df.index:
        slave_data = layout_attrib(by_index_df.at[j,'tag'], 
                                           by_index_df.at[j,'attrib'],
                                           by_index_df.at[j,'text'])
        master_data = pandas.merge(master_data, slave_data, on=['key'])
        
    # retrieve child elements
    loop_df = by_index_df[(by_index_df['element'].isin(list(master_element))) &
                          (by_index_df['count_child']>0)].reset_index()
    if len(loop_df)>0:
        loop_df['key'] = 1
        master_data = pandas.merge(master_data, loop_df[['index','key','tag']], on=['key'])
    
    # merge master elements with child
    if by_index_df.at[i,'tag'] not in result_dict.keys():
        result_dict[by_index_df.at[i,'tag']] = master_data
    else:
        result_dict[by_index_df.at[i,'tag']]= pandas.concat([result_dict[by_index_df.at[i,'tag']],
                                                            master_data], 
                                                            ignore_index=True)
    
    

for key, value in result_dict.items():
    col_list = list(result_dict[key].columns)

    col_target = []
    for item in col_list:
        col_target.append(item.replace('_x','').replace('_y',''))
    col_dup = my_gl.duplicate(col_target)
    col_target = my_gl.unique(col_target)
    
    filter_col = [x for x in col_list if x.startswith('neighbor')]

    import numpy
    test = result_dict[key].copy(deep=True)
    test = test.fillna('nc')

    for col in test.columns:
        # print(col)
        # col = 'neighbor_name_x'
        if col.endswith('_x') or col.endswith('_y'):
            print(col)
            target_col = col.replace('_x','').replace('_y','') 
            # if target_col in test.columns:
            #     test.astype({target_col : list})
            test[target_col] = test[target_col].astype(str) + ',' + test[col].astype(str)


def fucn (test, col, target_col):
    if test[col] == 'nc' and test[target_col] == 'nc':
        result = 'nc'
    elif  test[col] == 'nc' and test[target_col] != 'nc':
        result = 'nc'
    elif  test[col] != 'nc' and test[target_col] == 'nc':
        result = test[col]
    else 
        result = result,
    return 
    
numpy.vectorise()


# =============================================================================
# PREVIOUS
# =============================================================================
# # STEP 1: read all available field in root level (level_0)
# result_dict = {tree.getroot().tag : pandas.DataFrame()}
# for level_0 in root:
#     print(level_0.tag, level_0.attrib, level_0.text)
#     level_0.attrib

    
# for neighbor in root.iter('country'):
#      print(neighbor.tag, neighbor.attrib)
     


# a = ET.Element('country')
# for item in a:
#     print(a.tag)
    
    
# all_descendants = list(root.iter())
# process_list = []
# for item in all_descendants:
#     for row in item:
#         print(row, len(row))
#     if item == all_descendants[0]:
#         break

# # handling roots    
# result_dict = {'root':{}}
# sub_elements_list = []
# i = 0
# for item in root:
#     print(item, len(item),len(item.attrib), item.text)
#     result_dict['root'][item.tag]=[item.text]
#     if len(item)>0:
#         result_dict['root'][item.tag] = 'cf ' + item.tag 
#         sub_elements_list.append(item)


# for item in sub_elements_list:
#     print(item.tag)
    
 
# xml_to_process = [x for x in root]
# result_dict = {root.tag:{}}
# level = 0
# while len(xml_to_process)>0:
#     for i in range(len(xml_to_process)-1,-1,-1):
#         tag = xml_to_process[i].tag
#         attrib = xml_to_process[i].attrib
#         text = xml_to_process[i].text
#         print(tag, attrib, text)
#         if len(xml_to_process[i])==0:
#             if level == 0:
#                 result_dict[root.tag][tag]= [text]
#             xml_to_process.pop(i)
#         else:
            
#     level += 1
         

# xml_to_process[0].elements



# # Test 5
# def unique_tag(tag, key_list, range_max=100):
#     if tag in key_list:
#         for i in range(1,100):
#             if tag + '_' + str(i) not in key_list:
#                 result = tag + '_' + str(i) 
#                 break
#     else:
#         result = tag
        
#     return result

# # handling the ones whitout elements and attributes



# def extract_data(xml_to_process):
    
#     result_dict = {}
#     xml_list = []
#     result_dict['level_id'] = [xml_to_process[2]]
#     result_dict['level_df'] = [xml_to_process[0]]
    
#     for element in xml_to_process[1]:
#         tag = element.tag
#         text = element.text
#         attrib = element.attrib
#         print(tag,text,attrib,len(element),len(attrib))
#         if len(element)==0:
#             tag = unique_tag(tag, result_dict.keys(), 100)
#             result_dict[tag] = [text]
#             for key, value in attrib.items():
#                 tag1 = tag + '_' + key
#                 tag1 = unique_tag(tag1, result_dict.keys(), 100)
#                 result_dict[tag1] = [value]
#         else:
#             tag1 = unique_tag(tag1, result_dict.keys(), 100)
#             result_dict[tag1] = ['level_' + str(xml_to_process[2]+1)]
#             xml_list.append((tag,
#                              element,
#                              xml_to_process[2]+1,
#                              'pend'))
    
#     xml_to_process = list(xml_to_process)
#     xml_to_process[3] = 'done'
#     xml_to_process = [tuple(xml_to_process)]
    
#     return result_dict, xml_list, xml_to_process
    
# result_dict = {}
# xml_to_process = (root.tag,root,0,'pend')
# result_dict[xml_to_process[0]], xml_list, xml_to_process = extract_data(xml_to_process)





# # Step 1: list all possible combination
# for element in xml_to_process:
#     print(len(element), element.tag, element.text, element.attrib)
#     if len(element)==0:
#         if len(element.attrib)>0:
#             for key, value in element.attrib.items():
#                 result_dict[element.tag + '_' + key] = ''
#         else:
#             result_dict[element.tag] = element.text 
        
    
#         print(element.tag)
#     else:
#        xml_to_process 



# pandas.DataFrame(result_dict['data'])

   
