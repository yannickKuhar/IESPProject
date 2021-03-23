import nltk
from nltk.corpus import stopwords
from operator import add
import re
from collections import Counter
import operator

"""
Zakomentiraj line 30
"""


def preprocess_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [word for word in text if word not in stopwords.words('english')]
    nonPunct = re.compile('.*[A-Za-z0-9].*')
    text = [w for w in text if nonPunct.match(w)]
    return text


class doc_similarity:
    def __init__(self, jaccard_threshold=0.8):
        self.jaccard_threshold = jaccard_threshold
        self.text_db = {}
        self.hash_tables = {i: {} for i in range(4)}


    def similarity(self, text):
        text = preprocess_text(text)
        hashed_text = self.hash_text(text)
        # self.print_hash(hashed_text)

        occurences = self.in_hash_tables(hashed_text)
        # print(occurences)
        occurences = Counter(occurences)
        occurences = dict(sorted(occurences.items(), key=operator.itemgetter(1), reverse=True))

        if not len(occurences) or occurences[list(occurences.keys())[0]] < 2:
            # Document is not similar to any other document, add it to hash_tables
            self.add_to_hash_tables(hashed_text, text)
            #self.print_text_db()
            return True
        else:
            # More in-depth comparison of the seemingly similar documents
            if self.in_depth_check(text, occurences):
                # Document is not similar to any other document, add it to hash_tables
                self.add_to_hash_tables(hashed_text, text)
                #self.print_text_db()
                return True
            else:
                # Document is too similar to some other document, reject it
                print("Namaste.")
                return False


    def in_depth_check(self, current_text, occurences):
        for x in occurences:
            if occurences[x] > 1:
                ref_text = self.text_db[x]
                # More in-depth comparison
                js = self.jaccard_dist(current_text, ref_text)
                """print("Current: ", current_text)
                print("Reference: ", ref_text)
                print(js)"""
                if js > self.jaccard_threshold:
                    return False
            else:
                break
        return True


    @staticmethod
    def jaccard_dist(t1, t2):
        presek = set(t1) & set(t2)
        unija = set(t1 + t2)

        return len(presek) / len(unija)


    def in_hash_tables(self, hashed_text):
        q0 = hashed_text[0:8]
        q1 = hashed_text[8:16]
        q2 = hashed_text[16:24]
        q3 = hashed_text[24:32]

        similar_txts = []

        for t in self.hash_tables[0].keys():
            if t == q0: similar_txts += list(self.hash_tables[0][t])

        for t in self.hash_tables[1].keys():
            if t == q1: similar_txts += list(self.hash_tables[1][t])

        for t in self.hash_tables[2].keys():
            if t == q2: similar_txts += list(self.hash_tables[2][t])

        for t in self.hash_tables[3].keys():
            if t == q3: similar_txts += list(self.hash_tables[3][t])

        return similar_txts


    def add_to_hash_tables(self, hashed_text, text):
        q0 = hashed_text[0:8]
        q1 = hashed_text[8:16]
        q2 = hashed_text[16:24]
        q3 = hashed_text[24:32]

        if q0 in self.hash_tables[0].keys():
            self.hash_tables[0][q0].append(len(self.text_db))
        else:
            self.hash_tables[0][q0] = [len(self.text_db)]

        if q1 in self.hash_tables[1].keys():
            self.hash_tables[1][q1].append(len(self.text_db))
        else:
            self.hash_tables[1][q1] = [len(self.text_db)]

        if q2 in self.hash_tables[2].keys():
            self.hash_tables[2][q2].append(len(self.text_db))
        else:
            self.hash_tables[2][q2] = [len(self.text_db)]

        if q3 in self.hash_tables[3].keys():
            self.hash_tables[3][q3].append(len(self.text_db))
        else:
            self.hash_tables[3][q3] = [len(self.text_db)]

        self.text_db[len(self.text_db)] = text


    def print_hash_tables(self):
        print("---------------")
        for t in self.hash_tables:
            print(t, self.hash_tables[t])
        print("---------------")


    @staticmethod
    def print_hash(hashed_text):
        print(hashed_text[0:8])
        print(hashed_text[8:16])
        print(hashed_text[16:24])
        print(hashed_text[24:32])


    def print_text_db(self):
        for x in self.text_db:
            print(x, self.text_db[x])


    def hash_text(self, text):
        vec = [0 for _ in range(32)]

        for word in text:
            hashed_word = self.adler32(word)
            hashed_word = [1 if c == '1' else -1 for c in hashed_word]
            vec = list(map(add, vec, hashed_word))

        vec = ''.join(['1' if c > 0 else '0' for c in vec])
        return vec


    def adler32(self, string, prime=65521):
        chars = [char for char in string]
        sumA = 0;
        sumB = 1

        for c in chars:
            sumB += ord(c)
            sumA += sumB

        modA = sumA % prime
        modB = sumB % prime
        binA = format(modA, '#018b')[2:]
        binB = format(modB, '#018b')[2:]
        rez = binA + binB

        return rez


text0 = "Nasus is an imposing, jackal-headed Ascended—those heroic and god-like figures once revered by the people of Shurima. Fiercely intelligent, he was a guardian of knowledge and peerless strategist whose wisdom guided the empire to greatness for many centuries. After the failed Ascension of Azir, Nasus went into self-imposed exile, becoming little more than a legend. Now that the Sun Disc has risen once more, he has returned, determined to ensure it never falls again."
text1 = "Sadistic and cunning, Thresh is an ambitious and restless spirit of the Shadow Isles. Once the custodian of countless arcane secrets, he was undone by a power greater than life or death, and now sustains himself by tormenting and breaking others with slow, excruciating inventiveness. His victims suffer far beyond their brief mortal coil as Thresh wreaks agony upon their souls, imprisoning them in his unholy lantern to torture for all eternity."
text2 = "Tropical fish include fish found in tropical environments around the world, including both freshwater and salt water species."
text3 = "yes yes yes no no hue hue fiawgegvwsfa FWEEEEEEEEEEEEEEA"
text4 = "Nasus is an yes, jackal-headed Ascended—those no and god-like figures once shit by the people of Shurima. Fiercely intelligent, he was a guardian of knowledge and peerless strategist whose wisdom guided the empire to greatness for many centuries. After the failed Ascension of Azir, Nasus went into self-imposed exile, becoming little more than a legend. Now that the Sun xDDDD Disc has risen once more, he has returned, determined to ensure it never falls again."
text5 = "Document Similarity Search (DSS) is to find sim-ilar documents to a query doc in a text corpus oron the web. It is an important component in mod-ern information retrieval since DSS can improve thetraditional search engines and user experience (Wanet al., 2008; Deanet al., 1999). Traditional searchengines accept several terms submitted by a useras a query and return a set of docs that are rele-vant to the query.  However, for those users whoare not search experts, it is always difficult to ac-curately specify some query terms to express theirsearch purposes. Unlike short-query based search,DSS queries by a full (long) document, which allowsusers to directly submit a page or a document to thesearch engines as the description of their informa-tion needs. Meanwhile, the explosion of informationhas brought great challenges to traditional methods.For example, Inverted List (IL) which is a primarykey-term access method would return a very largeset of docs for a query document, which leads to thetime-consuming post-processing. Therefore, a neweffective algorithm is required.Hashing methods can perform highly efficient butapproximate similarity search, and have gained greatsuccess in many applications such as Content-BasedImage Retrieval (CBIR) (Keet al., 2004; Kulisetal., 2009b), near-duplicate data detection (Keetal., 2004; Mankuet al., 2007; Costaet al., 2010),etc. Hashing methods project high-dimensional ob-jects to compact binary codes calledfingerprints andmake similar fingerprints for similar objects. Thesimilarity search in the Hamming space1is muchmore efficient than in the original attribute space(Mankuet al., 2007)."
text6 = "SimHash: Hash-based Similarity DetectionCaitlin SadowskiUniversity of California, Santa Cruzsupertri@cs.ucsc.eduGreg LevinUniversity of California, Santa Cruzglevin@cs.ucsc.eduDecember 13, 20071  AbstractMost hash functions are used to separate and obscuredata,  so  that  similar  data  hashes  to  very  differentkeys.  We propose to use hash functions for the op-posite purpose:  to detect similarities between data.Detecting similar files and classifying documents isa  well-studied  problem,  but  typically  involves  com-plex heuristics and/orO(n2) pair-wise comparisons.Using a hash function that hashed similar files to sim-ilar values, file similarity could be determined simplyby comparing pre-sorted hash key values.  The chal-lenge is to find a similarity hash that minimizes falsepositives.We have implemented a family of similarity hashfunctions with this intent.  We have further enhancedtheir performance by storing the auxiliary data usedto  compute  our  hash  keys.   This  data  is  used  as  asecond  filter  after  a  hash  key  comparison  indicatesthat  two  files  are  potentially  similar.   We  use  thesetests to explore the notion of “similarity.”2  IntroductionAs storage capacities become larger it is increasinglydifficult to organize and manage growing file systems.Identical copies or older versions of files often becomeseparated and scattered across a directory structure.Consolidating or removing multiple versions of a filebecomes desirable.  However, deduplication technolo-gies  do  not  extend  well  to  the  case  where  files  arenot identical.  Techniques for identifying similar filescould also be useful for classification purposes and asan aid to search.  A standard technique in similaritydetection is to map features of a file into some high-dimensional space, and then use distance within thisspace as a measure of similarity.  Unfortunately, thistypically involves computing the distance between allpairs  of  files,  which  leads  toO(n2)  similarity  de-tection  algorithms.   If  these  file-to-vector  mappingscould  be  reduced  to  a  one-dimensional  space,  thenthe  data  points  could  be  sorted  inO(nlogn)  time,greatly increasing detection speed.Our goal was to create a “similarity hash function.”Typically,  hash  functions  are  designed  to  minimizecollisions (where two different inputs map to the samekey value).  With cryptographic hash functions, colli-sions should be nearly impossible, and nearly identi-cal data should hash to very different keys.  Our sim-ilarity  hash  function  had  the  opposite  intent:  verysimilar files should map to very similar, or even thesame,  hash  key,  and  distance  between  keys  shouldbe some measure of the difference between files.  Ofcourse,  “file size” is a sort of hash function on fileswhich  satisfies  these  requirements.   However,  whilesimilar files are expected to have similar sizes, thereis no expectation that two files which are close in sizehave  similar  content.   It  is  not  at  all  clear  how  tocondense information from a file into a more usefulone-dimensional key.While SimHash does produce integer-valued hashkeys,  we  ended  up  relying  on  auxiliary  data  to  re-fine  our  similarity  tests.   Our  key  values  are  basedon counting the occurrences of certain binary stringswithin  a  file,  and  combining  these  sums.   Unfo"
text7 = "He was born to mother and father. He was a monk know as Xyz."
text8 = "He was born to father and mother. He were an priest know as Xyz."

if __name__ == '__main__':
    ds = doc_similarity()
    ds.similarity(text0)
    ds.similarity(text1)
    ds.similarity(text2)
    ds.similarity(text3)
    ds.similarity(text4)
    ds.similarity(text5)
    ds.similarity(text6)
    ds.similarity(text7)
    ds.similarity(text8)



















































