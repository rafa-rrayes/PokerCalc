import streamlit as st
import anthropic
import base64
import os
from dotenv import load_dotenv
from pokercalc import *

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Initialize session state
if 'cartasJogador' not in st.session_state:
    st.session_state.cartasJogador = []
if 'cartasMesa' not in st.session_state:
    st.session_state.cartasMesa = []
if 'detected' not in st.session_state:
    st.session_state.detected = False

SUIT_DISPLAY = {
    'H': '♥️', 'D': '♦️', 'C': '♣️', 'S': '♠️'
}
SUIT_NAME = {
    'H': 'Copas', 'D': 'Ouros', 'C': 'Paus', 'S': 'Espadas'
}
RANK_DISPLAY = {
    '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
    '7': '7', '8': '8', '9': '9', 'T': '10',
    'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
}
VALID_RANKS = set(RANK_DISPLAY.keys())
VALID_SUITS = set(SUIT_DISPLAY.keys())


def card_display(code):
    """Convert 'AH' -> 'A ♥️'"""
    rank = RANK_DISPLAY.get(code[0], code[0])
    suit = SUIT_DISPLAY.get(code[1], code[1])
    return f"{rank} {suit}"


def detect_cards(image_bytes, media_type="image/jpeg"):
    """Send image to Claude Vision and detect poker cards."""
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "You are analyzing a photo of a poker game. Identify every visible playing card.\n\n"
                            "Return EXACTLY this format (no extra text):\n"
                            "PLAYER: XX, XX\n"
                            "TABLE: XX, XX, XX\n\n"
                            "Card notation:\n"
                            "- Rank: 2 3 4 5 6 7 8 9 T(=10) J Q K A\n"
                            "- Suit: H(Hearts) D(Diamonds) C(Clubs) S(Spades)\n"
                            "Example: AH = Ace of Hearts, TC = 10 of Clubs\n\n"
                            "The player's cards are usually the 2 cards closest to the camera / held in hand.\n"
                            "The table cards (community) are the ones in the center.\n"
                            "If you cannot distinguish player from table, put them all under TABLE and leave PLAYER empty.\n"
                            "Only include cards you can clearly identify."
                        ),
                    },
                ],
            }
        ],
    )
    return message.content[0].text


def parse_detection(response_text):
    """Parse Claude's response into (player_cards, table_cards) lists."""
    player = []
    table = []

    for line in response_text.strip().splitlines():
        line = line.strip()
        if line.upper().startswith("PLAYER:"):
            raw = line.split(":", 1)[1].strip()
            player = _parse_card_list(raw)
        elif line.upper().startswith("TABLE:"):
            raw = line.split(":", 1)[1].strip()
            table = _parse_card_list(raw)

    return player, table


def _parse_card_list(raw):
    """Turn 'AH, TC, 2D' into ['AH', 'TC', '2D'], validating each."""
    cards = []
    for token in raw.replace("[", "").replace("]", "").split(","):
        token = token.strip().upper()
        if len(token) == 2 and token[0] in VALID_RANKS and token[1] in VALID_SUITS:
            cards.append(token)
    return cards


def media_type_for(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if filename else "jpg"
    return {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "webp": "image/webp",
    }.get(ext, "image/jpeg")


# ── UI ────────────────────────────────────────────────────────────────

st.title("Calculadora de Poker")
st.caption("Tire uma foto ou faça upload de uma imagem das cartas")

jogadores = st.selectbox(
    "Numero de jogadores",
    ("2", "3", "4", "5", "6", "7", "8", "9", "10"),
)

tab_cam, tab_upload = st.tabs(["Câmera", "Upload"])

with tab_cam:
    camera_image = st.camera_input("Tire uma foto das cartas")

with tab_upload:
    uploaded_image = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png", "webp"])

# Determine which image to use
image_data = None
image_media_type = "image/jpeg"
if camera_image:
    image_data = camera_image.getvalue()
    image_media_type = "image/jpeg"
elif uploaded_image:
    image_data = uploaded_image.getvalue()
    image_media_type = media_type_for(uploaded_image.name)

if image_data:
    st.image(image_data, caption="Imagem capturada", use_container_width=True)

    if st.button("Detectar Cartas"):
        with st.spinner("Claude está analisando as cartas..."):
            try:
                response = detect_cards(image_data, image_media_type)
                st.session_state.claude_response = response
                player, table = parse_detection(response)
                st.session_state.cartasJogador = player
                st.session_state.cartasMesa = table
                st.session_state.detected = True
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao detectar cartas: {e}")

# ── Show detected / editable cards ───────────────────────────────────

if st.session_state.detected:
    if "claude_response" in st.session_state:
        with st.expander("Resposta do Claude"):
            st.code(st.session_state.claude_response)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cartas do Jogador")
        to_remove = []
        for i, c in enumerate(st.session_state.cartasJogador):
            if st.checkbox(card_display(c), key=f"pj_{c}_{i}", value=False):
                to_remove.append(c)
        if to_remove:
            for c in to_remove:
                st.session_state.cartasJogador.remove(c)
            st.rerun()

    with col2:
        st.subheader("Cartas na Mesa")
        to_remove = []
        for i, c in enumerate(st.session_state.cartasMesa):
            if st.checkbox(card_display(c), key=f"ms_{c}_{i}", value=False):
                to_remove.append(c)
        if to_remove:
            for c in to_remove:
                st.session_state.cartasMesa.remove(c)
            st.rerun()

    # Manual correction
    with st.expander("Adicionar carta manualmente"):
        mc1, mc2 = st.columns(2)
        with mc1:
            carta_manual = st.selectbox(
                "Carta",
                list(RANK_DISPLAY.keys()),
                format_func=lambda r: RANK_DISPLAY[r],
            )
        with mc2:
            naipe_manual = st.selectbox(
                "Naipe",
                list(SUIT_DISPLAY.keys()),
                format_func=lambda s: f"{SUIT_DISPLAY[s]} {SUIT_NAME[s]}",
            )
        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button("Adicionar ao Jogador"):
                code = carta_manual + naipe_manual
                if code not in st.session_state.cartasJogador:
                    st.session_state.cartasJogador.append(code)
                    st.rerun()
        with bc2:
            if st.button("Adicionar à Mesa"):
                code = carta_manual + naipe_manual
                if code not in st.session_state.cartasMesa:
                    st.session_state.cartasMesa.append(code)
                    st.rerun()

    # ── Calculate ─────────────────────────────────────────────────────
    if st.button("Calcular"):
        try:
            cartasPlayer = list(st.session_state.cartasJogador)
            cartasMesa = list(st.session_state.cartasMesa)

            if len(cartasPlayer) != 2:
                raise ValueError("Você precisa de exatamente 2 cartas do jogador")
            if len(cartasMesa) > 5:
                raise ValueError("A mesa pode ter no máximo 5 cartas")
            all_cards = cartasPlayer + cartasMesa
            if len(all_cards) != len(set(all_cards)):
                raise ValueError("Existem cartas duplicadas")

            probabilidade = calculateProb(cartasPlayer, cartasMesa, int(jogadores), 10000)

            st.write(f"Probabilidade de ganhar: {probabilidade[0]} %, de empatar: {probabilidade[1]} %")
            st.write(f"Os outros jogadores tem: {probabilidade[2]} % de probabilidade de ganhar")
            st.write(" ")
            if probabilidade[0] > probabilidade[2]:
                st.write("Voce tem a maior chance de ganhar! Vai com tudo!")
            st.write("Outs:")
            for out, chance in probabilidade[3].items():
                st.write(f"{out}: {round(chance, 2)} %")
        except Exception as e:
            st.error(f"Erro: {e}")

if st.button("Resetar"):
    st.session_state.cartasJogador = []
    st.session_state.cartasMesa = []
    st.session_state.detected = False
    if "claude_response" in st.session_state:
        del st.session_state.claude_response
    st.rerun()
