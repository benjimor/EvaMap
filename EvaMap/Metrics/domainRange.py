import rdflib

from EvaMap.Metrics.metric import metric

def domainRange(g_onto, liste_map, g_map, raw_data, g_link) :
    nbPossible = 0
    points = 0
    liste_O = []
    result = metric()
    result['name'] = "Domain and range of properties"
    for s, p, o in g_map.triples((None, None,None)):
        expected = ""
        nbPossible = nbPossible + 2
        boolean = True
        if p == rdflib.term.URIRef('a') or p == rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'):
            boolean = True if isinstance(o, rdflib.URIRef) else False
            expected = "URI"
        elif p == rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#label'):
            boolean = True if isinstance(o, rdflib.URIRef) else False
            expected = "URI"
        else:
            for _, _, o2 in g_link.triples((p, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#domain'), None)): #Pour toutes les valeurs domain de p
                expected = str(o2)
                for _, _, o3 in g_link.triples((s, (rdflib.term.URIRef('a')|rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')), None)) : #On récupère le type du sujet
                    if o2 != o3 and o2 != rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#Resource') : #Si le domaine de p est différent du type du sujet et que, cas général, le domaine de p n'est pas une ressource
                        liste_O.append(o3)	#On stock le type du sujet
                        for _, _, o4 in g_link.triples((s, rdflib.term.URIRef('https://www.w3.org/2002/07/owl#equivalentClass'), None)): #Pour tous les équivalents au sujet
                            for _, _, o6 in g_link.triples((s, (rdflib.term.URIRef('a')|rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')), None)) : #On récupère les type des sujets equivalents
                                liste_O.append(o4) #On stock ces types aussi
                        for O in liste_O : #Pour l'ensemble des types récupérés
                            for _, _, o5 in g_link.triples((O, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'), None)) : #on regarde pour toutes les sous-classes des types (équivalents ou non) de notre sujet
                                if o2 == o5: #Si ils sont équivalents au domaine
                                    boolean = True
                    else:
                        boolean = True
        if boolean:
            points = points + 1
        else:
            result['feedbacks'].append(f"{str(p)} has the wrong domain. Expected a {expected}")
        liste_O = []
        boolean = True
        for _, _, o2 in g_link.triples((p, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#range'), None)):
            boolean = False
            expected = str(o2)
            o3 = None
            if isinstance(o, rdflib.term.Literal):
                if o.datatype is not None:
                    o3 = o.datatype
                    if o2 == o3 : boolean = True
            if o3 is None:
                if isinstance(o, rdflib.term.URIRef):
                    for _, _, o3 in g_link.triples((o, rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')), None): #On récupère le type de l'objet
                        if o2 != o3:
                            liste_O.append(o3)	# On stock le type du sujet
                            for _, _, o4 in g_link.triples((s, rdflib.term.URIRef('https://www.w3.org/2002/07/owl#equivalentClass'), None)): #Pour tous les équivalents au sujet
                                for _, _, o6 in g_link.triples((s, (rdflib.term.URIRef('a')|rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')), None)) : #On récupère les type des sujets equivalents
                                    liste_O.append(o4) # On stock ces types aussi
                            for O in liste_O : # Pour l'ensemble des types récupérés
                                for _, _, o5 in g_link.triples((O, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'), None)) : #on regarde pour toutes les sous-classes des types (équivalents ou non) de notre sujet
                                    if o2 == o5: # Si ils sont équivalents au domaine
                                        boolean = True
                        else :
                            boolean = True
        if boolean:
            points = points + 1
        else:
            result['feedbacks'].append(f"{str(p)} has the wrong range. Expected a {expected}")

    if nbPossible == 0:
        result['score'] = 1
    else:
        result['score'] = 1-(nbPossible - points)/nbPossible
    return result
