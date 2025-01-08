import pdb
from neo4j import GraphDatabase

# Connexion à Neo4j
uri = "bolt://localhost:7687"  # URI de votre instance Neo4j
username = "neo4j"  # Votre nom d'utilisateur
password = "password"  # Votre mot de passe
driver = GraphDatabase.driver(uri, auth=(username, password))

# Fonction pour créer des nœuds et des relations
def create_graph(words):
    with driver.session() as session:
        # Nettoie la base de données
        session.run("MATCH (n) DETACH DELETE n")

        # Crée les nœuds Start et End
        session.run("CREATE (:Start {name: '_Start'})")
        session.run("CREATE (:End {name: '_End'})")

        # Crée un nœud pour chaque mot
        for i, word in enumerate(words):
            session.run(
                """
                CREATE (w:Word {name: $name, rang: $rang})
                """,
                name=word,
                rang=i
            )

        # Crée les relations successives (r_succ)
        for i in range(len(words) - 1):
            session.run(
                """
                MATCH (a:Word {rang: $rang1}), (b:Word {rang: $rang2})
                CREATE (a)-[:r_succ]->(b)
                """,
                rang1=i,
                rang2=i + 1
            )

        # Lier le premier mot au nœud Start
        session.run(
            """
            MATCH (start:Start), (firstWord:Word {rang: 0})
            CREATE (start)-[:r_succ]->(firstWord)
            """
        )

        # Lier le dernier mot au nœud End
        session.run(
            """
            MATCH (end:End), (lastWord:Word {rang: $last_rang})
            CREATE (lastWord)-[:r_succ]->(end)
            """,
            last_rang=len(words) - 1
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




def compound_words(compound_words_detection_res):
    """
    Connecte les fragments détectés dans le graphe en reliant le fragment au mot précédent et suivant.
    """
    with driver.session() as session:
        for compound_word_data in compound_words_detection_res:
            fragments = compound_word_data["compound_word"]
            fragment_str = ' '.join(fragments)
            fragment_length = len(fragments)

            # Créer un nœud pour le fragment
            session.run(
                """
                MERGE (frag:Word {name: $fragment_name})
                """,
                fragment_name=fragment_str
            )

            # Trouver le mot précédent et le mot suivant en une seule requête
            query = """
                    MATCH (prev)-[:r_succ]->(start:Word {name: $first_fragment_word})
                    MATCH (end:Word {name: $last_fragment_word})-[:r_succ]->(next)
                    MATCH path = (start)-[:r_succ*]->(end)
                    WHERE length(path) = $path_length
                    RETURN id(prev) AS prev_id, id(next) AS next_id
                    """
            result = session.run(
                query,
                first_fragment_word=fragments[0],
                last_fragment_word=fragments[-1],
                path_length=fragment_length - 1
            )


            record = result.single()

            if record:
                prev_id = record["prev_id"]
                next_id = record["next_id"]
                # Créer une relation entre le mot précédent et le fragment
                session.run(
                    """
                    MATCH (prev)
                    WHERE id(prev) = $prev_id
                    MATCH (frag:Word {name: $fragment_name})
                    MERGE (prev)-[:r_succ]->(frag)
                    """,
                    fragment_name=fragment_str,
                    prev_id=prev_id
                )

                # Créer une relation entre le fragment et le mot suivant
                session.run(
                    """
                    MATCH (frag:Word {name: $fragment_name})
                    MATCH (next) 
                    WHERE id(next) = $next_id
                    MERGE (frag)-[:r_succ]->(next)
                    """,
                    fragment_name=fragment_str,
                    next_id=next_id
                )

def apply_rules(rules):
    with driver.session() as session:
        for rule in rules:
            rule = rule.strip()  # Enlève les espaces inutiles
            if rule:
                try:
                    session.run(rule)  # Exécute la règle sur Neo4j
                except Exception as e:
                    print(f"Error applying rule: {rule}\n{e}")


# Fonction pour fermer la connexion à Neo4j
def close_connection():
    driver.close()

