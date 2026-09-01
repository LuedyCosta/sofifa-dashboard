<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel Tático</title>
  <style>
    body {
      background-color: #121212;
      color: #ffffff;
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }

    .painel-container {
      display: flex;
      gap: 20px;
      background: #1e1e1e;
      padding: 20px;
      border-radius: 8px;
      max-width: 900px;
      width: 100%;
    }

    /* Correção da Proporção do Campo (Horizontal) */
    .campo-futebol {
      width: 100%;
      max-width: 500px;
      aspect-ratio: 105 / 68; /* Proporção oficial aproximada de um campo */
      background-color: #1b4d3e;
      position: relative;
      border: 2px solid white;
      border-radius: 4px;
      overflow: hidden;
    }

    /* Linhas e marcações do campo */
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

    .grande-area-esq {
      left: 0;
      border-left: none;
    }

    .grande-area-dir {
      right: 0;
      border-right: none;
    }

    /* Marcadores dos Jogadores */
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
      cursor: pointer;
      transition: transform 0.2s;
    }

    .jogador:hover {
      transform: translate(-50%, -50%) scale(1.15);
      background-color: #f0f0f0;
      z-index: 10;
    }

    .informacoes {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 15px;
    }

    .card-info {
      background: #2a2a2a;
      padding: 15px;
      border-radius: 6px;
      border-left: 4px solid #3b82f6;
    }

    .card-info h3 {
      margin: 0 0 8px 0;
      font-size: 14px;
    }

    .card-info p {
      margin: 0;
      font-size: 13px;
      color: #ccc;
      line-height: 1.4;
    }
  </style>
</head>
<body>

  <div class="painel-container">
    <!-- Campo com Proporção Ajustada e Jogadores Posicionados -->
    <div class="campo-futebol">
      <div class="linha-meio"></div>
      <div class="circulo-central"></div>
      <div class="grande-area-esq"></div>
      <div class="grande-area-dir"></div>

      <!-- Jogadores (4-3-3 Holding) -->
      <!-- Goleiro -->
      <div class="jogador" style="top: 50%; left: 6%;" title="Goleiro (GOL)">G</div>
      
      <!-- Defesa -->
      <div class="jogador" style="top: 15%; left: 25%;" title="Lateral Direito (LD)">LD</div>
      <div class="jogador" style="top: 38%; left: 20%;" title="Zagueiro (ZAG)">ZAG</div>
      <div class="jogador" style="top: 62%; left: 20%;" title="Zagueiro (ZAG)">ZAG</div>
      <div class="jogador" style="top: 85%; left: 25%;" title="Lateral Esquerdo (LE)">LE</div>

      <!-- Meio-Campo (Holding / Volante + 2 Meias) -->
      <div class="jogador" style="top: 50%; left: 38%;" title="Volante (VOL)">VOL</div>
      <div class="jogador" style="top: 30%; left: 55%;" title="Meia Esquerda (MC)">MC</div>
      <div class="jogador" style="top: 70%; left: 55%;" title="Meia Direita (MC)">MC</div>

      <!-- Ataque -->
      <div class="jogador" style="top: 15%; left: 78%;" title="Ponta Esquerda (ATA)">PE</div>
      <div class="jogador" style="top: 50%; left: 82%;" title="Centroavante (ATA)">CA</div>
      <div class="jogador" style="top: 85%; left: 78%;" title="Ponta Direita (ATA)">PD</div>
    </div>

    <!-- Bloco de Informações da Formação -->
    <div class="informacoes">
      <div class="card-info">
        <h3>Informações da Formação (4-3-3 Holding)</h3>
        <p>Variação defensiva do 4-3-3 com um volante fixo protegendo a zaga e dois meias interiores armando o jogo.</p>
      </div>
      <div class="card-info" style="border-left-color: #10b981;">
        <h3>Vantagens (Prós)</h3>
        <p>Excelente equilíbrio na transição defensiva e proteção contra contra-ataques.</p>
      </div>
      <div class="card-info" style="border-left-color: #ef4444;">
        <h3>Desvantagens (Contras)</h3>
        <p>Pode pecar em volume ofensivo caso os meias interiores não avancem com frequência.</p>
      </div>
    </div>
  </div>

</body>
</html>
