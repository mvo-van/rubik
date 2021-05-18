import re
import sys

class rubik:

    dico = {"B" : { "cross" : ((0,1,3,2),(4,23,12,8),(5,22,13,9)),
                "mid" : ((0,2,3,1),(4,23,12,8)),
                "groupCross" : [(0,1,7,2)],
                "groupMid" : [(0,2,3,1)]},
        "U" : { "cross" : ((8,9,11,10),(12,17,7,2),(14,16,5,3)),
                "mid" : ((8,10,11,9),(3,13,16,6)),
                "groupCross" : [(3,2,7,4)],
                "groupMid" : [(3,7,8,5)]},
        "F" : { "cross" : ((16,17,19,18),(11,15,20,7),(10,14,21,6)),
                "mid" : ((16,18,19,17),(11,15,20,7)),
                "groupCross" : [(3,4,6,5)],
                "groupMid" : [(8,10,11,6)]},
        "D" : { "cross" : ((20,21,23,22),(18,15,1,4),(19,13,0,6)),
                "mid" : ((20,22,23,21),(19,14,0,5)),
                "groupCross" : [(5,6,1,0)],
                "groupMid" : [(4,11,9,0)]},
        "L" : { "cross" : ((4,5,7,6),(8,16,20,0),(10,18,22,2)),
                "mid" : ((4,6,7,5),(9,17,21,1)),
                "groupCross" : [(0,2,3,5)],
                "groupMid" : [(1,5,6,4)]},
        "R" : { "cross" : ((12,13,15,14),(9,1,21,17),(11,3,23,19)),
                "mid" : ((12,14,15,13),(10,2,22,18)),
                "groupCross" : [(7,1,6,4)],
                "groupMid" : [(2,9,10,7)]}}

    colors={"B":'\033[94m',
        "U":'\033[0m',
        "F":'\033[92m',
        "L":'\033[95m',
        "R":'\033[91m',
        "D":'\033[93m'}
    def __init__(self, mouv):
        self.cube = {"cross" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        "mid" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        "Color" : ['B','B','B','B','L','L','L','L','U','U','U','U','R','R','R','R','F','F','F','F','D','D','D','D'],
        "crossFace" : ['B','B','B','B','L','L','L','L','U','U','U','U','R','R','R','R','F','F','F','F','D','D','D','D'],
        "midFace" : ['B','B','B','B','L','L','L','L','U','U','U','U','R','R','R','R','F','F','F','F','D','D','D','D'],
        "groupCross" : [0,1,2,3,4,5,6,7],
        "groupMid" : [0,1,2,3,4,5,6,7,8,9,10,11]}
        self.mix(mouv)
    
    def mix(self,lstMouv):
        i = 0
        for mouv in lstMouv:
            if '\'' in mouv:
                self.oneMouv(mouv[0],3)
            elif '2' in mouv:
                self.oneMouv(mouv[0],2)
            else:
                self.oneMouv(mouv[0],1)
            i+=1

    def oneMouv(self,mouv,rep):
        mouvToDo = self.dico[mouv]
        while rep > 0:
            for key, part in mouvToDo.items():
                print(key+" "+str(part))
                for block in part:
                    print(key+" "+str(block))
                    for index,swap in enumerate(block):
                        save = self.cube[key][swap]
                        if index != 0:
                            self.cube[key][swap] = prev
                        else:
                            first = swap
                        prev = save
                        #print(self.cube)
                        print(str(save))
                    self.cube[key][first] = prev
            rep -= 1

    def MajFace(self):
        for index, case in enumerate(self.cube["cross"]):
            self.cube["crossFace"][index] = self.cube["Color"][case]
        for index, case in enumerate(self.cube["mid"]):
            self.cube["midFace"][index] = self.cube["Color"][case]

    def print(self):
        string ="      {13} [14] {15}\n      [12] \033[91mR [15]\n      {12} [13] {14}\n{1} [2] {3} {9} [10] {11} {17} [18] {19} {21} [22] {23}\n[0] \033[94mB [3] [8] \033[0mU [11] [16] \033[92mF [19] [20] \033[93mD [23]\n{0} [1] {2} {8} [9] {10} {16} [17] {18} {20} [21] {22}\n      {5} [6] {7}\n      [4] \033[95mL [7]\n      {4} [5] {6}\n"
        self.MajFace()
        for index,cube in enumerate(self.cube["midFace"]):
            reg="\["+str(index)+"\]"
            string = re.sub(reg,self.colors[cube]+cube,string)
        for index,cube in enumerate(self.cube["crossFace"]):
            reg="\{"+str(index)+"\}"
            string = re.sub(reg,self.colors[cube]+cube,string)
        print(string)
        #print("   %c%c%c\n   %cB%c\n   %c%c%c\n%c%c%c%c%c%c%c%c%c\n%cV%c%cR%c%cB%c%cO%c\n%c%c%c%c%c%c%c%c%c\n   %c%c%c\n   %cY%c\n   %c%c%c\n",self.cube["crossFace"])


def main():
    try:
        sys.argv[1]
    except:
        print("pas d'argument")
        return 0

arg="BUFLR'"
if re.search("^([ \t]*[BUFDLR][\'2]?[ \t]*)*$",arg):
    arg=re.sub(" $","",re.sub(r"([BUFDLR][\'2]?)",r"\1 ",re.sub("[\t ]","",arg)))
    arg=re.split(" ",arg)
    test = rubik(arg)
    test.print()
else:
    print("mauvais argument")

#lst = ['B','B2']
#test = rubik(lst)
#test.print()

