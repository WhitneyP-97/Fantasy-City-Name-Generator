#this is supposed to imitate how a human identifies patterns in different languages
#it reads in a file that contains a text in a language, and it will generate fictional words that follow the "rules" of the language
#useful for conlanging, or for writers to create fake city names, character names, etc based on either a real language or a constructed language sample

import re
import random
import statistics

class word:

    def toVector(self):
        v = []
        for i in self.w:
            v.append(i)
        return v

    def distanceVects(self):
        #this measures the distance from each letter in the word to every other letter
        dv = []
        for i in range(len(self.vector)):
            for j in range(len(self.vector)):
                d = []
                if j!=i:
                    d.append(self.vector[i])
                    d.append(self.vector[j])
                    d.append(j-i)
                    dv.append(d)
        return dv

    def allSubstrings(self):
        sub = []
        for i in range(len(self.vector)):
            for j in range(i, len(self.vector)):
                sub.append(self.w[i:j+1])
        return sub

    def startSubs(self):
        x = []
        for i in range(len(self.vector)):
            x.append(self.w[0:i+1])
        return x

    def endSubs(self):
        x = []
        for i in range(len(self.vector)):
            x.append(self.w[i:len(self.vector)])
        return x

    def first(self):
        return self.vector[0]

    def last(self):
        return self.vector[len(self.vector)-1]

    def __init__(self, string):
        self.w = string
        self.vector = self.toVector()
        self.distances = self.distanceVects()
        self.start = self.first()
        self.end = self.last()
        self.sub = self.allSubstrings()
        self.starts = self.startSubs()
        self.ends = self.endSubs()

class fullText:

    def startingChars(self):
        starts = {}
        for i in self.vect:
            if i.start not in starts:
                starts[i.start] = 1
            else:
                starts[i.start] = starts[i.start] + 1
        return starts

    def endingChars(self):
        ends = {}
        for i in self.vect:
            if i.end not in ends:
                ends[i.end] = 1
            else:
                ends[i.end] = ends[i.end] + 1
        return ends

    def startingSubs(self):
        starts = {}
        for i in self.vect:
            for j in i.starts:
                if j not in starts:
                    starts[j] = 1
                else:
                    starts[j] = starts[j] + 1
        return starts

    def endingSubs(self):
        ends = {}
        for i in self.vect:
            for j in i.ends:
                if j not in ends:
                    ends[j] = 1
                else:
                    ends[j] = ends[j] + 1
        return ends


    def distanceVects(self):
        d = []
        for i in self.vect:
            for j in i.distances:
                d.append(j)
        return d

    def substringCounts(self):
        a = {}
        b = []
        for i in self.vect:
            for j in i.sub:
                b.append(j);
        for i in b:
            if i in a:
                a[i] = a[i] + 1
            else:
                a[i] = 1
        return a

##    def pruneRareSubstrings(self,alpha):
##        for i in a:
##            if a[i]/len(self.vect) < alpha:
##                a.pop(i)
##        return

    def pruneRareSubstrings(self,x,alpha):
        #learn what is a rare substring and what is a common substring

        a = 0
        b = statistics.mean(x[i] for i in x)*alpha



        for i in range(1):
            aa = []
            bb = []
            for j in x:
                if abs(x[j] - a) < abs(x[j] - b):
                    aa.append(j)
                else:
                    bb.append(j)
            if len(bb)!=0:
                b = statistics.mean(x[k] for k in bb)
            if len(aa)!=0:
                a = statistics.mean(x[k] for k in aa)
        
        x = {i: x[i] for i in bb}
        
        return x
    
    def averageLength(self):
        a = [len(i.w) for i in self.vect]
        a = statistics.mean(a)
        return a

    def __init__(self, filepath):
        f = open(filepath, 'r', encoding = 'utf-8')
        self.text = f.read()
        self.vect = re.split(r'[ ,.…\n]',self.text)
        for i in range(len(self.vect)):
            self.vect[i] = self.vect[i].lower()
        for i in self.vect:
            if i == '':
                self.vect.remove(i)
        for i in range(len(self.vect)):
            self.vect[i] = word(self.vect[i])
        self.starts = self.startingSubs()
        self.ends = self.endingSubs()
        self.distances = self.distanceVects()
        self.avglen = self.averageLength()
        self.subs = self.substringCounts()
        self.popsubs = self.pruneRareSubstrings(self.subs,2)

def substringCounts(vect):
    a = {}
    b = []
    for i in vect:
        for j in i.sub:
            b.append(j);
    for i in b:
        if i in a:
            a[i] = a[i] + 1
        else:
            a[i] = 1
    return a

def pruneRareSubstrings(x,alpha):
    #learn what is a rare substring and what is a common substring

    a = 0
    b = statistics.mean(x[i] for i in x)*alpha



    for i in range(1):
        aa = []
        bb = []
        for j in x:
            if abs(x[j] - a) < abs(x[j] - b):
                aa.append(j)
            else:
                bb.append(j)
        if len(bb)!=0:
            b = statistics.mean(x[k] for k in bb)
        if len(aa)!=0:
            a = statistics.mean(x[k] for k in aa)
    
    x = {i: x[i] for i in bb}
    
    return x


def generateWord(fulltext):
    w = ''

    def chooseStartingLetter(fulltext):
        a = [i for i in fulltext.starts]
        b = [fulltext.starts[i] for i in fulltext.starts]
        x = random.choices(a,weights=b,k=1)
        y = x[0]

        return y
    
    def chooseNextLetter(fulltext, w, prev, length=4):
        #if length is high, then you will likely get a real word in the language
        #if length is low, you will probably get a fictional word that sounds somewhat like the language
        x = ''
        good = False
        count = 0

        while good==False and count<10:
            a = [i for i in fulltext.vect if prev in i.sub]
            b = substringCounts(a)
            b = {i:b[i] for i in b if i[0] == w[len(w)-1]}
            c = [i for i in b]
            d = [b[i] for i in b]
            x = random.choices(c,weights=d,k=1)
            q = w[0:len(w)-1] + x[0]
            q = word(q)
            good = True
            count = count+1

            for i in q.sub:
                if len(i) <= length:
                    if i not in fulltext.subs:
                        good = False
                        break

        if count == 10:
            return w[len(w)-1]
            
        return x[0]

    def determineIfEnd(fulltext, w, prev, length=4):
        #see above about length
        good = True

        for i in word(w).ends:
            if len(i) <= length:
                if i not in fulltext.ends:
                    good = False
                    break

        if good == True:
            chanceOfEnd = len(w)*0.5/fulltext.avglen
            x = random.random()
            if x < chanceOfEnd:
                return True
            return False

        else:
            return False
            
        
            
    w = chooseStartingLetter(fulltext)
    a = w

    end = determineIfEnd(fulltext, w,a)

    while not end:
        a = chooseNextLetter(fulltext,w,a)
        if a != '':
            w = w[0:len(w)-1]+a
        else:
            end = True
        if end == False:
            end = determineIfEnd(fulltext,w,a)
    return w

def generateWords(text, count):
    ans = ' '
    for i in range(count-1):
        ans = ans + generateWord(text) + ' '
    ans = ans + generateWord(text)
    return ans

fulltext1 = fullText('vietnamese.txt')
fulltext2 = fullText('russian.txt')
fulltext3 = fullText('german.txt')
fulltext4 = fullText('spanish.txt')
fulltext1 = fullText('italian.txt')

print('Generate a fictional Vietnamese city name: ' + generateWords(fulltext1,3) + ' city')
print('Generate a fictional Russian city name: ' + generateWords(fulltext2,2) + ' city')
print('Generate a fictional German city name: ' + generateWords(fulltext3,2) + ' city')
print('Generate a fictional Spanish city name: ' + generateWords(fulltext4,1) + ' city')
print('Generate a fictional Italian city name: ' + generateWords(fulltext5,1) + ' city')
