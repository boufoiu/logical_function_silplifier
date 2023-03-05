def verification(formule, nb_var):
    non = ["!"]
    operateurs = ["+", ".", "^", "º", "#"]
    nb_par_ouvrantes = 0
    nb_par_fermantes = 0
    formule = formule.upper()
    formule = "".join(formule.split(" "))  # Enlève tous les espaces
    erreurs = []
    min_car = 65
    max_car = min(90, 65+nb_var-1)
    faute = False
    if formule == "":
        faute = True
    else:
        if formule[0] not in ["(", non[0]] and (ord(formule[0]) < min_car or ord(formule[0]) > max_car):
            erreurs.append(f"Erreur à la première position ")
            faute = True
        if formule[0] == "(":  # Incrémenter le nombre de parenthèses ouvrantes si la formule débute par (
            nb_par_ouvrantes += 1
        longueur = len(formule)
        i = 1
        while i < longueur - 1:  # Car le premier et dernier caractère sont traités à part
            car = formule[i]
            prec = formule[i - 1]
            suiv = formule[i + 1]
            if ord(car) >= min_car and ord(car) <= max_car:  # Traitement d'une lettre alphabétique
                if ord(prec) >= min_car and ord(prec) <= max_car:  # 2 lettres collés: AB
                    erreurs.append(f"Il manque un opèrateur à la {i+2}éme position")
                    faute = True
                # Une lettre ou un NON après une lettre: BA , A!
                if (ord(suiv) >= min_car and ord(suiv) <= max_car) or suiv in non:
                    if suiv in non :
                        erreurs.append(f"Un opérateur ")
                    else:
                        erreurs.append(f"Il manque un opèrateur à la {i+1}éme position")
                    faute = True
            elif car in non:  # Traitement du caractère NON
                # ) ou une lettre avant NON: )! , A!
                if prec == ")" or (ord(prec) >= min_car and ord(prec) <= max_car):
                    if prec == ")" :
                        erreurs.append(f"Il manque un opèrateur à la {i+2}éme position")
                    faute = True
                # Un opérateur ou ) après NON: !+ , !)
                if suiv in operateurs or suiv == ")":
                    erreurs.append(f"Une parenthèse fermante après un opèrateur de nègation à la {i+2}ème position")
                    faute = True
            elif car in operateurs:  # Traitement des opérateurs
                # ( ou NON ou un opérateur avant un opérateur: (+ , !+ , ++
                if prec == "(" or prec in non or prec in operateurs:
                    if prec not in non:
                        erreurs.append(f"Mal utilisation de l'opèrateur à la {i+2}ème position")
                    faute = True
                # ) ou un opérateur après un opérateur: .) , .+
                if suiv == ")" or suiv in operateurs:
                    if suiv ==")":
                        erreurs.append(f"Une parenthèse fermante après un opèrateur à la {i+2}ème position")
                    
                    faute = True
            elif car == "(":  # Traitement d'une paranthèse ouvrante
                nb_par_ouvrantes += 1
                # Si pas un NON et pas un opérateur avant ( donc erreur
                if prec not in non and prec not in operateurs and prec != "(" :
                    erreurs.append(f"Mal utilisation de la parenthèse ouvrante à la {i+1}ème position")
                    faute = True
                # Un opérateur ou ) après ( : (+ , ()
                if suiv in operateurs or suiv == ")":
                    if suiv == ")":
                        erreurs.append(f"Parenthèses vides à {i+1}ème position")
                    faute = True
            elif car == ")":  # Traitement d'une paranthèse fermante
                nb_par_fermantes += 1
                # Un NON ou un opérateur ou ( avant ) : !) , +) , ()
                if prec in non or prec in operateurs or prec == "(":
                    faute = True
                # Si pas un opérateur et pas ) après ) donc erreur
                if suiv not in operateurs and suiv != ")":
                    faute = True
                if nb_par_fermantes > nb_par_ouvrantes:
                    erreurs.append(f"Parenthèse ouvrante manquante avant la {i+1}ème position")
                    faute = True
            else:
                if ord(car)<= 90 and ord(car)>max_car :
                    erreurs.append(f"Utilisation d'une variable non déclarée (nombre de variables érronné)")
                faute = True
            i += 1
        if len(formule) == 1:  # Dans le cas d'une formule contenant un seul caractère
            i = 0
        car = formule[i]  # Traitement du dernier caractère
        # Pas une lettre et pas un ) à la fin de la formule
        if (ord(car) < min_car or ord(car) > max_car) and car != ")":
            erreurs.append(f"Erreur à la dernière position")
            faute = True
        if len(formule) == 2:  # Dans le cas d'une formule contenant 2 caractères (correcte seulement dans le cas: !A)
            if formule[0] != "!" and ord(formule[1])<min_car or ord(formule[1])>max_car:  # Dans d'autres cas elle est sûrement fausse
                erreurs.append("Formule incorrecte")
                faute = True
        if (car == ")"):  # Incrémenter le nombre de parenthèses fermantes si la formule se termine par )
            nb_par_fermantes += 1
        if nb_par_ouvrantes > nb_par_fermantes:
            erreurs.append("Parenthèses fermantes manquantes ")
            faute = True
        elif nb_par_ouvrantes < nb_par_fermantes:
            erreurs.append("Parenthèses ouvrantes manquantes ")
            faute = True
    if faute == True:
        return "\n".join(erreurs)
    else:
        return "Pas d'erreurs"
