import streamlit as st
import random

GRID_HEIGHT = 13
GRID_WIDTH = 10

TETROMINOS = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
}

def create_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def create_tetromino():
    shape = random.choice(list(TETROMINOS.values()))
    return {"shape": shape, "x": 3, "y": 0}

def place_tetromino(grid, tetromino):
    temp_grid = [row.copy() for row in grid]
    shape = tetromino["shape"]
    x = tetromino["x"]
    y = tetromino["y"]

    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell and 0 <= y + i < GRID_HEIGHT and 0 <= x + j < GRID_WIDTH:
                temp_grid[y + i][x + j] = 1
    return temp_grid

def draw_grid(grid):
    html = "<div style='display: grid; grid-template-columns: repeat({}, 20px); gap: 2px; justify-content: center;'>".format(GRID_WIDTH)
    for row in grid:
        for cell in row:
            color = "#facc15" if cell else "#1e293b"
            html += f"<div style='width: 20px; height: 20px; background-color: {color}; border-radius: 4px;'></div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="🎮 Tetris Game", layout="wide")

    st.markdown("""
        <style>
            html, body, [data-testid="stApp"] {
                height: 100vh;
                margin: 0;
                padding: 0;
                background-color: #0f172a;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            h1, p {
                color: white;
                text-align: center;
            }
            .button-row {
                display: flex;
                justify-content: center;
                gap: 1rem;
                margin-top: 1rem;
                flex-wrap: wrap;
            }
            button {
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>🎮 Simple Tetris</h1>", unsafe_allow_html=True)
    st.markdown("<p>Made by Sidra Raza</p>", unsafe_allow_html=True)

    if "grid" not in st.session_state:
        st.session_state.grid = create_grid()
        st.session_state.tetromino = create_tetromino()

    grid = st.session_state.grid
    tetro = st.session_state.tetromino

    temp_grid = place_tetromino(grid, tetro)
    draw_grid(temp_grid)

    # Buttons in a horizontal line
    st.markdown('<div class="button-row">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⬅️ Left"):
            tetro["x"] = max(0, tetro["x"] - 1)
    with col2:
        if st.button("➡️ Right"):
            tetro["x"] = min(GRID_WIDTH - len(tetro["shape"][0]), tetro["x"] + 1)
    with col3:
        if st.button("⬇️ Down"):
            tetro["y"] = min(GRID_HEIGHT - len(tetro["shape"]), tetro["y"] + 1)
    with col4:
        if st.button("🔄 Rotate"):
            rotated = list(zip(*reversed(tetro["shape"])))
            if tetro["x"] + len(rotated[0]) <= GRID_WIDTH and tetro["y"] + len(rotated) <= GRID_HEIGHT:
                tetro["shape"] = rotated

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔁 Restart Game"):
        st.session_state.grid = create_grid()
        st.session_state.tetromino = create_tetromino()
        st.experimental_rerun()

if __name__ == "__main__":
    main()
