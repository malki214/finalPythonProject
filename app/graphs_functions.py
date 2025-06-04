import matplotlib.pyplot as plt
from PIL import Image
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
    counts=[len(check_over_20_lines()),len(check_file_over_200_lines()),
            len(find_unused_variables()),len(find_functions_without_docstrings())]

    print(counts)
    labels=["functions over 20 lines","file over 200 lines", "unused variables","functions without docstrings"]
    print(labels)
    plt.pie(counts,labels=labels
            ,autopct="%0.2f%%",explode=[0.05,0,0.05,0.01])
    # plt.show()
    plt.title("number problems for each problem type")
    plt.savefig(f'{path}/images/number_problems_for_each_problem_type.png')
    plt.close()
    return f'{path}/images/number_problems_for_each_problem_type.png'


def number_problem_per_file(path):
    init_count_warn_per_file()
    check_file_over_200_lines()
    check_over_20_lines()
    find_unused_variables()
    find_functions_without_docstrings()
    count_warn_per_file = get_count_warn_per_file()
    lengths=[value for value in count_warn_per_file.values()]
    # print(lengths)
    names_files = [key for key in count_warn_per_file.keys()]
    plt.bar(names_files, lengths)
    plt.title('number problem per file')
    plt.xlabel('file name')
    plt.ylabel('number problems')
    plt.savefig(f'{path}/images/number_problem_per_file.png')
    plt.close()
    return f'{path}/images/number_problem_per_file.png'
    # plt.show()

if __name__=='__main__':
    # f = file.File(path=r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app",name="main.py")
    open_directory(r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app")
    img = Image.open(histogram_functions_lengths(r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app"))
    img.show()
    img = Image.open(number_problems_for_each_problem_type(r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app"))
    img.show()
    img = Image.open(number_problem_per_file(r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app"))
    img.show()