import os

addr = '/Users/yibang/Documents/PyCharmWorkspace/cis556/hw1'
filename = 'encriptedText.txt'

def getfile():
    """
    :return: list of all hex strings in the file
    """
    os.chdir(addr)
    content = []
    with open(filename, 'r') as f:
        for line in f:
            # trim the last \n character if exists
            if line[len(line)-1] == '\n':
                content.append(line[:len(line)-1])
            else:
                content.append(line)
    f.close()
    return content

def strxor(a, b):     # xor two strings (trims the longer input)
    """
    :param a: plain text, NOT HEX
    :param b: plain text, NOT HEX
    :return:
    """
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

def decrypt():
    strList = getfile() # list of hex strings
    if len(strList) < 2:
        print "Cannot attack with " + str(len(strList)) + " cipher texts"
        return

    # a list of characters in the key, initiated with all nulls at the beginning
    keyCharList = ['00'] * 200

    # for each given hex string, XOR with other strings
    for i in range(len(strList)):
        txt1 = strList[i].decode('hex') # convert to normal string
        indexCount = {}     # map of how many times each character positions are 'likeyly space'
        indexesOfSpace = set()   #list of indexes on which we have confidence that the text as space

        for j in range(len(strList)):
            if i == j: continue # avoid XOR itself
            txt12xor = strxor(txt1, strList[j].decode('hex'))
            # find indexes where the result is an alphabetic character
            for ind in range(len(txt12xor)):
                if txt12xor[ind].isalpha():
                    if indexCount.has_key(ind):
                        indexCount[ind] += 1
                        if indexCount[ind] > 8:
                            indexesOfSpace.add(ind)
                    else:
                        indexCount[ind] = 0

        # XOR the text with a space text
        xor_with_space = strxor(txt1, ' '*200)
        # Those on the space indexes are decripted characters
        for ind in indexesOfSpace:
            keyCharList[ind] = xor_with_space[ind].encode('hex')

    keyHex = "".join([val for val in keyCharList])

    # manual adjusting by reading through broken texts and adjusting the key
    # text6 = "I mean unbreakable codes."
    # text9 = "Such an approach is purely theoretical. "
    # text11 = "But maybe, just maybe, there's a shortcut."
    # text14 = "...may be able to see things in other numbers that "
    # text0 = "While the number-field sieve is the best method current"
    # text14 = "...may be able to see things in other numbers that we can"
    # text9 = "Such an approach is purely theoretical. So far, no one has "
    # text10 = "The numbers are so unbelievably big, all the computers in the "
    # text11 = "But maybe, just maybe, there's a shortcut. I'll bet you anything "
    # text10 = "The numbers are so unbelievably big, all the computers in the world "
    # text16 = "   Congratulations, you have gotten this far.  But you're not done yet."
    # text2 = "...over the rationals, and hence contained in a single cyclotomic field."
    # text7 = "It would be a breakthrough of Gaussian proportions and allow us to acquire "
    # text0 = "While the number-field sieve is the best method currently known, there exists "
    # text9 = "Such an approach is purely theoretical. So far, no one has been able to accomplish "
    # text7 = "It would be a breakthrough of Gaussian proportions and allow us to acquire the solution "
    # text0 = "While the number-field sieve is the best method currently known, there exists an intriguing "
    # text10 = "The numbers are so unbelievably big, all the computers in the world could not break them down."
    # text9 = "Such an approach is purely theoretical. So far, no one has been able to accomplish such construction"
    # text0 = "While the number-field sieve is the best method currently known, there exists an intriguing possibility "
    # text7 = "It would be a breakthrough of Gaussian proportions and allow us to acquire the solution in a dramatically "
    # text9 = "Such an approach is purely theoretical. So far, no one has been able to accomplish such constructions yet.\n"
    # text0 = "While the number-field sieve is the best method currently known, there exists an intriguing possibility for "
    text2 = "...over the rationals, and hence contained in a single cyclotomic field.  Using the Artin map, we might induce "

    # the following 4 blocks of codes are tries for each guess above consecutively
    keySubstring = strxor(strList[2].decode('hex'), text2)
    for i, char in enumerate(keySubstring):
        keyCharList[i] = char.encode('hex')
    keyHex = "".join([val for val in keyCharList])

    for i in range(len(strList)):
        output = strxor(strList[i].decode("hex"), keyHex.decode("hex"))
        print i, "".join([char if keyCharList[ind] != '00' else '*' for ind, char in enumerate(output)])

decrypt()