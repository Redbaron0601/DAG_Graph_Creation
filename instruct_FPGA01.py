'''
    We analyze the calc patterns and write them into data-structure
    Form a DAG graph as description of logic-pattern among formulas
'''

import os
import re
import numpy as np
# For illustration, instance listed as follow
'''
First replace all ' ' as ''
testpat = '1.Youtput=(A1+B1)*C1+(D1+E1)*F1'
testpat01 = '2.Y22=A23/B11*C90+D76/E44*F5'
emp_test = '(.+?)\\.(.+?)\\=\\((.+?)\\+(.+?)\)\\*(.+?)\\+\\((.+?)\\+(.+?)\\)\\*(.*)'
emp_test01 = '(.+?)\\.(.+?)\\=(.+?)/(.+?)\\*(.+?)\\+(.+?)/(.+?)\\*(.*)'

suanshi01_pat = re.compile(emp_test, re.VERBOSE)
suanshi02_pat = re.compile(emp_test01, re.VERBOSE)
result1 = re.findall(suanshi01_pat, testpat)
result2 = re.findall(suanshi02_pat, testpat)
result3 = re.findall(suanshi02_pat, testpat01)
print(result1)
print(result2)
print(result3)

'''
#============================================================================

# Functional Coding
# First prepare variable set


def get_formula_details(path, regulations):
#'''

#'''
    if os.path.isfile(path):
        working_space = open(path, mode='r')
        calc_Formulas = working_space.readlines()
        dimension = len(calc_Formulas)
    elif os._isdir(path):
        print("We need pecise path to the txt file, please recheck!")
    else:
        raise NameError
    formula_Details = dict()
    pattern_found = dict()
    output_v = dict()
    input_v = dict()
    for formula in calc_Formulas:
        for pattern in regulations.keys():
            pat_found, variable = checkFunc(formula, pattern)
            if pat_found is not None:
                pattern_found.setdefault(variable[0], regulations.get(pattern))# Later we will use another map to calc time
                formula_Details[variable[0]] = {variable[1]: variable[2:]}
                if variable[1] in output_v.keys():
                   #if type(output_v[variable[1]]) == 'str':
                    output_v[variable[1]].join('+' + variable[0])
                else:
                    output_v.setdefault(variable[1], variable[0])
                for item in variable[2:]:
                    if item in input_v.keys():
                        #if type(put_v[variable[1]]) == 'str':
                        input_v[item].join('+' + variable[0])
                    else:
                        input_v.setdefault(item, variable[0])
            else:
                continue
    for key in output_v.keys():
        output_v[key] = output_v[key].split('+')
    for key in input_v.keys():
        input_v[key] = input_v[key].split('+')
    return pattern_found, output_v, input_v, formula_Details, dimension


def checkFunc(formula, pattern):
#'''
#
#'''
    result = re.findall(pattern, formula)
    try:
        tmp_result = list(result[0])# If lose, you will trigger an IndexError
#        if tmp_result is None:
#            flag = 0
#            return flag, None
#        else:
        for item in tmp_result:
            if item is None:
                print("Incomplete match should be dropped")
                pat = None
                continue
            else:
                pat = pattern
    except IndexError:
        print('Unsuccessful match, continue finding')
        pat = None
        tmp_result = None
    return pat, tmp_result#@type=tuple


def set_Generate(output_dict, input_dict):
    set_output = set(output_dict.keys())
    set_input = set(input_dict.keys())
    multi_use_variable = set_output & set_input
    single_way_output = set_output - multi_use_variable
    return multi_use_variable, single_way_output


#multi_v, single_v = set_Generate(output_dict, input_dict)


def build_DAG(parent_formula, output_dict, input_dict, formula_details, multi_v):
#'''
#   The output_dict you put in should be a deep copy of the origin output_v
#'''
    current_formula_id = output_dict[parent_formula]
    DAG_Graph = dict()
    DAG = []
    while(len(current_formula_id) >= 2):
#   Finish the iter sequence of one same variable
        current_formula_id = current_formula_id.sort()
        cur_Arrange = current_formula_id[-1]
        del output_dict[parent_formula].sort()[-1]
        current_variable = formula_details[cur_Arrange].values()
#       iter_parent_formula = formula_details[cur_Arrange].keys()
        for each_v in current_variable:
            if each_v in multi_v:
                DAG_iter = build_DAG(each_v, output_dict, input_dict, formula_details, multi_v)
                DAG.append(DAG_iter[cur_Arrange])
                print('Keep printing the picture')
            else:
                print('No more constraints for now')
        if DAG == []:
            DAG = [0]
    if len(current_formula_id) == 1:
        cur_Arrange = current_formula_id
        current_variable = formula_details[cur_Arrange].values()
        for each_v in current_variable:
            if each_v in multi_v:
                DAG_iter = build_DAG(each_v, output_dict, input_dict, formula_details, multi_v)
                DAG.append(DAG_iter[cur_Arrange])
                print('Keep printing the picture')
            else:
                print('No more constraints for now')
        if DAG == []:
            DAG = [0]
    else:
        print('There may have fatal errors in the dict of parent_formula, please check carefully')
        exit(42)
    DAG_Graph[cur_Arrange] = DAG
    return DAG_Graph
