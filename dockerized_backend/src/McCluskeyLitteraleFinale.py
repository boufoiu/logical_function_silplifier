from src.ModulesFinaux import *
from sympy import *
from sympy.abc import _clash
lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def McCLuskey_litterale_finale_avant(expr, nb_var):
    expr = expr.upper()
    cpt = 0
    copie = list(expr)
    for lettre in lettres:
        if lettre in copie:
            cpt = lettres.index(lettre) + 1
    if cpt < nb_var:
        nb_var = cpt
    expr = user_to_sympy(expr)
    expr = sympify(expr, locals=dict(_clash))
    expr = to_dnf(expr,force = True)
    expr = str(expr)
    expr = sympy_to_our(expr)
    taille = len(expr.split("+"))
    if type(expr) == str:
        expr = ordonner_parallèe(completion_parallèle(expr, nb_var))
        if expr == []:
            dic = {}
            dic["resultat"] = "Faux"
            return dic
        lsf = Conversion_algebre_bin(expr)
    lsf = list(set(lsf))
    if len(lsf) < 600:

        return McCLuskey_num_indeterminee_exacte(lsf, [])
    else:
        dic = Mcluskey_parallele(lsf, [], nb_var)
        if len(dic["resultat"].split("+")) > taille:
            dic["resultat"] = "".join(copie)
        return dic


"""def Mcluskey_parallele_avec_repitition(expr,indeterminee, nb_var):
    stop = False
    l = 0
    while not stop:
        resultat = Mcluskey_parallele(expr, indeterminee, nb_var)
        if l < len(resultat):
            l = len(resultat)
            indeterminee = []
        else:
            stop = True
    return resultat"""