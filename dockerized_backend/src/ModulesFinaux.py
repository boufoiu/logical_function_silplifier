import string
from itertools import combinations_with_replacement,permutations,combinations,product
import multiprocessing
import random
from time import perf_counter_ns
from sympy.logic.boolalg import to_dnf , to_cnf
from sympy import sympify 

from sympy.abc import _clash
liste_alphabet = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
from multiprocessing import Process

def user_to_sympy(f):
    f = "".join(f.split(" "))
    f = f.upper()
    f = f.replace("."," & ")
    f = f.replace("!","~")
    f = f.replace("+"," | ")
    return f

def our_to_user(f):
    f = f.split("+")
    l = []
    for m in f:
        m = '.'.join(list(m))
        liste_m = list(m)
        for c in liste_m:
            if c == c.upper() and c != ".":
                liste_m[liste_m.index(c)] = "!" + c
        l.append("".join(liste_m))
    return "+".join(l)


# Conversion_num_bin     validée    retourne liste de chaine
def Conversion_min_maj (disjonctive, nb_var):
    nouveau = []
    for term in disjonctive:
        for lettre in lettres:
            if term.find("¬" + lettre) != -1:   #    "¬A"  ->  "a"
                term = term.replace("¬" + lettre, lettre.lower())
        nouveau.append(term)
    return nouveau


def Conversion_num_bin_sans_nbvar (numeros):
    liste = []
    numeros = sorted(numeros)
    x = len(bin(max(numeros))) - 2
    for nombre in numeros:
        s = bin(nombre)[2:]  #6 -> "0000110"
        liste.append(s.zfill(x))
    return liste


def Conversion_num_bin (numeros,nb_var):
    liste = []
    numeros = sorted(numeros)
    x = nb_var
    for nombre in numeros:
        s = bin(nombre)[2:]  #6 -> "0000110"
        liste.append(s.zfill(x))
    return liste


# Conversion_algebre_bin  validée  retourne liste de chaine
def Conversion_algebre_bin (disjonctive):
    binaire = []
    if type(disjonctive) == str:
        disjonctive = ''.join(disjonctive.split(' '))       #Enlever les espaces
        disjonctive = disjonctive.split('+')                #Enlever l'opérateur +
    #print("disj = ",disjonctive)
    for term in disjonctive:
        monome = ""
        for lettre in term:
            if lettre == lettre.lower():
                monome = monome + '1'
            else:
                monome = monome + '0'
        binaire.append(monome)
    return binaire

# sympy_to_our      validée       retourne une chaine
def sympy_to_our(s):
    s = s.replace(" ", "")
    s = s.replace("&", "")
    s = s.replace("|", "+")
    s = s.replace("(", "")
    s = s.replace(")", "")
    ls = list(s)

    i = -1
    while i < len(ls):
        if (ls[i] == '~'):
            ls[i + 1] = ls[i + 1].upper()
            ls[i] = ''
            i = i + 2
        elif (ls[i].isalpha() and ls[i].isupper()):
            ls[i] = ls[i].lower()
            i = i + 1
        else:
            i = i + 1
    s = ''.join(ls)
    return s

# our_to_sympy          validée         retourne une chaine
def our_to_sympy(s):

    s = s.replace("+", "|")
    ls = list(s)
    i = 0
    while i < len(ls) - 1:
        if (ls[i].isalpha() and ls[i + 1].isalpha()) or (ls[i].isalpha() and ls[i + 1] == '(') or (
                ls[i] == ")" and ls[i + 1].isalpha()):
            ls.insert(i + 1, '&')
        i = i + 1;
    i = -1
    while i < len(ls) - 1:
        c = ls[i]
        if (c.isalpha()):
            if (c.isupper()):
                c = '~' + c
            # le cas (c) n'existe pas
            if (ls[i - 1] == "("):
                c = "(" + c
            if (ls[i + 1] == ")"):
                c = c + ")"
        ls[i] = c
        i = i + 1;
    ls = filter(lambda a: a not in {'(', ')'}, ls)
    s = (' '.join(ls)).upper()  # rajout d'espaces
    return s


def completion_parallèle(minterms,nb_var):
    form_literale = []
    p = multiprocessing.Pool()
    if type(minterms) == str:
        minterms = ''.join(minterms.split(' '))
        minterms = minterms.split("+")
    minterms = list(set(minterms))
    liste_bin = []
    lise_bin_save = [nb_var]
    liste = []
    for i in range(len(minterms)):
        liste_bin = lise_bin_save.copy()
        liste_bin.append(minterms[i])
        liste.append(liste_bin)
    #print(liste)
    resultat = p.map(boucle_completion_parallèle,liste)
    #print(resultat)
    for l in resultat:
        form_literale.extend(l)
    # form_literale = "+".join(form_literale)
    #print(form_literale)
    return list(set(form_literale))

def user_to_sympy(f):
    f = "".join(f.split(" "))
    f = f.upper()
    f = f.replace("."," & ")
    f = f.replace("!","~")
    f = f.replace("+"," | ")

    return f

def boucle_completion_parallèle(liste_bin):
    form_literale = []
    minterm = liste_bin[1]
    nb_var = liste_bin[0]
    vars = set(string.ascii_lowercase[0:nb_var])
    minterm = "".join(set(minterm))
    m = minterm.lower()
    if len(m) == len(set(m)):
        vars.difference_update(set(m))
        lsvar = list(vars)
        combs_bin = list(product('10', repeat=len(vars)))
        literal = minterm
        for term in combs_bin:
            for i in range(len(lsvar)):
                if term[i] == "0":
                    literal = literal + lsvar[i].upper()
                elif term[i] == "1":
                    literal = literal + lsvar[i]
            form_literale.append(literal)
            literal = minterm
    return form_literale


# regrouper                 validée            retourne une liste de chaines
def regrouper(mintermes, nb_var):
    if type(mintermes) == str: # si la formule est écrite sous forme d'une chaine
        mintermes = ''.join(mintermes.split(' '))
        mintermes = mintermes.split("+")

    listegroupes = []   # initialissation d'une liste vide qui va contenire les groupes
    for i in range(nb_var+1):# pour avoire une liste de nb_variables+1 sous liste
        listegroupes.append([])
    for minterme in mintermes:#parcourrer la liste des mintermes de la formule
        #--except retiré--
        m = list(minterme)#transformer le minterme(chine) vers à une liste de carractères
        n = m.count("1")        #ça donne le nombre d'ocurance de 1 dans le minterme m

        listegroupes[n].append(minterme) # inserer chaque minterme dans la sous liste corespondente à nb_1 dans ce minterme

    return listegroupes

#Adjacence              validée           retourne un minterme / None
def adjacence(m1,m2):
    m1 = list(m1)
    m2 = list(m2)
    simple = []
    i = 0
    arret = False
    nb_variable = len(m1)# m1 est suposé sous la forme sijenctive cannonique et converti en binaire , ainsi que m2
    if m1.count("-")==m2.count("-"):
        for i in range(nb_variable):
            if m1[i]==m2[i]:
                simple.append(m1[i])
            elif not arret :
                if m1!='-' and m2!="-":
                    simple.append('-')
                    arret = True
                else:
                    simple = None
                    arret = True
                    break
            else:
                simple = None
                break
    try:
        simple = ''.join(simple)
    except:
        simple = None
    if simple == '':
        simple = None
    return simple


# Retourne vrai si l'impliquant (impliq) peut représenter un minterme (terme), faux sinon
# contient          validée         retourne bool
def contient(impliq, terme):
    impliq = list(impliq)
    terme = list(terme)

    fin = False
    # Cas d'un impliquant groupé -> test: en supprimant toutes les indéterminés '-'
    while not fin:
        if "-" in impliq:
            i = impliq.index("-")
            impliq.pop(i)
            terme.pop(i)
        else:  # Cas d'un impliquant non groupé -> forcément un minterme
            fin = True
    if impliq == terme:
        return True
    else:
        return False


# Retourne la liste des impliquants premiers essentiels à partir de la liste des termes
# de la fonction (listf) et la liste des impliquants premiers (listImpliq)
#listIess            validée               retourne une liste de chaines
def listIess(listf, listImpliq):
    Iess = list()  # Initialisation à vide

    for i in range(len(listf)):
        j = 0
        sauv = str()  # Initialisation à vide
        cpt = 0  # Calcule le nb d'impliquants représentants un minterme
        while j < len(listImpliq) and cpt <= 1:
            if contient(listImpliq[j], listf[i]):
                sauv = listImpliq[j]
                cpt += 1
            j += 1
        if cpt == 1 and not sauv in Iess:  # Eviter les doublons
            Iess.append(sauv)
    return Iess

#Passage petrick ou pas        validée           retourne la liste des mintermes restants
def Arret(f,implq_prmier_ess):
    formules_minterme = []
    formules_minterme = f.copy()
    for premier in implq_prmier_ess:
        i = 0
        while i<len(formules_minterme):
            if contient(premier,formules_minterme[i]) == True :
                formules_minterme.pop(i)
                i = 0
            else:
                i += 1
    return formules_minterme

# ordonner      validée        retoune une liste de chaines
def ordonner_parallèe(f):
    #A = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    #global liste_alphabet
    p = multiprocessing.Pool()
    #f = '+'.join(minterms)
    return list(set(p.map(boucle_ordonner_parallèle,f)))

def boucle_ordonner_parallèle(minterm):
    global liste_alphabet
    return  ''.join(sorted(list(minterm), key=liste_alphabet.index))



def ConvInvers(formule_bin):
    if type(formule_bin) == str:
        formule_bin = "".join(formule_bin.split(" "))  # Enlève tous les espaces
        formule_bin = formule_bin.split("+")
    form_literale = []
    literal = []
    min_car = 65
    bits = len(formule_bin[0])
    if bits <= 26:
        for term in formule_bin:
            for i in range(min_car, min_car + bits):
                if term[i - min_car] == "1":
                    literal.append(chr(i).upper())
                elif term[i - min_car] == "0":
                    literal.append("!" + chr(i).upper())
            literal = ".".join(literal)
            form_literale.append(literal)
            literal = []
    else:
        for term in formule_bin:
            cpt = 1
            for chiffre in term:
                if chiffre == "1":
                    literal.append("X" + str(cpt))
                elif chiffre == "0":
                    literal.append("!X" + str(cpt))
                cpt += 1
            literal = ".".join(literal)
            form_literale.append(literal)
            literal = []
    form_literale = " + ".join(form_literale)
    if form_literale == "":
        return "Vrai"
    return form_literale

#ConvInvers_old         validée        retourne un chaine
def ConvInvers_old(formule_bin):
    if type(formule_bin) == str:
        formule_bin = "".join(formule_bin.split(" "))  # Enlève tous les espaces
        formule_bin = formule_bin.split("+")
    form_literale = []
    literal = ""
    min_car = 65
    for term in formule_bin:
        bits = len(term)
        for i in range(min_car, min_car + bits):
            if term[i - min_car] == "1":
                literal = literal + chr(i).upper()
            elif term[i - min_car] == "0":
                literal = literal + chr(i).lower()
        form_literale.append(literal)
        literal = ""
    form_literale = "+".join(form_literale)
    return form_literale

#impliq_premier_chakib          validée (non optimale)        retourne une liste de chaines
def impliq_premier_chakib_sans_dic(formule, nb_var):
    formule = list(set(formule))        #Pour enlever les doublants
    groupes = regrouper(formule, nb_var)
    groupes_copie = []
    # groupes_copie = formule
    groupes_copie = formule.copy()
    impliquant_premier = []
    nouv_groupe = []
    stop = False        # ou alors un booléen qui dit y avait-t-il adjacence ou pas
    while stop == False:
        #i = 0
        taille = len(groupes_copie)
        #print("Taille: ", taille)
        for i in range(len(groupes) - 1):
            #ne pas oublier le cas vide
            for terme1 in groupes[i]:
                for terme2 in groupes[i+1]:
                    minterme = adjacence(terme1, terme2)
                    if minterme != None:
                        if terme1 in groupes_copie:
                            groupes_copie.remove(terme1)
                        if terme2 in groupes_copie:
                            groupes_copie.remove(terme2)
                        if minterme not in nouv_groupe:
                            nouv_groupe.append(minterme)
        # Dans groupes_copie on aura tous les termes qui ne sont pas adjacents
        impliquant_premier.extend(groupes_copie)
        if taille == len(groupes_copie):
            stop = True
        else:
            groupes = regrouper(nouv_groupe, nb_var)
            groupes_copie = []
            groupes_copie = nouv_groupe.copy()
            nouv_groupe = []
    return list(set(impliquant_premier))


#impliq_premier_chakib     validée (non optimale)   retourne une liste de chaines, en ajoutant les groups dans dic
def impliq_premier_chakib(formule, nb_var, dic):
    formule = list(set(formule))        #Pour enlever les doublants
    groupes = regrouper(formule, nb_var)
    dic["groupes"] = groupes
    groupes_copie = []
    groupes_copie = formule.copy()
    impliquant_premier = []
    nouv_groupe = []
    stop = False        # ou alors un booléen qui dit y avait-t-il adjacence ou pas
    while stop == False:
        #i = 0
        taille = len(groupes_copie)
        #print("Taille: ", taille)
        for i in range(len(groupes) - 1):
            #ne pas oublier le cas vide
            for terme1 in groupes[i]:
                for terme2 in groupes[i+1]:
                    minterme = adjacence(terme1, terme2)
                    if minterme != None:
                        if terme1 in groupes_copie:
                            groupes_copie.remove(terme1)
                        if terme2 in groupes_copie:
                            groupes_copie.remove(terme2)
                        if minterme not in nouv_groupe:
                            nouv_groupe.append(minterme)
        # Dans groupes_copie on aura tous les termes qui ne sont pas adjacents
        impliquant_premier.extend(groupes_copie)
        if taille == len(groupes_copie):
            stop = True
        else:
            groupes = regrouper(nouv_groupe, nb_var)
            groupes_copie = []
            groupes_copie = nouv_groupe.copy()
            nouv_groupe = []
    return list(set(impliquant_premier))



#rand_numeric validée retourne une liste d'entiers
def rand_numeric(start, end, num):
    res = []
    j = 0
    while j <num:
        l = random.randint(start, end)
        if l not in res:    #Eviter les doublons
            res.append(l)
            j += 1
    return res


# rand_literal          validée              retourne une chaine
def rand_literal(nb_var,nb_minterme):
    A = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    A = A[:2*nb_var]
    f = []
    j = 0
    while j < nb_minterme:
        term = ""
        len_terme = random.randint(1,nb_var)
        for i in range(len_terme):
            l = random.randint(0,1)
            term += str(l)
        if term not in f :
            f.append(term)
            j += 1
    return ConvInvers_old(f)

# contien_fonction   validée            retourne la liste des mintermes restante de f
def contien_fonction(f,resultat):
    stop = False
    i = 0
    j = 0
    f = list(set(f))
    while not stop and i < len(f):
        m = f[i]
        trouve = False
        j = 0
        while not trouve and j < len(resultat):
            n = resultat[j]
            if contient(n, m):
                trouve = True
                f.pop(i)
            else:
                j += 1
        if trouve:
            i = 0
        else:
            i += 1
    return f


#speciale       validée              retourne une liste de mintermes (chaines)
def speciale (reste_termes, impliqNess):
    cpt = 0
    ancien = 0
    liste_optimale = []
    terme_optimal = ""
    reste_termes = list(set(reste_termes))
    impliqNess = list(set(impliqNess))
    stop = False
    while reste_termes != [] and not stop:           # On répète jusqu'à avoir exprimé tous les termes restants
        ancien = 0
        cpt = 0
        for impliq in impliqNess:       # Parcourir pour chaque impliquant
            for terme in reste_termes:      # Pour trouver les termes qu'il exprime
                if contient(impliq, terme):
                    cpt += 1
            if cpt > ancien:                # Pour trouver l'impliquant qui exprime le plus de termes
                terme_optimal = impliq      # Idée : si cpt == len(reste_termes) pas la peine de vérifier les autres impliquants
                ancien = cpt
            cpt = 0
        if terme_optimal != "":
            liste_optimale.append(terme_optimal)        # Ajouter l'impliquant qui exprime le plus de termes
            j = 0
            while j < len(reste_termes):
                if contient(terme_optimal, reste_termes[j]):
                    reste_termes.pop(j)                 # Enlever les termes exprimés par le meilleur impliquant
                    j -= 1
                j += 1
            impliqNess.remove(terme_optimal)            # Enlever le meilleur impliquant de la liste des impliquants
            terme_optimal = ""
        if impliqNess == []:
            stop = True

    return liste_optimale


# adjacence_groupes             NON validée        retourne une liste de chaines
def adjacence_groupes(liste_groupes):
    groupe1 = liste_groupes[0]
    groupe2 = liste_groupes[1]
    groupescopie = liste_groupes[2]
    nouv_groupe = []
    for terme1 in groupe1:
        for terme2 in groupe2:
            minterme = adjacence(terme1, terme2)
            if minterme != None:
                if terme1 in groupescopie:
                    groupescopie.remove(terme1)
                if terme2 in groupescopie:
                    groupescopie.remove(terme2)
                if minterme not in nouv_groupe:
                    nouv_groupe.append(minterme)
    liste = []
    liste.append(nouv_groupe)
    liste.append(groupescopie)
    return liste


#impliq_premier            validée             retourne une liste de chaines
def impliq_premier_sans_dic(formule, nb_var):
    formule = list(set(formule))
    groupes = regrouper(formule, nb_var)
    p = multiprocessing.Pool()
    groupes_copie = []
    for groupe in groupes:
        for terme in groupe:
            groupes_copie.append(terme)
    impliquant_premier = []
    nouv_groupe = []
    stop = False        # ou alors un booléen qui dit y avait-t-il adjacence ou pas
    while stop == False:
        i = 0
        taille = len(groupes_copie)
        liste_groupes = []
        for i in range(len(groupes) - 1):
            liste_three = []
            liste_three.append(groupes[i])
            liste_three.append(groupes[i+1])
            liste_three.append(groupes_copie)
            liste_groupes.append(liste_three)
        resultat = p.map(adjacence_groupes,liste_groupes)
        copy = set(groupes_copie.copy())
        for liste in resultat:
            nouv_groupe.append(liste[0])
            copy = set(copy).intersection(set(liste[1]))
        groupes_copie = list(copy)
        impliquant_premier.extend(groupes_copie)
        if taille == len(groupes_copie):
            stop = True
        else:
            groupes = nouv_groupe.copy()
            groupes_copie = []
            for groupe in groupes:
                for terme in groupe:
                    groupes_copie.append(terme)
            nouv_groupe = []
    return list(set(impliquant_premier))


#impliq_premier            validée             retourne une liste de chaines, en ajoutant les groupes dans dic
def impliq_premier_sans_obj(formule, nb_var, dic):
    formule = list(set(formule))
    groupes = regrouper(formule, nb_var)
    dic["groupes"] = groupes
    #print(groupes)
    p = multiprocessing.Pool()
    groupes_copie = []
    for groupe in groupes:
        for terme in groupe:
            groupes_copie.append(terme)
    """for i in range(nb_var+1):
        liste_liste.append([])"""
    impliquant_premier = []
    nouv_groupe = []
    stop = False        # ou alors un booléen qui dit y avait-t-il adjacence ou pas
    while stop == False:
        #print("\navant : ",groupes_copie)
        i = 0
        taille = len(groupes_copie)
        liste_groupes = []
        for i in range(len(groupes) - 1):
            liste_three = []
            liste_three.append(groupes[i])
            liste_three.append(groupes[i+1])
            liste_three.append(groupes_copie)
            liste_groupes.append(liste_three)
        #print("\nliste_groupes = \n",liste_groupes)
        #print("\nteste :\n ")
        resultat = p.map(adjacence_groupes,liste_groupes)
        copy = set(groupes_copie.copy())
        for liste in resultat:
            nouv_groupe.append(liste[0])
            #print("\nliste[1] = ",liste[1])
            copy = set(copy).intersection(set(liste[1]))
            #print("\ncopy = ",copy)
        groupes_copie = list(copy)
        """print("nouv_groupe = ",nouv_groupe)
        print("\nresultat = ",resultat)
        print("\napres : ",groupes_copie)"""
        impliquant_premier.extend(groupes_copie)
        if taille == len(groupes_copie):
            stop = True
        else:
            #groupes = regrouper(nouv_groupe, nb_var)
            groupes = nouv_groupe.copy()
            groupes_copie = []
            for groupe in groupes:
                for terme in groupe:
                    groupes_copie.append(terme)
            nouv_groupe = []
    return list(set(impliquant_premier))

# Retourne dans le dictionnaire une liste d'objets
def impliq_premier(formule, nb_var, dic):
    formule = list(set(formule))
    groupes = regrouper(formule, nb_var)
    liste = []
    for groupe in groupes:
        diction = {}
        diction["liste"] = groupe
        liste.append(diction)
    dic["groupes"] = liste
    #print(groupes)
    p = multiprocessing.Pool()
    groupes_copie = []
    for groupe in groupes:
        for terme in groupe:
            groupes_copie.append(terme)
    """for i in range(nb_var+1):
        liste_liste.append([])"""
    impliquant_premier = []
    nouv_groupe = []
    stop = False        # ou alors un booléen qui dit y avait-t-il adjacence ou pas
    while stop == False:
        #print("\navant : ",groupes_copie)
        i = 0
        taille = len(groupes_copie)
        liste_groupes = []
        for i in range(len(groupes) - 1):
            liste_three = []
            liste_three.append(groupes[i])
            liste_three.append(groupes[i+1])
            liste_three.append(groupes_copie)
            liste_groupes.append(liste_three)
        #print("\nliste_groupes = \n",liste_groupes)
        #print("\nteste :\n ")
        resultat = p.map(adjacence_groupes,liste_groupes)
        copy = set(groupes_copie.copy())
        for liste in resultat:
            nouv_groupe.append(liste[0])
            #print("\nliste[1] = ",liste[1])
            copy = set(copy).intersection(set(liste[1]))
            #print("\ncopy = ",copy)
        groupes_copie = list(copy)
        """print("nouv_groupe = ",nouv_groupe)
        print("\nresultat = ",resultat)
        print("\napres : ",groupes_copie)"""
        impliquant_premier.extend(groupes_copie)
        if taille == len(groupes_copie):
            stop = True
        else:
            #groupes = regrouper(nouv_groupe, nb_var)
            groupes = nouv_groupe.copy()
            groupes_copie = []
            for groupe in groupes:
                for terme in groupe:
                    groupes_copie.append(terme)
            nouv_groupe = []
    return list(set(impliquant_premier))



# nb_element_contient    validée       retourne nb de mintermes exprimés par un impliquent_premier
def nb_element_contient(impliq,reste_mintermes):
    cpt = 0
    for terme in reste_mintermes:  # Pour trouver les termes qu'il exprime
        if contient(impliq, terme):
            cpt += 1
    return cpt

# ConvInvers_synthèse        validée       retourne la syntaxe de synthèse
def ConvInvers_synthèse(formule_bin):
    if type(formule_bin) == str:
        formule_bin = "".join(formule_bin.split(" "))  # Enlève tous les espaces
        formule_bin = formule_bin.split("+")
    form_literale = []
    literal = []
    min_car = 65
    bits = len(formule_bin[0])
    if bits <= 26:
        for term in formule_bin:
            for i in range(min_car, min_car + bits):
                if term[i - min_car] == "1":
                    #literal = literal + chr(i).upper()
                    literal.append(chr(i).upper())
                elif term[i - min_car] == "0":
                    #literal = literal + "~" + chr(i).upper()
                    literal.append("~" + chr(i).upper())
            literal = " & ".join(literal)
            form_literale.append(literal)
            literal = []
    else:
        for term in formule_bin:
            cpt = 1
            for chiffre in term:
                if chiffre == "1":
                    literal.append("X" + str(cpt))
                elif chiffre == "0":
                    literal.append("~X" + str(cpt))
                cpt += 1
            literal = " & ".join(literal)
            form_literale.append(literal)
            literal = []
    form_literale = " + ".join(form_literale)
    return form_literale

# Retourne un dictionnaire d'attribut (Pi) à partir de la liste des impliquants non essentiels (ImpliqsNess)
def impliq_vers_lettre(ImpliqNess):
    diction = dict()
    for i in range(1, len(ImpliqNess) + 1):
        index = "P" + str(i)
        diction.update({index: ImpliqNess[i - 1]})
    return diction


# Générer la formule conjonctive de Petrick selon la syntaxe de la bib SymPy " (P1 | P2) & (..) & .. "
# à partir de la liste des termes restants (liste_termes) et le dictionnaire des impliquants non essentiels (diction)
def genConj(liste_terme, diction):
    tmp = list()  # Liste temporaire contenant les impliquants non essentiels symbolisés selon (diction)
    liste_finale = list()  # Liste contenant le produit des sommes (conjonction)
    somme = "("
    for terme in liste_terme:
        for impliq in diction:
            # Cas d'un impliquant qui exprime le terme
            if contient(diction[impliq], terme):
                tmp.append(impliq)
        # Jumeler les elements de (tmp) dans une chaine (somme) "(P1 | P2 | ..Pi)"
        for elem in tmp:
            if elem != tmp[-1]:
                somme = somme + elem + " | "
            else:
                somme = somme + elem + ")"

        liste_finale.append(somme)
        somme = "("
        tmp = []
        # print(liste_finale)
    liste_finale = " & ".join(liste_finale)  # Réaliser le produit des sommes
    return liste_finale


# Retourne le terme de coût minimum à partir d'une liste (formule)
def minimum(formule):
    sauv = formule[0]  # 1er terme
    for term in formule:
        if term.count("P") < sauv.count("P"):
            # '<' car pas de meilleur ( choisir la 1ere occurrence )
            # On utilise count car len ne sera pas correcte pour des index de tailles diff: len("P1") < len("P11")
            sauv = term
    return sauv


# Retourne la fonction simpliée totale sous forme disjonctive
# à partir d'une chaine de caractères (formule) sous la forme disjonctive,
# le dictionnaire des impliquants non essentiels (diction),
# et la liste des impliquants essentiels (liste_Iess) fournie par la méthode de McCluskey
def symplif(formule, diction):
    # formule= Sympy_to_our (formule)     #Formule de type chaine de caractère, conversion en externe
    formule = "".join(formule.split(" "))  # Enlève tous les espaces, très important dans les traitements
    formule = formule.split("+")
    optim = minimum(formule).upper()  # Trouver le terme de la formule de coût minimum
    print("optim :",optim)
    terme = []  # Liste des impliquants non essentiels adéquats
    term = "P"
    for car in optim:  # Parcourir car par car
        if car == "P":  # Dans ce cas on a atteint le prochain P(i) donc term contient P(i-1)
            print("term",term)
            if term in diction:
                terme.append(diction[term])
            term = "P"
            # pass
        elif car != " ":  # Car sans cette condition le dernier terme serait "P5 " pour "P1P4P5 " (sans enlever les espaces)
            term = term + car
    if term in diction:  # Pour le dernier terme
        terme.append(diction[term])
    print("terme : ",terme)
    return terme

#=========================================================================
# Modules originaux sans dictionnaire

#-----------------------------------------------
# Pour le cas exacte sans parallélisme
def McCLuskey_num_indeterminee_exacte_sans_dic(expr, indeterminee):
    # expr = "1, 2, 3, 4, 8"
    if type(expr) == str:
        expr = "".join(expr.split(" "))
        expr = expr.split(",")
        j = 0
        while j < len(expr):
            expr[j] = int(expr[j])
            j += 1
    if type(indeterminee) == str:
        if indeterminee != "":
            indeterminee = "".join(indeterminee.split(" "))
            indeterminee = indeterminee.split(",")
            j = 0
            while j < len(indeterminee):
                indeterminee[j] = int(indeterminee[j])
                j += 1
        else:
            indeterminee = []
    sauv_expr = expr.copy()
    if indeterminee != []:
        sauv_indeterminee = indeterminee.copy()
        indeterminee = list(set(indeterminee).difference(set(expr)))  # Pour enlever les indeterminees qui sont dans expr
        expr.extend(indeterminee)
    nb_var = len(bin(max(expr))) - 2
    expr = list(set(expr))
    if type(expr) == list:
        if type(expr[0]) != str:
            lsf = Conversion_num_bin(expr, nb_var)
            sauv_expr = Conversion_num_bin(sauv_expr, nb_var)
        else:
            lsf = expr.copy()
    else:
        pass

    # lsf contient la liste des tous les termes convertis en binaire
    lsf = list(set(lsf))
    lsf_sauv = lsf.copy()
    lsp = impliq_premier_sans_dic(lsf, nb_var)  # liste impliquants premiers

    # lsf contient la liste des termes non indéterminés
    lsf = sauv_expr.copy()
    ess = listIess(lsf, lsp)  # liste impliquants essentiels

    lsf = sauv_expr.copy()
    reste = Arret(lsf, ess)
    if len(reste) == 0:
        return ConvInvers(ess)
    else:
        ness = list(set(lsp).difference(set(ess)))
        ls = speciale(reste, ness)
        ls.extend(ess)
        return ConvInvers(ls)
#-----------------------------------------------

# Sans l'indeterminee (pour le parallélisme)
def McCLuskey_num_parallel(expr):
    #print(expr)
    expr = list(set(expr))
    # lsf contient la liste des tous les termes convertis en binaire

    lsf = list(set(expr))
    lsf_sauv = lsf.copy()
    nb_var = len(expr[0])
    lsp = impliq_premier_chakib_sans_dic(lsf, nb_var)  # liste impliquants premiers
    ess = listIess(lsf,lsp)
    reste = Arret(lsf, ess)
    if len(reste) == 0:
        return ess
    else:
        ness = list(set(lsp).difference(set(ess)))
        ls = speciale(reste, ness)
        ls.extend(ess)
        return ls

# Pour l'indeterminée (pour le parallélisme)
def McCLuskey_num_indeterminee_parallel(expr):
    nbre_indet = expr.pop(-1)       # il faut enlever le numéro au départ
    # lsf contient la liste des tous les termes convertis en binaire

    lsf = list(set(expr))
    lsf_sauv = lsf.copy()
    nb_var = len(expr[0])
    lsp = impliq_premier_chakib_sans_dic(lsf, nb_var)  # liste impliquants premiers
    # //////////////////////////////////
    for i in range(nbre_indet):
        expr.pop(-1)
        # Cette boucle permet de supprimer tous les indet
    # //////////////////////////////////
    ess = listIess(expr,lsp)
    sauv = expr.copy()
    reste = Arret(expr, ess)
    if len(reste) == 0:
        #print("resultat de contient fonction = ", contien_fonction(expr, ess))
        return ess
    else:
        ness = list(set(lsp).difference(set(ess)))
        ls = speciale(reste, ness)
        ls.extend(ess)
        return ls

# La division des termes se fait aléatoirement
def Mcluskey_parallele_sans_dic(expr,indeterminee, nb_var):
    p = multiprocessing.Pool()
    sauv_expr = expr.copy()
    if indeterminee != []:
        sauv_indeterminee = indeterminee.copy()
        indeterminee = list(set(indeterminee).difference(set(expr)))  # Pour enlever les indeterminees qui sont dans expr
        expr.extend(indeterminee)
    expr = list(set(expr))
    if type(expr) == list:
        if type(expr[0]) != str:
            lsf = Conversion_num_bin(expr, nb_var)
            sauv_expr = Conversion_num_bin(sauv_expr, nb_var)
        else:
            lsf = expr.copy()
    else:
        pass

    stop = False
    liste_entree = []
    lsf = list(set(lsf))
    while not stop:
        l = 0
        liste = []
        while l<500 and not stop:
            liste.append(lsf[0])
            lsf.pop(0)
            l+=1
            if lsf == []:
                stop = True
        liste_entree.append(liste)
    resultat_save = p.map(McCLuskey_num_parallel,liste_entree)
    resultat = []
    for l in resultat_save:
        resultat.extend(l)
    resultat = list(set(resultat))
    return ConvInvers(resultat)

# La division de l'ensemble des termes se fait bien plus précisément
def Mcluskey_parallele2_sans_dic(expr,indeterminee):
    p = multiprocessing.Pool()
    sauv_expr = expr.copy()
    if indeterminee != []:
        sauv_indeterminee = indeterminee.copy()
        indeterminee = list(set(indeterminee).difference(set(expr)))  # Pour enlever les indeterminees qui sont dans expr
        expr.extend(indeterminee)
    try:
        nb_var = len(bin(max(expr))) - 2
    except:
        nb_var = len(expr[0])
    expr = list(set(expr))
    if type(expr) == list:
        if type(expr[0]) != str:
            lsf = Conversion_num_bin(expr, nb_var)
            sauv_expr = Conversion_num_bin(sauv_expr, nb_var)
        else:
            lsf = expr.copy()
    else:
        pass

    stop = False
    liste_entree = []
    lsf = list(set(lsf))
    len_f = len(lsf)
    groupes = regrouper(lsf, nb_var)
    lsf = []
    while groupes != []:
       for g in groupes:
            t = 0
            ref = int((len(g)/len_f)*500) + 1
            while t <= ref and g != []:
                lsf.append(g[0])
                g.pop(0)
       while [] in groupes:
           groupes.remove([])

    while not stop:
        l = 0
        liste = []
        while l<500 and not stop:
            liste.append(lsf[0])
            lsf.pop(0)
            l+=1
            if lsf == []:
                stop = True
        liste_entree.append(liste)
    resultat_save = p.map(McCLuskey_num_parallel,liste_entree)
    resultat = []
    for l in resultat_save:
        resultat.extend(l)
    resultat = list(set(resultat))
    return ConvInvers(resultat)

# Elle traite l'indéterminée tout en divisant soignesement l'ensemble des termes
def Mcluskey_parallele3_sans_dic(expr, indeterminee):
    p = multiprocessing.Pool()
    sauv_expr = expr.copy()
    if indeterminee != []:
        sauv_indeterminee = indeterminee.copy()
        indeterminee = list(set(indeterminee).difference(set(expr)))  # Pour enlever les indeterminees qui sont dans expr
    try:
        nb_var = max(len(bin(max(expr))) - 2, len(bin(max(indeterminee))) - 2)
    except:
        nb_var = len(expr[0])
    expr = list(set(expr))
    if type(expr) == list:
        if type(expr[0]) != str:
            lsf = Conversion_num_bin(expr, nb_var)          # sans les indeterminées
            sauv_expr = Conversion_num_bin(sauv_expr, nb_var)
            #Plus
            indeterminee = Conversion_num_bin(indeterminee, nb_var)
        else:
            lsf = expr.copy()
    else:
        pass
    """print("Taille indet: ", len(indeterminee))
    print("Taille expr: ", len(expr))
    print("Taille globale: ", len(expr) + len(indeterminee))"""
    stop = False
    stop2 = False
    liste_entree = []
    lsf = list(set(lsf))
    len_f = len(lsf)
    groupes = regrouper(lsf, nb_var)
    lsf = []
    while groupes != []:
        for g in groupes:
            t = 0
            ref = int((len(g) / len_f) * 500) + 1
            while t <= ref and g != []:
                lsf.append(g[0])
                g.pop(0)
        while [] in groupes:
            groupes.remove([])

    while not stop:
        l = 0
        liste = []
        while l < 500 and not stop:
            liste.append(lsf[0])
            lsf.pop(0)
            l += 1
            if lsf == []:
                stop = True

        # Partie pour insérer les indet
        j = 0
        while j < 100 and not stop2:         # Le seuil à améliorer
            liste.append(indeterminee[0])
            indeterminee.pop(0)
            j += 1
            if indeterminee == []:
                stop2 = True
        #print("Taille: ", len(liste))
        liste.append(j)  # Pour savoir le nombre d'indeterminées insérées, pour le traitement dans le module
        # Fin de la partie

        liste_entree.append(liste)
    resultat_save = p.map(McCLuskey_num_indeterminee_parallel, liste_entree)
    resultat = []
    for l in resultat_save:
        resultat.extend(l)
    resultat = list(set(resultat))
    return ConvInvers(resultat)

#=========================================================================



#=========================================================================
# Modules avec dictionnaire pour le link


# retourne la simplification exacte avec un dictionnaire (validée)

def McCLuskey_num_indeterminee_exacte(expr, indeterminee):
    dic = {}
    if type(expr) == str:
        expr = "".join(expr.split(" "))
        expr = expr.split(",")
        j = 0
        while j < len(expr):
            expr[j] = int(expr[j])
            j += 1
    if type(indeterminee) == str:
        if indeterminee != "":
            indeterminee = "".join(indeterminee.split(" "))
            indeterminee = indeterminee.split(",")
            j = 0
            while j < len(indeterminee):
                indeterminee[j] = int(indeterminee[j])
                j += 1
        else:
            indeterminee = []
    sauv_expr = expr.copy()
    if indeterminee != []:
        sauv_indeterminee = indeterminee.copy()
        indeterminee = list(set(indeterminee).difference(set(expr)))  # Pour enlever les indeterminees qui sont dans expr
        expr.extend(indeterminee)
    #nb_var = len(bin(max(expr))) - 2
    expr = list(set(expr))
    if type(expr) == list:
        if type(expr[0]) != str:
            nb_var = len(bin(max(expr))) - 2
            lsf = Conversion_num_bin(expr, nb_var)
            sauv_expr = Conversion_num_bin(sauv_expr, nb_var)
        else:
            lsf = expr.copy()
            nb_var = len(expr[0])
    else:
        pass

    # lsf contient la liste des tous les termes convertis en binaire
    lsf = list(set(lsf))
    lsf_sauv = lsf.copy()
    dic["fonction"] = sauv_expr.copy()
    lsp = impliq_premier(lsf, nb_var, dic)  # liste impliquants premiers

    # lsf contient la liste des termes non indéterminés
    lsf = sauv_expr.copy()
    ess = listIess(lsf, lsp)  # liste impliquants essentiels
    dic["premiers"] = lsp
    dic["essentiels"] = ess

    lsf = sauv_expr.copy()
    reste = Arret(lsf, ess)
    if len(reste) == 0:
        dic["resultat"] = ConvInvers(ess)
        return dic
    else:
        ness = list(set(lsp).difference(set(ess)))
        ls = speciale(reste, ness)
        ls.extend(ess)
        dic["resultat"] = ConvInvers(ls)
        return dic

# Sans l'indeterminee (pour le parallélisme) avec dic
def McCLuskey_num_parallel_avec_dic(expr):
    #print(expr)
    expr = list(set(expr))
    # lsf contient la liste des tous les termes convertis en binaire
    resultat = []           # Contiendra une liste contenant impliquants premiers, essentiels et résultat
    lsf = list(set(expr))
    lsf_sauv = lsf.copy()
    nb_var = len(expr[0])
    lsp = impliq_premier_chakib_sans_dic(lsf, nb_var)  # liste impliquants premiers
    resultat.append(lsp)
    ess = listIess(lsf,lsp)
    resultat.append(ess)
    reste = Arret(lsf, ess)
    if len(reste) == 0:
        resultat.append(ess)   # ess est la liste essentielle et résultat en même temps
        return resultat
    else:
        ness = list(set(lsp).difference(set(ess)))
        ls = speciale(reste, ness)
        ls.extend(ess)
        resultat.append(ls)
        return resultat

# Pour l'indeterminée (pour le parallélisme) avec dic
def McCLuskey_num_indeterminee_parallel_avec_dic(expr):
    nbre_indet = expr.pop(-1)       # il faut enlever le numéro au départ
    resultat = []           # Contiendra une liste contenant impliquants premiers, essentiels et résultat
    # lsf contient la liste des tous les termes convertis en binaire

    lsf = list(set(expr))
    lsf_sauv = lsf.copy()
    nb_var = len(expr[0])
    lsp = impliq_premier_chakib_sans_dic(lsf, nb_var)  # liste impliquants premiers
    resultat.append(lsp)
    # //////////////////////////////////
    for i in range(nbre_indet):
        expr.pop(-1)
        # Cette boucle permet de supprimer tous les indet
    # //////////////////////////////////
    ess = listIess(expr,lsp)
    resultat.append(ess)
    sauv = expr.copy()
    reste = Arret(expr, ess)
    if len(reste) == 0:
        resultat.append(ess)
        return resultat
    else:
        ness = list(set(lsp).difference(set(ess)))
        ls = speciale(reste, ness)
        ls.extend(ess)
        resultat.append(ls)
        return resultat



# La division des termes se fait aléatoirement, ne traite pas l'indéterminée ---  avec dictionnaire (avec liste d'objets) ---
def Mcluskey_parallele(expr,indeterminee, nb_var):
    p = multiprocessing.Pool()
    dic = {}
    sauv_expr = expr.copy()
    if indeterminee != []:
        sauv_indeterminee = indeterminee.copy()
        indeterminee = list(set(indeterminee).difference(set(expr)))  # Pour enlever les indeterminees qui sont dans expr
        expr.extend(indeterminee)
    expr = list(set(expr))
    if type(expr) == list:
        if type(expr[0]) != str:
            lsf = Conversion_num_bin(expr, nb_var)
            sauv_expr = Conversion_num_bin(sauv_expr, nb_var)
        else:
            lsf = expr.copy()
    else:
        pass

    stop = False
    liste_entree = []
    lsf = list(set(lsf))
    dic["fonction"] = lsf.copy()
    if len(lsf) == 2 ** nb_var:
        groupes = regrouper(lsf, nb_var)
        # =======================================
        # Pour créer une liste d'objets
        liste = []
        for groupe in groupes:
            diction = {}
            diction["liste"] = groupe
            liste.append(diction)
        dic["groupes"] = liste
        # =======================================
        dic["premiers"] = [""]
        dic["essentiels"] = [""]
        dic["resultat"] = ["-" * nb_var]
        return dic
    groupes = regrouper(lsf, nb_var)
    # =======================================
    # Pour créer une liste d'objets
    petitGroupe = []
    for groupe in groupes:
        diction = {}
        diction["liste"] = groupe
        petitGroupe.append(diction)
    dic["groupes"] = petitGroupe
    # =======================================
    while not stop:
        l = 0
        liste = []
        while l<500 and not stop:
            liste.append(lsf[0])
            lsf.pop(0)
            l+=1
            if lsf == []:
                stop = True
        liste_entree.append(liste)
    resultat_save = p.map(McCLuskey_num_parallel_avec_dic,liste_entree)
    resultat = []
    """dic["premiers"] = lsp
    dic["essentiels"] = ess"""
    premiers = []
    ess = []
    for liste in resultat_save:
        premiers.extend(liste[0])
        ess.extend(liste[1])
        resultat.extend(liste[2])
    premiers = list(set(premiers))
    ess = list(set(ess))
    resultat = list(set(resultat))
    dic["premiers"] = premiers
    dic["essentiels"] = ess
    dic["resultat"] = ConvInvers(resultat)
    #dic["resultat"] = resultat
    return dic

# La division de l'ensemble des termes se fait bien plus précisément, ---  avec dictionnaire (avec liste d'objets)  ---
def Mcluskey_parallele2(expr,indeterminee):
    p = multiprocessing.Pool()
    dic = {}
    sauv_expr = expr.copy()
    if indeterminee != []:
        sauv_indeterminee = indeterminee.copy()
        indeterminee = list(set(indeterminee).difference(set(expr)))  # Pour enlever les indeterminees qui sont dans expr
        expr.extend(indeterminee)
    try:
        nb_var = len(bin(max(expr))) - 2
    except:
        nb_var = len(expr[0])
    expr = list(set(expr))
    if type(expr) == list:
        if type(expr[0]) != str:
            lsf = Conversion_num_bin(expr, nb_var)
            sauv_expr = Conversion_num_bin(sauv_expr, nb_var)
        else:
            lsf = expr.copy()
    else:
        pass

    stop = False
    liste_entree = []
    lsf = list(set(lsf))
    len_f = len(lsf)
    dic["fonction"] = lsf.copy()
    if len(lsf) == 2 ** nb_var:
        groupes = regrouper(lsf, nb_var)
        # =======================================
        # Pour créer une liste d'objets
        liste = []
        for groupe in groupes:
            diction = {}
            diction["liste"] = groupe.copy()
            liste.append(diction)
        dic["groupes"] = liste
        # =======================================
        dic["premiers"] = [""]
        dic["essentiels"] = [""]
        dic["resultat"] = ["-" * nb_var]
        return dic
    groupes = regrouper(lsf, nb_var)
    # =======================================
    # Pour créer une liste d'objets
    liste = []
    for groupe in groupes:
        diction = {}
        diction["liste"] = groupe.copy()   # copy est importante car sinon le groupe sera vidée dans la while groupes != []
        liste.append(diction)
    dic["groupes"] = liste
    # =======================================
    lsf = []
    while groupes != []:
       for g in groupes:
            t = 0
            ref = int((len(g)/len_f)*500) + 1
            while t <= ref and g != []:
                lsf.append(g[0])
                g.pop(0)
       while [] in groupes:
           groupes.remove([])
    while not stop:
        l = 0
        liste = []
        while l<500 and not stop:
            liste.append(lsf[0])
            lsf.pop(0)
            l+=1
            if lsf == []:
                stop = True
        liste_entree.append(liste)
    resultat_save = p.map(McCLuskey_num_parallel_avec_dic,liste_entree)
    resultat = []
    premiers = []
    ess = []
    for liste in resultat_save:
        premiers.extend(liste[0])
        ess.extend(liste[1])
        resultat.extend(liste[2])
    premiers = list(set(premiers))
    ess = list(set(ess))
    resultat = list(set(resultat))
    dic["premiers"] = premiers
    dic["essentiels"] = ess
    dic["resultat"] = ConvInvers(resultat)
    #dic["resultat"] = resultat
    return dic

# Elle traite l'indéterminée tout en divisant soignesement l'ensemble des termes, ---  avec dictionnaire (avec liste d'objets) ---
def Mcluskey_parallele3(expr, indeterminee):
    p = multiprocessing.Pool()
    dic = {}
    sauv_expr = expr.copy()
    nb = 0
    if indeterminee != []:
        sauv_indeterminee = indeterminee.copy()
        indeterminee = list(set(indeterminee).difference(set(expr)))  # Pour enlever les indeterminees qui sont dans expr
    try:
        if indeterminee != []:
            nb_var = max(len(bin(max(expr))) - 2, len(bin(max(indeterminee))) - 2)
        else:
            nb_var = len(bin(max(expr))) - 2
    except:
        nb_var = len(expr[0])
    expr = list(set(expr))
    if type(expr) == list:
        if type(expr[0]) != str:
            lsf = Conversion_num_bin(expr, nb_var)          # sans les indeterminées
            sauv_expr = Conversion_num_bin(sauv_expr, nb_var)
            #Plus
            indeterminee = Conversion_num_bin(indeterminee, nb_var)
        else:
            lsf = expr.copy()
    else:
        pass
    """print("Taille indet: ", len(indeterminee))
    print("Taille expr: ", len(expr))
    print("Taille globale: ", len(expr) + len(indeterminee))"""
    stop = False
    stop2 = False
    liste_entree = []
    lsf = list(set(lsf))
    len_f = len(lsf)
    dic["fonction"] = lsf.copy()
    if len(lsf) == 2 ** nb_var:
        groupes = regrouper(lsf, nb_var)
        # =======================================
        # Pour créer une liste d'objets
        liste = []
        for groupe in groupes:
            diction = {}
            diction["liste"] = groupe.copy()
            liste.append(diction)
        dic["groupes"] = liste
        # =======================================
        dic["premiers"] = [""]
        dic["essentiels"] = [""]
        dic["resultat"] = ["-" * nb_var]
        return dic
    groupes = regrouper(lsf, nb_var)
    # =======================================
    # Pour créer une liste d'objets
    liste = []
    for groupe in groupes:
        diction = {}
        diction["liste"] = groupe.copy()
        liste.append(diction)
    dic["groupes"] = liste
    # =======================================
    lsf = []
    while groupes != []:
        for g in groupes:
            t = 0
            ref = int((len(g) / len_f) * 500) + 1
            while t <= ref and g != []:
                lsf.append(g[0])
                g.pop(0)
        while [] in groupes:
            groupes.remove([])

    while not stop:
        l = 0
        liste = []
        while l < 500 and not stop:
            liste.append(lsf[0])
            lsf.pop(0)
            l += 1
            if lsf == []:
                stop = True

        # Partie pour insérer les indet
        j = 0
        if indeterminee != []:
            while j < 100 and not stop2:         # Le seuil à améliorer
                liste.append(indeterminee[0])
                indeterminee.pop(0)
                j += 1
                if indeterminee == []:
                    stop2 = True
        #print("Taille: ", len(liste))
        liste.append(j)  # Pour savoir le nombre d'indeterminées insérées, pour le traitement dans le module
        # Fin de la partie

        liste_entree.append(liste)
    resultat_save = p.map(McCLuskey_num_indeterminee_parallel_avec_dic, liste_entree)
    resultat = []
    premiers = []
    ess = []
    for liste in resultat_save:
        premiers.extend(liste[0])
        ess.extend(liste[1])
        resultat.extend(liste[2])
    premiers = list(set(premiers))
    ess = list(set(ess))
    resultat = list(set(resultat))
    dic["premiers"] = premiers
    dic["essentiels"] = ess
    dic["resultat"] = ConvInvers(resultat)
    #dic["resultat"] = resultat
    return dic


# Elle traite l'indéterminée tout en divisant aléatoirement l'ensemble des termes, ---  avec dictionnaire (avec liste d'objet) ---
def Mcluskey_parallele4(expr, indeterminee):
    p = multiprocessing.Pool()
    dic = {}
    sauv_expr = expr.copy()
    nb = 0
    if indeterminee != []:
        sauv_indeterminee = indeterminee.copy()
        indeterminee = list(set(indeterminee).difference(set(expr)))  # Pour enlever les indeterminees qui sont dans expr
    try:
        if indeterminee != []:
            nb_var = max(len(bin(max(expr))) - 2, len(bin(max(indeterminee))) - 2)
        else:
            nb_var = len(bin(max(expr))) - 2
    except:
        nb_var = len(expr[0])
    expr = list(set(expr))
    if type(expr) == list:
        if type(expr[0]) != str:
            lsf = Conversion_num_bin(expr, nb_var)          # sans les indeterminées
            sauv_expr = Conversion_num_bin(sauv_expr, nb_var)
            #Plus
            indeterminee = Conversion_num_bin(indeterminee, nb_var)
        else:
            lsf = expr.copy()
    else:
        pass
    """print("Taille indet: ", len(indeterminee))
    print("Taille expr: ", len(expr))
    print("Taille globale: ", len(expr) + len(indeterminee))"""
    stop = False
    stop2 = False
    liste_entree = []
    lsf = list(set(lsf))
    dic["fonction"] = lsf.copy()
    if len(lsf) == 2 ** nb_var:
        dic["premiers"] = [""]
        groupes = regrouper(lsf, nb_var)
        # =======================================
        # Pour créer une liste d'objets
        liste = []
        for groupe in groupes:
            diction = {}
            diction["liste"] = groupe.copy()
            liste.append(diction)
        dic["groupes"] = liste
        # =======================================
        dic["essentiels"] = [""]
        dic["resultat"] = ["-" * nb_var]
        return dic
    groupes = regrouper(lsf, nb_var)
    # =======================================
    # Pour créer une liste d'objets
    liste = []
    for groupe in groupes:
        diction = {}
        diction["liste"] = groupe.copy()
        liste.append(diction)
    dic["groupes"] = liste
    # =======================================
    while not stop:
        l = 0
        liste = []
        while l < 500 and not stop:
            liste.append(lsf[0])
            lsf.pop(0)
            l += 1
            if lsf == []:
                stop = True

        # Partie pour insérer les indet
        j = 0
        if indeterminee != []:
            while j < 100 and not stop2:         # Le seuil à améliorer
                liste.append(indeterminee[0])
                indeterminee.pop(0)
                j += 1
                if indeterminee == []:
                    stop2 = True
        #print("Taille: ", len(liste))
        liste.append(j)  # Pour savoir le nombre d'indeterminées insérées, pour le traitement dans le module
        # Fin de la partie

        liste_entree.append(liste)
    resultat_save = p.map(McCLuskey_num_indeterminee_parallel_avec_dic, liste_entree)
    resultat = []
    premiers = []
    ess = []
    for liste in resultat_save:
        premiers.extend(liste[0])
        ess.extend(liste[1])
        resultat.extend(liste[2])
    premiers = list(set(premiers))
    ess = list(set(ess))
    resultat = list(set(resultat))
    dic["premiers"] = premiers
    dic["essentiels"] = ess
    dic["resultat"] = ConvInvers(resultat)
    #dic["resultat"] = resultat
    return dic


def ConvSynthese(expr):
    expr = "".join(expr.split(" "))
    expr = expr.replace(".", "&")
    expr = expr.replace("!", "~")
    if ("(" not in expr) or (")" not in expr):
        expr = expr.split("+")
        formule = []
        i = 0
        while i < len(expr):
            liste = []
            for j in range(4):
                if i < len(expr):
                    # Ici on ajoute les parenthèses pour séparer les ET
                    terme = expr[i].split("&")
                    k = 0
                    liste_termes = []
                    while k < len(terme):
                        termes = []
                        for index in range(4):
                            if k < len(terme):
                                termes.append(terme[k])
                            k += 1
                        liste_termes.append("(" + "&".join(termes) + ")")
                    liste.append("&".join(liste_termes))
                i += 1
            # Ici on ajoute les parenthèses pour séparer les OU
            formule.append("(" + "+".join(liste) + ")")
        formule = "+".join(formule)
    else:   # ((A+B)+!C)&(!A+B+C) =>  [(A+B+!C), (!A+B+C)]
        expr = expr.split("&")
        formule = []
        i = 0
        while i < len(expr):
            liste = []
            expr[i].replace("(", "")
            expr[i].replace(")", "")        # (A+B+!C) => A+B+!C
            for j in range(4):
                if i < len(expr):
                    # Ici on ajoute les parenthèses pour séparer les OU
                    terme = expr[i].split("+")
                    k = 0
                    liste_termes = []
                    while k < len(terme):
                        termes = []
                        for index in range(4):
                            if k < len(terme):
                                termes.append(terme[k])
                            k += 1
                        liste_termes.append("(" + "+".join(termes) + ")")
                    liste.append("(" + "+".join(liste_termes) + ")")
                i += 1
            # Ici on ajoute les parenthèses pour séparer les ET
            formule.append("(" + "&".join(liste) + ")")
        formule = "&".join(formule)
    return formule



#donne le resultat sous forme conj/dij
#forme = "DNF" ou "CNF"


def forme_resultat(formule, forme):
    formule_copy = formule
    formule = user_to_sympy(formule)

    formule = sympify(formule, locals=dict(_clash))

    if forme == "DNF":  # forme normale disjonctive
        return formule_copy.upper()
    elif forme == "CNF":  # forme normale conjonctive
        x = str(to_cnf(formule))
        x = x.replace("&", ".")
        x = x.replace("|", "+")
        x = x.replace("~", "!")
        x = "".join(x.split(" "))
        return x
