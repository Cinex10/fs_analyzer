from neo4j import GraphDatabase

# Connexion à Neo4j
uri = "bolt://localhost:7687"  # URI de votre instance Neo4j
username = "neo4j"  # Votre nom d'utilisateur
password = "password"  # Votre mot de passe
driver = GraphDatabase.driver(uri, auth=(username, password))

# Fonction pour créer des nœuds et des relations
def create_graph(words):
    with driver.session() as session:
        # Nettoie la base de données (facultatif)
        session.run("MATCH (n) DETACH DELETE n")

        # Crée les nœuds Start et End
        session.run("CREATE (:Start {name: '_Start'})")
        session.run("CREATE (:End {name: '_End'})")

        # Liste pour stocker les identifiants des nœuds de mots
        word_nodes = []

        # Crée un nœud pour chaque mot (même mot = nouveau nœud)
        for i, word in enumerate(words):
            result = session.run(
                """
                CREATE (w:Word {name: $name, id: $id})
                RETURN id(w) AS node_id
                """,
                name=word,
                id=i  # Ajoute un ID unique basé sur l'index dans la phrase
            )
            word_nodes.append(result.single()["node_id"])

        # Crée les relations successives (r_succ)
        for i in range(len(word_nodes) - 1):
            session.run(
                """
                MATCH (a:Word), (b:Word)
                WHERE id(a) = $id1 AND id(b) = $id2
                CREATE (a)-[:r_succ]->(b)
                """,
                id1=word_nodes[i],
                id2=word_nodes[i + 1]
            )

        # Lier le premier mot au nœud Start
        session.run(
            """
            MATCH (start:Start), (firstWord:Word)
            WHERE id(firstWord) = $first_word_id
            CREATE (start)-[:STARTS]->(firstWord)
            """,
            first_word_id=word_nodes[0]
        )

        # Lier le dernier mot au nœud End
        session.run(
            """
            MATCH (end:End), (lastWord:Word)
            WHERE id(lastWord) = $last_word_id
            CREATE (lastWord)-[:ENDS]->(end)
            """,
            last_word_id=word_nodes[-1]
        )
    
def create_node(Word) :
    with driver.session() as session: 
         session.run("CREATE (:Word {name: $name})", name=Word)


def create_relation (name1 , name2 ) : 
    pass 
     
def create_word_tag_relations(word_tag_map):
    with driver.session() as session:
        for word, relations in word_tag_map.items():
            for relation in relations:
                relation_type = relation['relation_type']
                to_node_name = relation['to_node_name']
                to_node_type = relation['to_node_type']

                # Merge sur tout le modèle (Word, relation et nœud cible) pour éviter les doublons
                session.run(
                    f"""
                    MERGE (w:Word {{name: $word}})
                    CREATE (n:{to_node_type} {{name: $to_node_name}})
                    CREATE (w)-[:{relation_type}]->(n)
                    """,
                    word=word,
                    to_node_name=to_node_name
                )


# Fonction pour fermer la connexion à Neo4j
def close_connection():
    driver.close()

