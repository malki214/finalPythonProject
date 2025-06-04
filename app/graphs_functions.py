# import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from models import file
from alerts_functions import *

def histogram_functions_lengths(path):
    lengths=get_functions_lengths()
    arr_length=lengths.values()
    plt.hist(arr_length, bins=[0,5,10,15,20,25,30], edgecolor='black')
    plt.title('function lengths')
    plt.xlabel('lengths')
    plt.ylabel('Number of functions')
    plt.savefig(f'{path}/images/histogram_functions_lengths.png')
    plt.close()
    return f'{path}/images/histogram_functions_lengths.png'
    # plt.show()

def number_problems_for_each_problem_type(path):
    counts=[len(check_over_20_lines()),0 if check_file_over_200_lines() is None else 1,
            len(find_unused_variables()),len(find_functions_without_docstrings())]

    # print(counts)
    labels=["functions over 20 lines","file over 200 lines", "unused variables","functions without docstrings"]
    # print(labels)
    plt.pie(counts,labels=labels
            ,autopct="%0.2f%%",explode=[0.05,0,0.05,0.01])
    # plt.show()
    plt.savefig(f'{path}/images/number_problems_for_each_problem_type.png')
    plt.close()
    return f'{path}/images/number_problems_for_each_problem_type.png'


def number_problem_per_file(file):
    lengths=len(check_over_20_lines())+len(find_unused_variables())+len(find_functions_without_docstrings())+(0 if check_file_over_200_lines() is None else 1)
    # print(lengths)
    names_files = [f'{file.name}', 'Category B', 'Category C']
    lens = [lengths, 45, 56]
    plt.bar(names_files, lens)
    plt.title('Bar Graph lengths files')
    plt.xlabel('names')
    plt.ylabel('length')
    plt.savefig(f'{file.path}/images/number_problem_per_file.png')
    plt.close()
    return f'{file.path}/images/number_problem_per_file.png'
    # plt.show()

if __name__=='__main__':
    f = file.File(path=r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app",name="main.py")
    open_file(f)
    img = Image.open(histogram_functions_lengths(r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app"))
    img.show()
    img = Image.open(number_problems_for_each_problem_type(r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app"))
    img.show()
    img = Image.open(number_problem_per_file(f))
    img.show()