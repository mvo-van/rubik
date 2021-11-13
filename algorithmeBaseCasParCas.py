import re
import sys
import json

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
                #print(key+" "+str(part))
                for block in part:
                    #print(key+" "+str(block))
                    for index,swap in enumerate(block):
                        save = self.cube[key][swap]
                        if index != 0:
                            self.cube[key][swap] = prev
                        else:
                            first = swap
                        prev = save
                        #print(self.cube)
                        #print(str(save))
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

def verfiCube(cube):
    for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
        if (cube.cube['mid'][i] != -1 and cube.cube['mid'][i] != i) or (cube.cube['cross'][i] != -1 and cube.cube['cross'][i] != i):
            return 0
        if i < 12:
            if (cube.cube['groupMid'][i] != -1 and cube.cube['groupMid'][i] != i):
                return 0
        if i < 8:
            if (cube.cube['groupCross'][i] != -1 and cube.cube['groupCross'][i] != i):
                return 0
    return 1

def findQuickPlaceMid(nbr,lstOkMid,lstOkCross,lstOkgroupCross,lstOkgroupMid):
    arg="RR'"
    arg=re.sub(" $","",re.sub(r"([BUFDLR][\'2]?)",r"\1 ",re.sub("[\t ]","",arg)))
    arg=re.split(" ",arg)
    test = rubik(arg)
    result = {}
    for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
        test.cube['mid'][i] = -1
        test.cube['cross'][i] = -1
        if i < 12:
            test.cube['groupMid'][i] = -1
        if i < 8:
            test.cube['groupCross'][i] = -1    
  
    for i in lstOkMid:
        test.cube['mid'][i] = i
    for i in lstOkCross:
        test.cube['cross'][i] = i
    for i in lstOkgroupMid:
        test.cube['groupMid'][i] = i
    for i in lstOkgroupCross:
        test.cube['groupCross'][i] = i
    
    for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
        if i not in lstOkMid:
            test.cube['mid'][i] = nbr
            #print(test.cube["mid"])
            chemin = findChemin(test,'')
            #print(chemin)
            result[str(i)]=chemin
            test.cube['mid'][i] = -1
    return result

def findQuickPlaceCross(nbr,lstOkMid,lstOkCross,lstOkgroupCross,lstOkgroupMid):
    arg="RR'"
    arg=re.sub(" $","",re.sub(r"([BUFDLR][\'2]?)",r"\1 ",re.sub("[\t ]","",arg)))
    arg=re.split(" ",arg)
    test = rubik(arg)
    result = {}
    for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
        test.cube['mid'][i] = -1
        test.cube['cross'][i] = -1
        if i < 12:
            test.cube['groupMid'][i] = -1
        if i < 8:
            test.cube['groupCross'][i] = -1    
  
    for i in lstOkMid:
        test.cube['mid'][i] = i
    for i in lstOkCross:
        test.cube['cross'][i] = i
    for i in lstOkgroupMid:
        test.cube['groupMid'][i] = i
    for i in lstOkgroupCross:
        test.cube['groupCross'][i] = i
    
    for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
        if i not in lstOkCross:
            test.cube['cross'][i] = nbr
            print(test.cube["cross"])
            chemin = findChemin(test,'')
            print(chemin)
            result[str(i)]=chemin
            test.cube['cross'][i] = -1
    return result
    #print(test.cube['mid'],test.cube['cross'],test.cube['groupMid'],test.cube['groupCross'])

def findChemin(cube,notMouv):    
    # lstMouv="UFBRLD"
    # lstSubMouv="'2"
    # difChemin=[[]]
    # lstMouv=lstMouv.replace(notMouv,'')
    # newDifChemin=[]
    file = open('lstMouv.json','r')
    jsonMouv = json.loads(file.read())
    file.close()
    if verfiCube(cube)==1:
        return []
    #while 1:        
        # newDifChemin=[]
        # for chemin in jsonMouv:
            
        #     #print(chemin)
        #     #lstMouv="UFBRLD"
        #     # if len(chemin) > 0:
        #     #     lstMouv=lstMouv.replace(chemin[-1][0],'')
        #     #newChemin=chemin
        #     for mouv in lstMouv:    
        #         newChemin=chemin.copy()
        #         newChemin += [mouv]
        #         newDifChemin+=[newChemin]
        #         #print(newDifChemin)
        #         for sub in lstSubMouv:
        #             newChemin=chemin.copy()
        #             newChemin += [mouv+sub]
        #             newDifChemin+=[newChemin]
    for chemin in jsonMouv:
        testCube = rubik(["R","R'"])
        testCube.cube['mid']=cube.cube['mid'].copy()
        testCube.cube['cross']=cube.cube['cross'].copy()
        testCube.cube['groupMid']=cube.cube['groupMid'].copy()
        testCube.cube['groupCross']=cube.cube['groupCross'].copy()
        testCube.mix(chemin)
        if verfiCube(testCube):
            return chemin
    return[]
#    difChemin=newDifChemin

file = open('baseCasPK.json','r')
jsonBase = json.loads(file.read())
file.close()


print(jsonBase)
# jsonBase += [{"la grande couronne":[]}]

# jsonBase[0]["la grande couronne"]+=[{"mid":[]}]
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"4":findQuickPlaceMid(4,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('4')
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"5":findQuickPlaceMid(5,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('5')
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"12":findQuickPlaceMid(12,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('12')
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"14":findQuickPlaceMid(14,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('14')
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"15":findQuickPlaceMid(15,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('5')
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"20":findQuickPlaceMid(20,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('20')
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"23":findQuickPlaceMid(23,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('23')

# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"1":findQuickPlaceMid(1,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('1')
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"2":findQuickPlaceMid(2,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('2')
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"17":findQuickPlaceMid(17,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('17')
# jsonBase[0]["la grande couronne"][0]["mid"]+=[{"18":findQuickPlaceMid(18,[8,3,9,6,10,13,11,16],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8],)}]
# print('18')

# jsonBase += [{"la grande couronne 2":[]}]

# jsonBase[1]["la grande couronne 2"]+=[{"mid":[]}]

# jsonBase[1]["la grande couronne 2"][0]["mid"]+=[{"4":findQuickPlaceMid(4,[8,3,9,6,10,13,11,16,7,17],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8,6],)}]
# print("4 finish")
# jsonBase[1]["la grande couronne 2"][0]["mid"]+=[{"12":findQuickPlaceMid(12,[8,3,9,6,10,13,11,16,7,17],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8,6],)}]
# print("12 finish")
# jsonBase[1]["la grande couronne 2"][0]["mid"]+=[{"15":findQuickPlaceMid(15,[8,3,9,6,10,13,11,16,7,17],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8,6],)}]
# print("15 finish")

jsonBase += [{"la grande couronne 3":[]}]

jsonBase[2]["la grande couronne 3"]+=[{"mid":[]}]
jsonBase[2]["la grande couronne 3"][0]["mid"]+=[{"1":findQuickPlaceMid(1,[8,3,9,6,10,13,11,16,7,17,18,15],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8,6,10],)}]
print("1 finish")
jsonBase[2]["la grande couronne 3"][0]["mid"]+=[{"2":findQuickPlaceMid(2,[8,3,9,6,10,13,11,16,7,17,18,15],[8,5,2,9,3,12,10,7,16,11,14,17],[2,7,3,4],[3,5,7,8,6,10],)}]
print("2 finish")


file = open('baseCasPK.json','w')
file.write(json.dumps(jsonBase))
file.close()
#print(json)
#print(findQuickPlaceMid(8,[],[],[],[],))

