from cProfile import label
import schemdraw
from schemdraw.parsing import logic_parser
from  schemdraw import logic
import schemdraw.elements as elm
from src.ModulesFinaux import ConvSynthese


def Synthese(formule):
    if(formule=="VRAI"):
            d= schemdraw.Drawing(show=False)
            d += elm.Dot().label('1', loc='left')
            d += elm.Line().label('f', loc='right')

    else:
        if(formule == "FAUX"):
            d = schemdraw.Drawing(show=False)
            d += elm.Dot().label('0', loc='left')
            d += elm.Line().label('f', loc='right')
        else:
            formule=ConvSynthese(formule)
            # schemdraw.theme("solarizedl")
            # Convertir une formule binaire en une formule littérale selon la syntaxe de SchemDraw
            d = logic_parser.logicparse(formule, outlabel='$f$', gateH=1.25, gateW=5)
            # d.config(bgcolor='#85ebd9')

    d.save("./Synthese.png", transparent=False)



