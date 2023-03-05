from http.client import ImproperConnectionState
from fastapi import FastAPI                             # Création des APIs
from fastapi.middleware.cors import CORSMiddleware      # Limiter l'accès aux APIs
# Nos modules:
from src.Vérification import verification
from src.McCluskeyLitteraleFinale import *
# from McCluskeyLitteraleFinale1 import *
# from McCluskeyLittérale import *
from src.McCluskeyNumFinale import *
from src.ModulesFinaux import *
from src.Synthese import Synthese 

app = FastAPI()


# Configuring CORS ( allow defined frontend origins to communicate to these backend APIs )
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#    ___________
#      A P I s


@app.get("/SimplificationLitterale")
async def get_functionLit(nbVar: int, formule: str ):
    x = verification(formule, nbVar)
    diction={}
        # Erreur syntaxique
    if x != "Pas d'erreurs":
        diction["err"] = 1
        diction["resultat"] = x
    else:
        # Formule simplifiée
        diction["err"] = 0
        diction["resultat"] = McCLuskey_litterale_finale_avant (formule, nbVar)
    return diction


# API validée
@app.get("/RandomLitterale")
async def get_randomfunctionLit(nbVar : int , nbmin : int) : 
    diction={}
    diction["randLit"] = our_to_user(rand_literal(nbVar, nbmin))
    return diction

# API validée
@app.get("/SimplificationNumerique")
async def get_functionNum(exp: str, indet: str=None ):
    diction= McCluskey_num_indeterminee_finale(exp, indet)
    return diction

# API validée
@app.get("/RandomNumerique")
async def get_randomfunctionNum(debut: int, fin: int, nbMin: int):
    diction = {}
    diction["randNum"] = rand_numeric(debut, fin, nbMin)
    return diction


# API validée
@app.get("/FormeResultat")
async def get_formeResultat(formule: str, forme: str):
    diction = {}
    diction["formeRes"] = forme_resultat(formule, forme)
    return diction

# API validée
@app.get("/Synthese")
async def get_synthese(formule: str):
    # Nothing is returned
    Synthese(formule)
    return {"Success": "True"}
