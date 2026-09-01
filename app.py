import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Painel Tático", layout="wide")

painel_tatico_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel Tático Dinâmico</title>
  <style>
    body {
      background-color: #121212;
      color: #ffffff;
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      padding: 10px;
      box-sizing: border-box;
    }

    .painel-container {
      display: flex;
      gap: 20px;
      background: #1e1e1e;
      padding: 20px;
      border-radius: 8px;
      max-width: 950px;
      width: 100%;
    }

    .campo-futebol {
      width: 100%;
      max-width: 500px;
      aspect-ratio: 105 / 68;
      background-color: #1b4d3e;
      position: relative;
      border: 2px solid white;
      border-radius: 4px;
      overflow: hidden;
    }

    .linha-meio {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 50%;
      border-left: 2px dashed rgba(255, 255, 255, 0.7);
    }

    .circulo-central {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 20%;
      aspect-ratio: 1 / 1;
      border: 2px solid rgba(255, 255, 255, 0.7);
      border-radius: 50%;
      transform: translate(-50%, -50%);
    }

    .grande-area-esq, .grande-area-dir {
      position: absolute;
      top: 20%;
      bottom: 20%;
      width: 15%;
      border: 2px solid rgba(255, 255, 255, 0.7);
    }

    .grande-area-esq { left: 0; border-left: none; }
    .grande-area-dir { right: 0; border-right: none; }

    .jogador {
      position: absolute;
      transform: translate(-50%, -50%);
      width: 28px;
      height: 28px;
      background-color: #ffffff;
      color: #000;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 10px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.4);
      transition: all 0.3s ease-in-out;
    }

    .informacoes {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 15px;
    }

    .seletor-grupo {
      background: #2a2a2a;
      padding: 15px;
      border-radius: 6px;
    }

    .seletor-grupo label {
      display: block;
      margin-bottom: 8px;
      font-size: 14px;
      font-weight: bold;
    }

    .seletor-grupo select {
      width: 100%;
      padding: 8px;
      background: #333;
      color: #fff;
      border: 1px solid #555;
      border-radius: 4px;
      font-size: 14px;
    }

    .card-info {
      background: #2a2a2a;
      padding: 15px;
      border-radius: 6px;
      border-left: 4px solid #3b82f6;
    }

    .card-info h3 { margin: 0 0 8px 0; font-size: 14px; }
    .card-info p { margin: 0; font-size: 13px; color: #ccc; line-height: 1.4; }
  </style>
</head>
<body>

  <div class="painel-container">
    <!-- Campo de Futebol -->
    <div class="campo-futebol" id="campo">
      <div class="linha-meio"></div>
      <div class="circulo-central"></div>
      <div class="grande-area-esq"></div>
      <div class="grande-area-dir"></div>
    </div>

    <!-- Bloco de Controles e Informações -->
    <div class="informacoes">
      <div class="seletor-grupo">
        <label for="formacao-select">Escolha a Formação:</label>
        <select id="formacao-select" onchange="mudarFormacao()">
          <option value="433-holding">4-3-3 Holding</option>
          <option value="442">4-4-2 Tradicional</option>
          <option value="352">3-5-2</option>
        </select>
      </div>

      <div class="card-info">
        <h3 id="info-titulo">Informações da Formação</h3>
        <p id="info-descricao">Carregando...</p>
      </div>
      <div class="card-info" style="border-left-color: #10b981;">
        <h3>Vantagens (Prós)</h3>
        <p id="info-pros">Carregando...</p>
      </div>
      <div class="card-info" style="border-left-color: #ef4444;">
        <h3>Desvantagens (Contras)</h3>
        <p id="info-contras">Carregando...</p>
      </div>
    </div>
  </div>

  <script>
    const formacoes = {
      "433-holding": {
        titulo: "Informações da Formação (4-3-3 Holding)",
        descricao: "Variação defensiva do 4-3-3 com um volante fixo protegendo a zaga e dois meias interiores armando o jogo.",
        pros: "Excelente equilíbrio na transição defensiva e proteção contra contra-ataques.",
        contras: "Pode pecar em volume ofensivo caso os meias interiores não avancem com frequência.",
        jogadores: [
          { pos: "GOL", top: 50, left: 6 },
          { pos: "LD",  top: 15, left: 25 },
          { pos: "ZAG", top: 38, left: 20 },
          { pos: "ZAG", top: 62, left: 20 },
          { pos: "LE",  top: 85, left: 25 },
          { pos: "VOL", top: 50, left: 38 },
          { pos: "MC",  top: 30, left: 55 },
          { pos: "MC",  top: 70, left: 55 },
          { pos: "PE",  top: 15, left: 78 },
          { pos: "CA",  top: 50, left: 82 },
          { pos: "PD",  top: 85, left: 78 }
        ]
      },
      "442": {
        titulo: "Informações da Formação (4-4-2 Tradicional)",
        descricao: "Esquema clássico e equilibrado, com duas linhas de quatro jogadores e dupla de ataque fixa.",
        pros: "Fácil compactação defensiva e forte presença física no meio-campo e ataque.",
        contras: "Pode sofrer contra times que acumulam muitos jogadores no meio de campo (ex: superioridade numérica).",
        jogadores: [
          { pos: "GOL", top: 50, left: 6 },
          { pos: "LD",  top: 15, left: 25 },
          { pos: "ZAG", top: 38, left: 20 },
          { pos: "ZAG", top: 62, left: 20 },
          { pos: "LE",  top: 85, left: 25 },
          { pos: "MD",  top: 15, left: 50 },
          { pos: "MC",  top: 38, left: 45 },
          { pos: "MC",  top: 62, left: 45 },
          { pos: "ME",  top: 85, left: 50 },
          { pos: "ATA", top: 38, left: 78 },
          { pos: "ATA", top: 62, left: 78 }
        ]
      },
      "352": {
        titulo: "Informações da Formação (3-5-2)",
        descricao: "Formação ofensiva que utiliza três zagueiros e alas muito agressivos pelo lado do campo.",
        pros: "Excelente controle do meio-campo e superioridade numérica no ataque.",
        contras: "Espaços nas costas dos alas podem ser explorados por pontas rápidos adversários.",
        jogadores: [
          { pos: "GOL", top: 50, left: 6 },
          { pos: "ZAG", top: 25, left: 20 },
          { pos: "ZAG", top: 50, left: 18 },
          { pos: "ZAG", top: 75, left: 20 },
          { pos: "ALA", top: 10, left: 50 },
          { pos: "VOL", top: 38, left: 40 },
          { pos: "MC",  top: 50, left: 55 },
          { pos: "VOL", top: 62, left: 40 },
          { pos: "ALA", top: 90, left: 50 },
          { pos: "ATA", top: 35, left: 80 },
          { pos: "ATA", top: 65, left: 80 }
        ]
      }
    };

    function mudarFormacao() {
      const select = document.getElementById("formacao-select");
      const chave = select.value;
      const dados = formacoes[chave];

      document.getElementById("info-titulo").innerText = dados.titulo;
      document.getElementById("info-descricao").innerText = dados.descricao;
      document.getElementById("info-pros").innerText = dados.pros;
      document.getElementById("info-contras").innerText = dados.contras;

      const campo = document.getElementById("campo");
      const jogadoresAntigos = campo.querySelectorAll(".jogador");
      jogadoresAntigos.forEach(j => j.remove());

      dados.jogadores.forEach(j => {
        const div = document.createElement("div");
        div.className = "jogador";
        div.style.top = j.top + "%";
        div.style.left = j.left + "%";
        div.innerText = j.pos;
        div.title = j.pos;
        campo.appendChild(div);
      });
    }

    window.onload = mudarFormacao;
  </script>
</body>
</html>
"""

components.html(painel_tatico_html, height=450, scrolling=True)
