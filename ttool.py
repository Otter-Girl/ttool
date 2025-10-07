from translate import Translator
from tabulate import tabulate
translator = Translator(to_lang="en", from_lang="ja")


def ttool(translation_ja):
    #~~~
    #Main function.
    #~~~
        #Reformat text
    japanese_collum = splitter(translation_ja)
        #Translate the input
    english_collum = []
    for i in range(len(japanese_collum)):
        english_collum.append(translator.translate(japanese_collum[i]))
    #
        #Zipper both texts into a table.
    print(tabulate({"Japanease":japanese_collum, "English":english_collum}, tablefmt="simple"))


def splitter(input):
    #~~~
    #This function removes new lines and makes a list of individual text boxes. The list lets us easily make a table.
    #~~~
    inputsectioned = input.split(sep="\n\n\n")
    inputlisted = []
    for i in range(len(inputsectioned)):
        section = inputsectioned[i].split(sep="\n\n")
        for j in range(len(section)):
            block = section[j]
            if len(block) > 499:
                block = blocktoolong(block)
                for k in range(len(block)):
                    inputlisted.append(block[k])
                continue
            inputlisted.append(block)
    return inputlisted

def blocktoolong(block, index = 0):
    temp = []
    indexold = index
    while index != -1:
        indexold = index
        index = block.find('\n', index + 450)
        temp.append(block[indexold:index])
    return temp

if __name__ == '__main__':
    #~~~
    #We will mainly be running this file from the command line so we like to do grunt work here.
    #If you want to use ttool as a module you can input raw strings only.
    #~~~

        #Get file and contents
    filepath = input("Input file path.\n")          #Str Variable
    file = open(filepath, "r", encoding="utf-8")    #File Variable
    filecontents = file.read()                      #Str Variable
        #Start main function
    ttool(filecontents)