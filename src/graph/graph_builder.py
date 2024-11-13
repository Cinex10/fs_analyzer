from neo4j import GraphDatabase

# Connexion à Neo4j
uri = "bolt://localhost:7688"  # URI de votre instance Neo4j
username = "neo4j"  # Votre nom d'utilisateur
password = "testpassword"  # Votre mot de passe
driver = GraphDatabase.driver(uri, auth=(username, password))

# Fonction pour créer des nœuds et des relations
def create_graph(words):
    with driver.session() as session:
        # Nettoie la base de données (facultatif)
        session.run("MATCH (n) DETACH DELETE n")
        
        session.run("CREATE (:Start {name: '_Start'})")

        session.run("CREATE (:End {name: '_End'})")



        # Crée des nœuds pour chaque mot
        for word in words:
            session.run("CREATE (:Word {name: $name})", name=word)
        
        # Exemple de relations (crée des relations entre mots successifs)
        for i in range(len(words) - 1):
            
            session.run(
                """
                MATCH (a:Word {name: $name1}), (b:Word {name: $name2})
                CREATE (a)-[:r_succ]->(b)
                """,
                name1=words[i],
                name2=words[i + 1]
            )


         # Lier le nœud "start" au premier mot
        session.run(
            """
            MATCH (start:Start), (firstWord:Word {name: $firstWord})
            CREATE (start)-[:STARTS]->(firstWord)
            """, 
            firstWord=words[0]
        )
        
        # Lier le nœud "end" au dernier mot
        session.run(
            """
            MATCH (end:End), (lastWord:Word {name: $lastWord})
            CREATE (lastWord)-[:ENDS]->(end)
            """, 
            lastWord=words[-1]
        )
    
def create_node(Word) :
    with driver.session() as session: 
         session.run("CREATE (:Word {name: $name})", name=Word)


def create_relation (name1 , name2 ) : 
    pass 
     
# Fonction pour fermer la connexion à Neo4j
def close_connection():
    driver.close()
