from src.ModulesFinaux import *

def McCluskey_num_indeterminee_finale (expr, indeterminee):
    if type(expr) == str:
        expr = "".join(expr.split(" "))
        expr = expr.split(",")
        j = 0
        while j < len(expr):
            expr[j] = int(expr[j])
            j += 1
    #if type(indeterminee) == str:
    if indeterminee != None:
        indeterminee = "".join(indeterminee.split(" "))
        indeterminee = indeterminee.split(",")
        j = 0
        while j < len(indeterminee):
            indeterminee[j] = int(indeterminee[j])
            j += 1
    else:
        indeterminee = []
    if (len(expr) + len(indeterminee) < 600):       # A redéfinir
        return McCLuskey_num_indeterminee_exacte(expr, indeterminee)
    else:
        return Mcluskey_parallele4(expr, indeterminee)      # Le choix peut changer ensuite