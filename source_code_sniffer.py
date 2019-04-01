# encoding: utf-8
import glob
import os
import re

regex_method = r'(public|private|protected).*(static|void|\w*)(.*\(.*\).*)({$)'
regex_class = r'(^.*class.*{?)'
score = []
line_methods_max = 50
line_class_max = 100

path = os.getcwd() + '/Dataset'


def start_sniffer(fname):
    count = _sdata()['data']
    lines = file_to_array(fname)
    count["lines"] = len(lines)
    is_class = False
    is_method = False
    for l in lines:
        if contains_regex(regex_class, l):
            count["class"] += 1
            is_class = True
            is_method = False
        if contains_regex(regex_method, l):
            count["methods"] += 1
            is_method = True
            is_class = False
        if is_class:
            count['qtd bad lines class'] += 1
        if is_method:
            count['qtd bad lines methods'] += 1
        print(l)
    if count['qtd bad lines class'] >= line_class_max:
        count['qtd bad smells found'] += 1
    if count['qtd bad lines methods'] >= line_methods_max:
        count['qtd bad smells found'] += 1
    return count


def file_to_array(fname):
    f = open(fname, "r")
    lines = list(line for line in f)
    f.close()
    return lines


def contains_regex(regex, line):
    found = re.search(regex, line)
    if found:
        return True
    return False


def print_console_format(name):
    print("****************************** %s ******************************" % name.upper())


def print_console_result(name, size):
    print '{0:10} ==============>>> {1:10d}'.format(name.title(), size)


def input_params_from_god():
    try:
        global line_methods_max
        global line_class_max
        line_methods_max = int(raw_input('Insira o número de linhas de código para um metódo ser considerado "deus":'))
        line_class_max = int(raw_input('Insira o número de linhas de código para uma clase ser considerado "deus":'))
    except ValueError:
        print("Você digitou um valor que não é numero!")


def _sdata():
    return {"path": "", 'data': {"lines": 0, "class": 0, "methods": 0, 'qtd bad smells found': 0, 'qtd bad lines class': 0, 'qtd bad lines methods': 0}}


def run():
    # input_params_from_god()
    list_filenames = []
    list_dirpaths = []
    list_dirnames = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        list_filenames.extend(filenames)
        list_dirnames.extend(dirnames)
        list_dirpaths.extend(dirpath)
        if filenames:
            sdata = _sdata()
            sdata['path'] = dirpath
            for filename in glob.glob(os.path.join(dirpath, '*.java')):
                print_console_format("ANALISE DO ARQUIVO")
                print "Diretorio >>", filename, "<<\n\n"
                count = start_sniffer(filename)
                print_console_format("resultado")
                for name, size in count.items():
                    print_console_result(name, size)
                    sdata['data'][name] += size
                print_console_format("+++++++++")
                print "\n\n"
            score.append(sdata)

    print_console_format("resultado final")
    for i in score:
        for name, size in i:
            print_console_result('Total of %s' % name, size)
    print_console_result('Max lines methods', line_methods_max)
    print_console_result('Max lines class', line_class_max)
    print_console_format("+++++++++++++++")


run()
