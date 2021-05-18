import json
def creatChemin():
    lstMouv="UFBRLD"
    lstSubMouv="'2"
    difChemin=[]
    newDifChemin=[]
    saveDifChemin=[[]]
    i=0
    while i<5:        
        newDifChemin=[]
        #print(i)
        for chemin in saveDifChemin:
            
            #print(chemin)
            lstMouv="UFBRLD"
            if len(chemin) > 0:
                lstMouv=lstMouv.replace(chemin[-1][0],'')
            #newChemin=chemin
            for mouv in lstMouv:    
                newChemin=chemin.copy()
                newChemin += [mouv]
                newDifChemin+=[newChemin]
                #print(newDifChemin)
                for sub in lstSubMouv:
                    newChemin=chemin.copy()
                    newChemin += [mouv+sub]
                    newDifChemin+=[newChemin]
        saveDifChemin=newDifChemin.copy()
        difChemin+=newDifChemin.copy()
        i+=1
    #print(difChemin)
    return difChemin


jsonBase=creatChemin()
file = open('lstMouv.json','w')
file.write(json.dumps(jsonBase))
file.close()