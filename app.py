import streamlit as st
import streamlit.components.v1 as components

from database import save_score, get_ranking


st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="centered"
)


# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        max-width: 900px;
        margin: auto;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 25px;
    }

    .ranking-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-top: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="title">🐍 Snake Game</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">먹이를 먹고 최고 점수에 도전하세요!</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Player name
# -----------------------------
player_name = st.text_input(
    "플레이어 이름",
    value="Player",
    max_chars=20
)


if not player_name.strip():
    player_name = "Player"


# -----------------------------
# JavaScript Snake Game
# -----------------------------
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    background: #ffffff;
    font-family: Arial, sans-serif;
}

.game-container {
    width: 100%;
    max-width: 600px;
    margin: auto;
    text-align: center;
}

.info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    font-size: 20px;
    font-weight: bold;
}

canvas {
    border: 4px solid #222;
    background: #111;
    width: 100%;
    max-width: 500px;
    height: auto;
    display: block;
    margin: auto;
}

button {
    margin-top: 15px;
    padding: 10px 22px;
    border: none;
    border-radius: 8px;
    background: #28a745;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    background: #218838;
}

.help {
    margin-top: 12px;
    color: #666;
    font-size: 14px;
}

.game-over {
    color: #dc3545;
    font-size: 24px;
    font-weight: bold;
    margin-top: 10px;
}

</style>

</head>

<body>

<div class="game-container">

    <div class="info">
        <div>점수: <span id="score">0</span></div>
        <div>최고점수: <span id="highScore">0</span></div>
    </div>

    <canvas id="gameCanvas" width="500" height="500"></canvas>

    <div id="message"></div>

    <button onclick="restartGame()">
        다시 시작
    </button>

    <div class="help">
        ⬆️ ⬇️ ⬅️ ➡️ 방향키로 이동하세요
    </div>

</div>


<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const gridSize = 20;
const tileCount = canvas.width / gridSize;

let snake;
let food;

let dx;
let dy;

let score = 0;
let highScore = 0;

let gameRunning = true;

let gameLoop;


function loadHighScore() {

    const saved = localStorage.getItem("snakeHighScore");

    if (saved) {
        highScore = parseInt(saved);
    }

    document.getElementById("highScore").innerText = highScore;
}


function initializeGame() {

    snake = [
        { x: 10, y: 10 },
        { x: 9, y: 10 },
        { x: 8, y: 10 }
    ];

    dx = 1;
    dy = 0;

    score = 0;

    gameRunning = true;

    document.getElementById("score").innerText = score;
    document.getElementById("message").innerHTML = "";

    createFood();

    if (gameLoop) {
        clearInterval(gameLoop);
    }

    gameLoop = setInterval(updateGame, 120);
}


function createFood() {

    let validPosition = false;

    while (!validPosition) {

        food = {
            x: Math.floor(Math.random() * tileCount),
            y: Math.floor(Math.random() * tileCount)
        };

        validPosition = true;

        for (let part of snake) {

            if (
                part.x === food.x &&
                part.y === food.y
            ) {
                validPosition = false;
                break;
            }
        }
    }
}


function updateGame() {

    if (!gameRunning) {
        return;
    }

    const head = {
        x: snake[0].x + dx,
        y: snake[0].y + dy
    };


    // 벽 충돌
    if (
        head.x < 0 ||
        head.x >= tileCount ||
        head.y < 0 ||
        head.y >= tileCount
    ) {
        endGame();
        return;
    }


    // 자기 몸 충돌
    for (let i = 0; i < snake.length; i++) {

        if (
            head.x === snake[i].x &&
            head.y === snake[i].y
        ) {
            endGame();
            return;
        }
    }


    snake.unshift(head);


    // 먹이
    if (
        head.x === food.x &&
        head.y === food.y
    ) {

        score += 10;

        document.getElementById("score").innerText = score;

        if (score > highScore) {

            highScore = score;

            localStorage.setItem(
                "snakeHighScore",
                highScore
            );

            document.getElementById(
                "highScore"
            ).innerText = highScore;
        }

        createFood();

    } else {

        snake.pop();

    }

    drawGame();
}


function drawGame() {

    // 배경
    ctx.fillStyle = "#111";
    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // 격자
    ctx.strokeStyle = "#222";

    for (let i = 0; i <= tileCount; i++) {

        ctx.beginPath();

        ctx.moveTo(
            i * gridSize,
            0
        );

        ctx.lineTo(
            i * gridSize,
            canvas.height
        );

        ctx.stroke();


        ctx.beginPath();

        ctx.moveTo(
            0,
            i * gridSize
        );

        ctx.lineTo(
            canvas.width,
            i * gridSize
        );

        ctx.stroke();
    }


    // 먹이
    ctx.fillStyle = "#ff3333";

    ctx.beginPath();

    ctx.arc(
        food.x * gridSize + gridSize / 2,
        food.y * gridSize + gridSize / 2,
        gridSize / 2 - 2,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // 뱀
    snake.forEach((part, index) => {

        if (index === 0) {
            ctx.fillStyle = "#00ff66";
        } else {
            ctx.fillStyle = "#00cc55";
        }

        ctx.fillRect(
            part.x * gridSize + 1,
            part.y * gridSize + 1,
            gridSize - 2,
            gridSize - 2
        );
    });
}


function changeDirection(newDx, newDy) {

    // 반대 방향으로 바로 이동하는 것 방지

    if (
        newDx === -dx &&
        newDy === -dy
    ) {
        return;
    }

    dx = newDx;
    dy = newDy;
}


document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "ArrowUp") {

            event.preventDefault();

            changeDirection(0, -1);

        } else if (event.key === "ArrowDown") {

            event.preventDefault();

            changeDirection(0, 1);

        } else if (event.key === "ArrowLeft") {

            event.preventDefault();

            changeDirection(-1, 0);

        } else if (event.key === "ArrowRight") {

            event.preventDefault();

            changeDirection(1, 0);
        }
    }
);


function endGame() {

    gameRunning = false;

    clearInterval(gameLoop);

    document.getElementById(
        "message"
    ).innerHTML =
        '<div class="game-over">GAME OVER</div>';

    // Streamlit 부모 페이지로 점수 전달
    window.parent.postMessage(
        {
            type: "snake_game_score",
            score: score
        },
        "*"
    );
}


function restartGame() {

    initializeGame();

    drawGame();
}


loadHighScore();

initializeGame();

drawGame();

</script>

</body>
</html>
"""


components.html(
    game_html,
    height=620,
    scrolling=False
)


# -----------------------------
# Ranking
# -----------------------------
st.markdown(
    '<div class="ranking-title">🏆 TOP 10 랭킹</div>',
    unsafe_allow_html=True
)

ranking = get_ranking()


if ranking:

    for index, row in enumerate(ranking, start=1):

        name = row["name"]
        score = row["score"]
        created_at = row["created_at"]

        if index == 1:
            medal = "🥇"
        elif index == 2:
            medal = "🥈"
        elif index == 3:
            medal = "🥉"
        else:
            medal = f"{index}."

        st.write(
            f"**{medal} {name} — {score}점**  "
            f"({created_at})"
        )

else:

    st.info(
        "아직 등록된 점수가 없습니다. "
        "첫 번째 기록을 만들어 보세요!"
    )


st.divider()

st.caption(
    "Snake Game · Streamlit + SQLite"
)
