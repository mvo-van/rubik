# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bibli.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mvo-van- <mvo-van-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/11/13 12:05:47 by mvo-van-          #+#    #+#              #
#    Updated: 2021/11/28 13:58:11 by mvo-van-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re

ERREURARG = """Mauvais argument
       python3 rubik.py [MELANGE] [OPTION]...
        MELANGE : 
            -"^([FRUBLD]['2]? )*$" : melange a effectue
            -g[0-99] : generation d'un melange d'une longeur donnee
        OPTIONS :
            -v visualisation de chaque coup effectue sur le rubik's cube
            -h visualisation par sous-etapes
            -m[0-2] choix de l'algorithme de resolution
                    0 : algo debutant
                    1 : algo 8355
                    2 : algo general
            -t total mouvements
        EXEMPLES :  python3 rubik.py "F R U B L D"
                    python3 rubik.py "F R U B L D" -v -m1
                    python3 rubik.py -g65 -h -v"""

dictTag = {"TAGv" : 1 << 0, "TAGh" : 1 << 1, "TAG0" : 1 << 2, "TAG1" : 1 << 3, "TAG2" : 1 << 4, "TAGt" : 1 << 5}

class solution:
    def __init__(self, tags, start):
        self.start = start
        self.tags = tags
        self.titre = []
        self.combinaison = []
        self.combinaisonVue = []
        self.piece = []
        self.pieceVue = []
        self.mouv = []

    def print(self):
        if self.tags & dictTag["TAGv"]:
            print("VUE PAR MOUVEMENT DE PIECE :\n")
            print(self.start)
            for index, value in enumerate(self.piece):
                if len(value) > 0:
                    listmouvement = ""
                    print("mouvement :")
                    for mouvement in value:
                        listmouvement += mouvement + " "
                    print(listmouvement)
                    print(self.pieceVue[index])
        if self.tags & dictTag["TAGh"]:
            print("VUE PAR COMBINAISON DE MOUVEMENTS :\n")
            print(self.start)
            for index, titreGroup in enumerate(self.titre):
                if len(self.combinaison[index]) > 0:
                    listmouvements = ""
                    for mouvement in self.combinaison[index]:
                        listmouvements += mouvement + " "
                    print(titreGroup)
                    print("combinaison : ", listmouvements)
                    print(self.combinaisonVue[index])
        listmouvements = ""
        for mouvement in self.mouv:
            listmouvements += mouvement + " "
        print(listmouvements)
        if self.tags & dictTag["TAGt"]:
            print("total mouvement : ", len(self.mouv))


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
            if mouv == "":
                return
            elif '\'' in mouv:
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
                for block in part:
                    for index,swap in enumerate(block):
                        save = self.cube[key][swap]
                        if index != 0:
                            self.cube[key][swap] = prev
                        else:
                            first = swap
                        prev = save
                    self.cube[key][first] = prev
            rep -= 1

    def MajFace(self):
        for index, case in enumerate(self.cube["cross"]):
            self.cube["crossFace"][index] = self.cube["Color"][case]
        for index, case in enumerate(self.cube["mid"]):
            self.cube["midFace"][index] = self.cube["Color"][case]

    def string(self):
        string ="      {13} [14] {15}\n      [12] \033[91mR [15]\n      {12} [13] {14}\n{1} [2] {3} {9} [10] {11} {17} [18] {19} {21} [22] {23}\n[0] \033[94mB [3] [8] \033[0mU [11] [16] \033[92mF [19] [20] \033[93mD [23]\n{0} [1] {2} {8} [9] {10} {16} [17] {18} {20} [21] {22}\n      {5} [6] {7}\n      [4] \033[95mL [7]\n      {4} [5] {6}\n"
        self.MajFace()
        for index,cube in enumerate(self.cube["midFace"]):
            reg="\\["+str(index)+"\\]"
            string = re.sub(reg,self.colors[cube]+cube,string)
        for index,cube in enumerate(self.cube["crossFace"]):
            reg="\\{"+str(index)+"\\}"
            string = re.sub(reg,self.colors[cube]+cube,string)
        return string

    def print(self):
        string ="      {13} [14] {15}\n      [12] \033[91mR [15]\n      {12} [13] {14}\n{1} [2] {3} {9} [10] {11} {17} [18] {19} {21} [22] {23}\n[0] \033[94mB [3] [8] \033[0mU [11] [16] \033[92mF [19] [20] \033[93mD [23]\n{0} [1] {2} {8} [9] {10} {16} [17] {18} {20} [21] {22}\n      {5} [6] {7}\n      [4] \033[95mL [7]\n      {4} [5] {6}\n"
        self.MajFace()
        for index,cube in enumerate(self.cube["midFace"]):
            reg="\\["+str(index)+"\\]"
            string = re.sub(reg,self.colors[cube]+cube,string)
        for index,cube in enumerate(self.cube["crossFace"]):
            reg="\\{"+str(index)+"\\}"
            string = re.sub(reg,self.colors[cube]+cube,string)
        print(string)