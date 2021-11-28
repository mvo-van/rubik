# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utile.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mvo-van- <mvo-van-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/11/13 12:05:37 by mvo-van-          #+#    #+#              #
#    Updated: 2021/11/28 13:53:26 by mvo-van-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random
import re

def melangeGenerat(nb):
    nb = int(nb)
    mel = ""
    lstMouv = ["B","U","F","L","R","D","B'","U'","F'","L'","R'","D'","B2","U2","F2","L2","R2","D2"]
    save = ""
    while nb > 0:
        mouv = random.choice(lstMouv)
        if mouv[0] != save:
            save = mouv[0]
            mel += mouv + " "
            nb -=1
    return mel

def findpos(wher,search,rubik):
    if wher in ["cross","mid","groupCross","groupMid"]:
        return str(rubik.cube[wher].index(search))
    if wher == "colorMid":
        string = ""
        for index in range(search,search+4):
            if rubik.cube["mid"][index] >= search and rubik.cube["mid"][index] < search+4:
                string += "1"
            else:
                string += "0"
        return string

def cleanMouvement(listMouvement):
    mouvs = []
    for lastMouv in listMouvement :
        if len(mouvs) > 0:
            if mouvs[-1][0] == lastMouv[0]:
                if mouvs[-1][-1] == lastMouv[-1] and mouvs[-1][-1] != "2":
                    mouvs[-1] = "{}2".format(mouvs[-1][0])
                elif mouvs[-1][-1] == lastMouv[-1]:
                    del(mouvs[-1])
                elif mouvs[-1][-1] == "2" or lastMouv[-1] == "2":
                    if mouvs[-1][-1] == "'" or lastMouv[-1] == "'":
                        mouvs[-1] = mouvs[-1][0]
                    else:
                        mouvs[-1] = "{}'".format(mouvs[-1][0])
                else:
                    del(mouvs[-1])
            else:
                mouvs += [lastMouv]
        else:
            mouvs += [lastMouv]
    return mouvs

def creeMelange(arg):
    if re.match(r"^((([ \t]*[BUFDLR][\'2]?[ \t]*)*)|(-g[0-9]+)){1}$",arg):
        if re.search("^(-g[0-9]+)$",arg):
            arg = melangeGenerat(arg[2:])
            print(arg+"\n")
        arg=re.sub(" $","",re.sub(r"([BUFDLR][\'2]?)",r"\1 ",re.sub("[\t ]","",arg)))
        arg=re.split(" ",arg)
        return(arg)
    return None