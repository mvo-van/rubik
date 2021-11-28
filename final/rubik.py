# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    rubik.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mvo-van- <mvo-van-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/11/13 12:05:25 by mvo-van-          #+#    #+#              #
#    Updated: 2021/11/28 13:59:54 by mvo-van-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import json
from bibli import *
from utile import findpos, cleanMouvement, creeMelange

def readTag(liste):
    tags = 0
    for tag in liste[2:]:
        if re.search("^-([thv]|m[0-2])$",tag):
            tags |= dictTag["TAG"+tag[-1]]
        else:
            return None
    return tags

def startAlgo(tag, arg):
    lstSolution = []
    for algo in ["base","base5338","generale"]:
        cube = rubik(arg)
        lstSolution.append(solution(tag, cube.string()))
        file = open(algo + '.json','r')
        jsonBase = json.loads(file.read())
        file.close()
        parcourBase(lstSolution, cube, jsonBase)                     
    printSolution(lstSolution,tag)

def parcourBase(lstSolution, cube, jsonBase):
    lstMouv = []
    for niveau1 in jsonBase:
        for titre,lstniveau1 in niveau1.items():
            lstSolution[-1].titre.append(titre)
            lstSubMouv  = []
            for niveau2 in lstniveau1:
                for wher,lstniveau2 in niveau2.items():
                    for niveau3 in lstniveau2:
                        for search,lstniveau3 in niveau3.items():
                            lstSubMouv += lstniveau3[findpos(wher,int(search),cube)]
                            lstSolution[-1].piece.append(lstniveau3[findpos(wher,int(search),cube)])
                            lstMouv += lstniveau3[findpos(wher,int(search),cube)]
                            cube.mix(lstniveau3[findpos(wher,int(search),cube)])
                            lstSolution[-1].pieceVue.append(cube.string())
            lstSubMouv  = cleanMouvement(lstSubMouv)
            lstSolution[-1].combinaison.append(lstSubMouv)
            lstSolution[-1].combinaisonVue.append(cube.string())
    lstSolution[-1].mouv = cleanMouvement(lstMouv)

def printSolution(lstSolution, tag):
    if len(lstSolution[0].mouv) < len(lstSolution[1].mouv):
        min = 0
    else:
        min = 1
    if len(lstSolution[min].mouv) > len(lstSolution[2].mouv):
        min = 2
    if tag & dictTag["TAG0"]:
        lstSolution[0].print()
    elif tag & dictTag["TAG1"]:
        lstSolution[1].print()
    elif tag & dictTag["TAG2"]:
        lstSolution[2].print()
    else:
        lstSolution[min].print()

def main():
    if len(sys.argv) > 1:
        arg = creeMelange(sys.argv[1])
        tag = readTag(sys.argv)
        if arg and tag != None:
            startAlgo(tag, arg)
        else:
            print(ERREURARG)
    else:
        print(ERREURARG)

main()
