from cmgben import cmgben


def tohex(text, encoding=cmgben):
    # Main function
    text = prep(text)
    engtext = stripper(text)
    hextext = encoder(engtext, encoding)
    text = glossmaker(hextext, engtext)
    print(text)


def prep(text):
    # This encoding and decoding removes all non-Latin and special characters.
    text = text.encode("ascii", errors="ignore")
    return text.decode("ascii")


def stripper(text):
    # Splitting lines as a lot of \n is used during translation to keep things visually clear.
    text = text.splitlines()
    intertext = []
    strippedtext = []
    # Strip away the remnants of Japanese text
    for line in text:
        intertext.append(line.lstrip(" .!?-1234567890MC\t"))
    # The '*' was inputted manually as a control for this code, it means "stop stripping here" since there are '!'s and
    # '?'s we want to preserve.
    for line in intertext:
        strippedtext.append(line.lstrip("*"))
    return strippedtext


def encoder(text, encoding=cmgben):
    intertext = []
    for line in text:
        if line == '':
            intertext.append("FF ")
        else:
            intertext.append(line.strip().translate(encoding) + "FE ")
    intertext.append("FF ")
    hextext = cleanup("".join(intertext))
    return hextext


def cleanup(text):
    # ~~~
    # This function replaces certain character strings with equivalent tiles from the tileset that result in
    # less memory use overall. And example is instead of using three periods for an ellipsis, instead there is a single
    # tile that serves as an ellipsis, saving two bytes of hex in memory.
    # ~~~
    #
    # To-do:
    # Apostrophes, quotation marks (maybe just use apostrophes), combo tiles, any other things yet unknown

    # text = text.replace("FE FF", "FF")  # Don't think we need this, but just in case.
    text = text.replace("94 94 94", "8A")  # "..." : "8A "
    return text.rstrip()


def glossmaker(hextext, engtext):
    glossary = '\n\n'
    indecies = {'line': 0, 'hexadecimal': 0, 'english': -2}
    for textboxes in range(hextext.count("FF ")):
        try:
            indecies['line'] = indecies['hexadecimal']
            indecies['hexadecimal'] = hextext.find('FF ', indecies['hexadecimal'] + 1)
            indecies['english'] = engtext.index('', indecies['english'] + 1) + 1
        except ValueError:
            indecies['english'] = -1
        toolong = islinetoolong(hextext, indecies)
        address = str(hex(int(indecies['hexadecimal'] / 3))).lstrip('0x')
        entry = str(engtext[indecies['english']]).rstrip()
        glossary = ''.join([glossary, address, ': ', entry, toolong, '\n'])
    hextext += glossary
    return hextext


def islinetoolong(hextext, indecies):
    line = indecies['line']
    linetoolong = ''
    while line + 3 < indecies['hexadecimal']:
        if hextext.find('FE ', line) - line > 54 and hextext.find('FF ', line) - line > 3:
            linetoolong = ' *!*'
        line = hextext.find('FE ', line + 1)
    return linetoolong


if __name__ == '__main__':
    # ~~~
    # We will mainly be running this file from the command line, so we like to do grunt work here.
    # If you want to use this converter as a module you can input raw strings only.
    # ~~~

    # Get file and contents
    filepath = input("Input file path.\n")  # Str Variable
    file = open(filepath, "r", encoding="utf-8")  # File Variable
    filecontents = file.read()  # Str Variable
    # Start main function
    tohex(filecontents)
