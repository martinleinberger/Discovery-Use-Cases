# This program acts as a hello world program. It's goal is to extract all names of files that are stored in the
# antlrLexer contribution


import rdflib

#namespace of 101companies
ns = rdflib.Namespace('http://101companies.org/property/')

#recursive load, which will further explore folders and files of a given entry point
#this is used to build the graph
def recLoad(g, uri):
    g2 = rdflib.Graph()
    g2.load(uri)
    for row in g2.query(
        """
        SELECT ?o WHERE { {?s co:folder ?o } UNION {?s co:file ?o } }
        """,
        initNs=dict(co=ns)
    ):
        recLoad(g2, row[0])

    g += g2

#commands to build the graph
g = rdflib.Graph()
recLoad(g, 'http://localhost/services/discovery/contributions/antlrLexer?format=rdf')

#sparql query that will get us all filenames
qres = g.query("""
                SELECT DISTINCT ?name
                WHERE {
                    ?file co:classifier "File" .
                    ?file co:name ?name
                }
               """,
               initNs=dict(
                   co=ns
               ))

#printing of results
for row in qres.result:
    print row



#other, more exploratory stuff:
    # for s, p, o in g:
    #     print s, p, o
    #
    # print '-------------'
    #
    # for x in g.subject_predicates(object='build.gradle'):
    #     print x
    #
    # print '-------------'
    #
    # for x in g.subject_objects(predicate=rdflib.URIRef('http://101companies.org/property/file')):
    #     print x