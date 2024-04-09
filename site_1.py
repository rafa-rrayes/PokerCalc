import streamlit as st
from pokercalc import *
# Mapping for card suits
naipes = {
    "O": "D",  # Ouros to Diamonds
    "C": "C",  # Copas to Clubs
    "E": "S",  # Espadas to Spades
    "P": "H"   # Paus to Hearts
}

# Initialize cartasJogador and cartasMesa in session state if not present
if 'cartasJogador' not in st.session_state:
    st.session_state.cartasJogador = []
if 'cartasMesa' not in st.session_state:
    st.session_state.cartasMesa = []

def adicionar_carta(carta, naipe, target):
    # Append the selected card to the appropriate list in the session state
    carta_full = carta + ' de ' + naipe
    if target == "jogador" and carta_full not in st.session_state.cartasJogador:
        st.session_state.cartasJogador.append(carta_full)
    elif target == "mesa" and carta_full not in st.session_state.cartasMesa:
        st.session_state.cartasMesa.append(carta_full)

st.title("Calculadora de Poker")

# UI elements for input
jogadores = st.selectbox(
    'Numero de jogadores',
    ('2', '3', '4', '5', '6', '7', '8', '9', '10')
)
carta = st.selectbox(
    'Carta',
    ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
)
naipe = st.radio(
    "Naipe",
    ["Copas :hearts:", "Ouros :diamonds:", "Paus :clubs:", "Espadas :spades:"]
)

# Buttons to add a card to player's hand or to the table
col1, col2 = st.columns(2)
with col1:
    if st.button('Adicionar ao Jogador'):
        adicionar_carta(carta, naipe, "jogador")
    # Display checkboxes for player's cards
    st.write("Cartas do jogador:")
    for cartaJ in st.session_state.cartasJogador:
        if st.checkbox(cartaJ, key="jogador_"+cartaJ, value=False):
            st.session_state.cartasJogador.remove(cartaJ)
            st.rerun()
with col2:
    if st.button('Adicionar à Mesa'):
        adicionar_carta(carta, naipe, "mesa")
    st.write("Cartas na mesa:")
    for cartaM in st.session_state.cartasMesa:
        if st.checkbox(cartaM, key="mesa_"+cartaM, value=False):
            st.session_state.cartasMesa.remove(cartaM)
            st.rerun()
if st.button('Calcular'):
    try:
        cartasPlayer = []
        for cartinha in st.session_state.cartasJogador:
            numero = cartinha.split(' de ')[0]
            if numero == '10':
                numero = 'T'
            naip = naipes[cartinha.split(' de ')[1][0]]
            cartasPlayer.append(numero + naip)
        cartasMesa = []
        for cartinha in st.session_state.cartasMesa:
            numero = cartinha.split(' de ')[0]
            if numero == '10':
                numero = 'T'
            naip = naipes[cartinha.split(' de ')[1][0]]
            cartasMesa.append(numero + naip)
        if len(cartasPlayer) != 2 or len(cartasMesa) > 5:
            raise Exception("Cartas inválidas")
        if len(cartasMesa+cartasPlayer) != len(list(set(cartasMesa+cartasPlayer))):
            raise Exception("Cartas invalidas")
        probabilidade = calculateProb(cartasPlayer, cartasMesa, int(jogadores), 10000)
        st.write(f"Probabilidade de ganhar: {probabilidade[0]} %, de empatar: {probabilidade[1]} %")
        st.write(f"Os outros jogadores tem: {probabilidade[2]} % de probabilidade de ganhar")
        st.write(" ")
        if probabilidade[0] > probabilidade[2]:
            st.write("Você é o que tem maior chance de ganhar! vai com tudo!")
        st.write("Outs:")
        for out, chance in probabilidade[3].items():
            st.write(f"{out}:      {round(chance, 2)} %", )
        

    except:
        st.write("Ocorreu algum erro, confira se você selecionou as cartas corretamente")