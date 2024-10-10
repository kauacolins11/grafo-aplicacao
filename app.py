import networkx as nx
from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

# Criando o grafo bipartido
graph = nx.Graph()

# Dicionário de músicas por gênero
musicas_por_genero = {
    'Rock': [
        {'nome': 'Bohemian Rhapsody', 'artista': 'Queen'},
        {'nome': 'Hotel California', 'artista': 'Eagles'}
    ],
    'Pop': [
        {'nome': 'Shape of You', 'artista': 'Ed Sheeran'},
        {'nome': 'Blinding Lights', 'artista': 'The Weeknd'}
    ],
    'Jazz': [
        {'nome': 'Take Five', 'artista': 'Dave Brubeck'},
        {'nome': 'So What', 'artista': 'Miles Davis'}
    ],
    'Eletrônica': [
        {'nome': 'Titanium', 'artista': 'David Guetta ft. Sia'},
        {'nome': 'Wake Me Up', 'artista': 'Avicii'}
    ],
    'Hip-Hop': [
        {'nome': 'Sicko Mode', 'artista': 'Travis Scott'},
        {'nome': 'Lose Yourself', 'artista': 'Eminem'}
    ],
    'Country': [
        {'nome': 'Jolene', 'artista': 'Dolly Parton'},
        {'nome': 'The Gambler', 'artista': 'Kenny Rogers'}
    ],
    'Clássica': [
        {'nome': 'Clair de Lune', 'artista': 'Debussy'},
        {'nome': 'Symphony No. 5', 'artista': 'Beethoven'}
    ],
    'Reggae': [
        {'nome': 'No Woman, No Cry', 'artista': 'Bob Marley'},
        {'nome': 'Bad Boys', 'artista': 'Inner Circle'}
    ],
    'Blues': [
        {'nome': 'The Thrill is Gone', 'artista': 'B.B. King'},
        {'nome': 'Hoochie Coochie Man', 'artista': 'Muddy Waters'}
    ],
    'Funk': [
        {'nome': 'Superstition', 'artista': 'Stevie Wonder'},
        {'nome': 'Get Up (I Feel Like Being a) Sex Machine', 'artista': 'James Brown'}
    ],
    'Sertanejo': [
        {'nome': 'Evidências', 'artista': 'Chitãozinho & Xororó'},
        {'nome': 'Ai Ai Ai', 'artista': 'Vitor Kley'}
    ],
    'K-Pop': [
        {'nome': 'Dynamite', 'artista': 'BTS'},
        {'nome': 'Lovesick Girls', 'artista': 'BLACKPINK'}
    ],
    'R&B': [
        {'nome': 'Blame It', 'artista': 'Jamie Foxx'},
        {'nome': 'No Guidance', 'artista': 'Chris Brown ft. Drake'}
    ],
    'Soul': [
        {'nome': 'A Change is Gonna Come', 'artista': 'Sam Cooke'},
        {'nome': 'Respect', 'artista': 'Aretha Franklin'}
    ],
    'Pagode': [
        {'nome': 'O Mundo é um Moinho', 'artista': 'Cartola'},
        {'nome': 'Deixa eu te Amar', 'artista': 'Sorriso Maroto'}
    ],
    'MPB': [
        {'nome': 'Apenas Mais Uma de Amor', 'artista': 'Lulu Santos'},
        {'nome': 'Garota de Ipanema', 'artista': 'Tom Jobim'}
    ],
    'Samba': [
        {'nome': 'Mas, que Nada!', 'artista': 'Jorge Ben Jor'},
        {'nome': 'Cazuza', 'artista': 'Exalta Samba'}
    ],
    'Forró': [
        {'nome': 'Asa Branca', 'artista': 'Luiz Gonzaga'},
        {'nome': 'Olha Pro Céu', 'artista': 'Luiz Gonzaga'}
    ],
    'Trap': [
        {'nome': 'Bad and Boujee', 'artista': 'Migos'},
        {'nome': 'Gucci Gang', 'artista': 'Lil Pump'}
    ]
}

# Dicionário de gêneros semelhantes
generos_semelhantes = {
    'Rock': ['Pop', 'Blues', 'Funk'],
    'Pop': ['Rock', 'Hip-Hop', 'R&B'],
    'Jazz': ['Blues', 'Soul'],
    'Eletrônica': ['Hip-Hop', 'Pop'],
    'Hip-Hop': ['R&B', 'Pop'],
    'Country': ['Funk', 'Sertanejo'],
    'Clássica': ['Jazz', 'Soul'],
    'Reggae': ['Samba', 'MPB'],
    'Blues': ['Rock', 'Jazz'],
    'Funk': ['Soul', 'Hip-Hop'],
    'Sertanejo': ['Country', 'Pagode'],
    'K-Pop': ['Pop', 'Eletrônica'],
    'R&B': ['Hip-Hop', 'Soul'],
    'Soul': ['Jazz', 'Funk'],
    'Pagode': ['Samba', 'Sertanejo'],
    'MPB': ['Samba', 'Reggae'],
    'Samba': ['Reggae', 'MPB'],
    'Forró': ['Sertanejo', 'Pagode'],
    'Trap': ['Hip-Hop', 'Eletrônica']
}

generos = list(musicas_por_genero.keys())

# Adicionar nós e arestas ao grafo
for genero, musicas in musicas_por_genero.items():
    graph.add_node(genero)
    for musica in musicas:
        nome = musica['nome']
        artista = musica['artista']
        # Cria um nó para cada música e conecta ao seu gênero
        graph.add_node(nome, artista=artista)  # Adicionando artista como atributo
        graph.add_edge(genero, nome)

# Função para recomendar músicas semelhantes por gênero
def recomendar_musicas_semelhantes(genero):
    similares = generos_semelhantes.get(genero, [])
    musicas_semelhantes = []  # Usamos uma lista ao invés de set
    
    for gen in similares:
        # Para cada gênero similar, pegamos as músicas e incluímos o nome e o gênero
        musicas_semelhantes.extend([
            {'nome': musica['nome'], 'artista': musica['artista'], 'genero': gen}
            for musica in musicas_por_genero.get(gen, [])
        ])
    
    return musicas_semelhantes


# Função para recomendar músicas usando BFS (Busca em Largura)
def recomendar_musica_por_genero_bfs(genero):
    # Inicia a busca em largura a partir do nó do gênero
    bfs_edges = list(nx.bfs_edges(graph, genero))
    recomendacoes = [{'nome': j, 'artista': graph.nodes[j]['artista'], 'genero': genero} 
                     for i, j in bfs_edges if i == genero]
    return recomendacoes


@app.route('/', methods=['GET', 'POST'])
def index():
    recomendacoes = []
    recomendacoes_similares = []

    if request.method == 'POST':
        genero_escolhido = request.form.get('genero')
        if genero_escolhido in musicas_por_genero:
            recomendacoes = recomendar_musica_por_genero_bfs(genero_escolhido)

            # Gêneros semelhantes
            recomendacoes_similares = recomendar_musicas_semelhantes(genero_escolhido)

    return render_template('index.html', recomendacoes=recomendacoes, recomendacoes_similares=recomendacoes_similares)
    

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")  # Abre o navegador padrão
    app.run(debug=True)