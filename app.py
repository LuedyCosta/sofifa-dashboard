import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Painel Tático Dinâmico", layout="wide")

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
      align-items: flex-start;
      min-height: 100vh;
      margin: 0;
      padding: 15px;
      box-sizing: border-box;
    }

    .painel-container {
      display: flex;
      gap: 20px;
      background: #1e1e1e;
      padding: 20px;
      border-radius: 8px;
      max-width: 1050px;
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
      flex-shrink: 0;
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
      gap: 12px;
    }

    .seletor-duplo {
      display: flex;
      gap: 10px;
    }

    .seletor-grupo {
      flex: 1;
      background: #2a2a2a;
      padding: 12px;
      border-radius: 6px;
    }

    .seletor-grupo label {
      display: block;
      margin-bottom: 6px;
      font-size: 13px;
      font-weight: bold;
    }

    .seletor-grupo select {
      width: 100%;
      padding: 8px;
      background: #333;
      color: #fff;
      border: 1px solid #555;
      border-radius: 4px;
      font-size: 13px;
    }

    .card-info {
      background: #2a2a2a;
      padding: 12px 15px;
      border-radius: 6px;
      border-left: 4px solid #3b82f6;
    }

    .card-info h3 { margin: 0 0 5px 0; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
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
      <div class="seletor-duplo">
        <div class="seletor-grupo">
          <label for="formacao-select">Formação:</label>
          <select id="formacao-select" onchange="atualizarPainel()">
            <option value="433-holding">4-3-3 Holding</option>
            <option value="442">4-4-2 Tradicional</option>
            <option value="352">3-5-2</option>
          </select>
        </div>

        <div class="seletor-grupo">
          <label for="preset-select">Tactical Preset:</label>
          <select id="preset-select" onchange="atualizarPainel()">
            <option value="padrao">Padrão (Standard)</option>
            <option value="pontas">Jogo pelas Pontas (Wing Play)</option>
            <option value="tikitaka">Tiki-Taka / Posse de Bola</option>
            <option value="contra-ataque">Contra-Ataque (Counter-Attack)</option>
            <option value="gegenpress">Gegenpressing / Pressão Alta</option>
            <option value="kick-rush">Chuta e Corre (Kick & Rush)</option>
            <option value="park-bus">Estacionar o Ônibus (Park the Bus)</option>
          </select>
        </div>
      </div>

      <div class="card-info" style="border-left-color: #3b82f6;">
        <h3 id="info-titulo">Explicação Breve</h3>
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

      <div class="card-info" style="border-left-color: #f59e0b;">
        <h3>Estratégia de Combate (Como Anular)</h3>
        <p id="info-combate">Carregando...</p>
      </div>
    </div>
  </div>

  <script>
    const formacoesPosicoes = {
      "433-holding": [
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
      ],
      "442": [
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
      ],
      "352": [
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
    };

    const analiseMatriz = {
      "433-holding": {
        "padrao": {
          desc: "Estrutura equilibrada com o volante assegurando a proteção defensiva enquanto o time alterna entre ataque cadenciado e pontas abertos.",
          pros: "Boa ocupação de espaço no campo inteiro e facilidade para ajustar a postura durante a partida.",
          contras: "Pode faltar agressividade ofensiva contra equipes muito retrancadas.",
          combate: "Pressionar a zona dos dois MCs para forçar o passe recuado para o volante e quebrar o ritmo de construção."
        },
        "pontas": {
          desc: "Os pontas (PE/PD) encostam na linha de fundo com apoio direto de LD e LE, usando o volante como pino de segurança.",
          pros: "Volume massivo de cruzamentos e isolamento 1v1 constante nos corredores laterais.",
          contras: "Espaço vago nas costas dos laterais se eles subirem ao mesmo tempo.",
          combate: "Dobrar a marcação nos pontas com lateral+volante e acionar transições rápidas nas costas dos laterais avançados."
        },
        "tikitaka": {
          desc: "Triangulações constantes entre Volante, MCs e Pontas para atrair o adversário e infiltrar pelo meio.",
          pros: "Controle absoluto da posse e desgaste físico/mental do adversário que tenta roubar a bola.",
          contras: "Risco de perdas no terço defensivo com a linha alta; falta de objetividade se o adversário fechar o meio.",
          combate: "Bloqueio médio-baixo bem compacto no centro e contra-ataques diretos assim que recuperar a bola."
        },
        "contra-ataque": {
          desc: "Linha de defesa e volante recuados; roubada de bola ativa passe rápido para a velocidade dos pontas e do centroavante.",
          pros: "Extremamente letal em espaço aberto e difícil de sofrer gols em ataque organizado.",
          contras: "Pouca retenção de bola e isolamento do CA caso os pontas demorem a recompor/subir.",
          combate: "Manter a 'contra-pressão' imediata no momento da perda da bola e não ceder espaço para a corrida dos pontas."
        },
        "gegenpress": {
          desc: "Os pontas e MCs sufocam a saída adversária no terço final, com o volante mantendo a linha alta perto da intermediária.",
          pros: "Recuperação de bola em zonas de perigo imediato, gerando chances claras com o rival desorganizado.",
          contras: "Enorme desgaste físico e risco iminente de bola longa nas costas dos dois zagueiros.",
          combate: "Usar ligação direta (Chuta e Corre) buscando o centroavante para ultrapassar a primeira linha de pressão."
        },
        "kick-rush": {
          desc: "Zagueiros e volante usam passes longos buscando a casquinha do CA ou o duelo individual dos pontas.",
          pros: "Anula completamente a pressão alta rival e coloca a bola na área em poucos segundos.",
          contras: "Aproveitamento baixo de posse de bola e dependência do ganho da segunda bola pelos MCs.",
          combate: "Impor superioridade física nos duelos aéreos com os zagueiros e posicionar volantes para recolher a segunda bola."
        },
        "park-bus": {
          desc: "Linha de 4 defensores + volante cimentados dentro da área, com pontas voltando como alas defensivos.",
          pros: "Dificuldade quase nula de conceder infiltrações pelo centro da área.",
          contras: "Incapacidade de sair para o jogo, atraindo ataque total do adversário por 90 minutos.",
          combate: "Chutes de longa/média distância para forçar rebotes e jogadas ensaiadas de escanteio/falta."
        }
      },
      "442": {
        "padrao": {
          desc: "Duas linhas de quatro compactas com dois atacantes trabalhando em dupla no setor ofensivo.",
          pros: "Fácil entendimento tático, cobertura completa da largura do campo e forte presença de área.",
          contras: "Pode ser inferiorizado numericamente contra trios de meio-campo rivais.",
          combate: "Explorar a superioridade numérica de 3 contra 2 no meio-campo usando entrelinhas."
        },
        "pontas": {
          desc: "Os meias laterais (MD/ME) e os laterais fazem dobradinhas para municiar a dupla de atacantes na área.",
          pros: "Aproveitamento máximo da presença de dois centroavantes para finalizar cruzamentos.",
          contras: "Corredor central fica desprotegido se os dois MCs não cobrirem os lados.",
          combate: "Dominar a zona central do campo e atacar por dentro explorando a distância entre os MCs e meias abertos."
        },
        "tikitaka": {
          desc: "Troca de passes curtos entre a dupla de zaga, MCs e meias abertos afunilando para tabelas com a dupla de ataque.",
          pros: "Gera linhas de passe curtas e apoios constantes em todas as zonas do campo.",
          contras: "Falta de pontas agudos para dar amplitude caso o adversário feche a área.",
          combate: "Fechamento compacto em bloco baixo e indução do jogo para as laterais onde o 4-4-2 perde profundidade."
        },
        "contra-ataque": {
          desc: "Linhas baixas e juntas; recuperação ativa lançamento imediato para a dupla de atacantes fazer a transição.",
          pros: "Muralha defensiva com duas linhas de 4 e apoio mútuo imediato na frente.",
          contras: "Gasto de energia enorme dos meias laterais para cobrir todo o corredor ida e volta.",
          combate: "Atacar com paciência, evitando cruzamentos precipitados e mantendo o balanço defensivo para interceptar a transição."
        },
        "gegenpress": {
          desc: "A dupla de ataque e meias pressionam a saída do adversário em bloco alto e coordenado.",
          pros: "Sufoca defesas com dois zagueiros e força o erro ainda dentro da grande área rival.",
          contras: "Deixa grande espaço entre a linha de defesa e a linha de meio caso a pressão falhe.",
          combate: "Giro rápido de bola com passe na diagonal para o lateral oposto desmarcado."
        },
        "kick-rush": {
          desc: "Ligação direta do goleiro ou zagueiros para um dos atacantes disputar no alto e o outro rasgar em velocidade.",
          pros: "Aproveita a presença de dois atacantes para ganhar bolas divididas no campo ofensivo.",
          contras: "Jogo feio e desconectado, pouca criação técnica pelo meio-campo.",
          combate: "Manter zagueiros firmes no jogo aéreo e sobressair o controle da bola no chão ao recuperar."
        },
        "park-bus": {
          desc: "Duas linhas de 4 completamente afuniladas no próprio terço com atacantes recuados até a intermediária.",
          pros: "Atrancamento total das rotas centrais e das pontas na intermediária defensiva.",
          contras: "Presença nula no campo de ataque, aceitando a pressão contínua do adversário.",
          combate: "Circulação rápida de bola de um lado para o outro para desestabilizar as linhas e triangulações rápidas."
        }
      },
      "352": {
        "padrao": {
          desc: "Três zagueiros protegem o centro enquanto alas cobrem o corredor inteiro e o meio-campo ganha corpo.",
          pros: "Domínio numérico no meio-campo e forte densidade dentro da própria área.",
          contras: "Espaços vulneráveis nas costas dos alas quando ambos sobem.",
          combate: "Explorar os espaços deixados pelos alas com pontas rápidos e inversões de jogo."
        },
        "pontas": {
          desc: "Os alas (ALA) atuam como autênticos pontas, contando com o apoio dos zagueiros das pontas da sobra defensiva.",
          pros: "Amplitude total com sobreposição e excelente volume de bolas alçadas na área.",
          contras: "Sobrecarga física extrema nos alas e exposição dos zagueiros de lado no 1v1.",
          combate: "Atacar diretamente os zagueiros dos lados com atacantes velozes quando o ala estiver adiantado."
        },
        "tikitaka": {
          desc: "Construção desde a zaga com 3 defensores e triangulações envolventes com os volantes e o MC.",
          pros: "Superioridade numérica fácil na saída de bola (3 zagueiros + volantes) contra qualquer pressão.",
          contras: "Lentidão se a bola não chegar rapidamente aos dois atacantes.",
          combate: "Pressionar alto com três atacantes para igualar o 3v3 na saída de bola dos zagueiros."
        },
        "contra-ataque": {
          desc: "Os alas fecham numa linha de 5 defensores sem a bola; roubada ativa transição direta para os 2 atacantes.",
          pros: "Inviolável por dentro e transição com superioridade no meio de campo.",
          contras: "Distância muito grande entre a linha defensiva de 5 e a dupla de ataque.",
          combate: "Rodar a bola na intermediária sem pressa e utilizar chutes de fora para atrair os zagueiros."
        },
        "gegenpress": {
          desc: "Meio-campo encorpadíssimo com 5 jogadores mordendo em cima e linha de 3 zagueiros na altura da metade do campo.",
          pros: "Domínio físico assustador e sufocamento total no meio-campo.",
          contras: "Um passe vertical certo do adversário quebra 5 jogadores de uma vez.",
          combate: "Usar passes verticais rápidos 'quebra-linhas' diretamente para atacantes abertos no mano a mano."
        },
        "kick-rush": {
          desc: "Zagueiros usam o corredor central livre para lançar diretamente nos dois centroavantes físicos.",
          pros: "Simplicidade e objetividade aproveitando a densidade ofensiva na frente.",
          contras: "Desaproveitamento da qualidade técnica dos volantes e MC no meio-campo.",
          combate: "Atrair a bola longa e dominar as sobras com três volantes ou meio-campo povoado."
        },
        "park-bus": {
          desc: "Formação de linha defensiva de 5 jogadores + 3 volantes bloqueando a entrada da grande área.",
          pros: "Muralha praticamente intransponível para finalizações de dentro da área.",
          contras: "Falta de válvula de escape; extrema passividade diante do rival.",
          combate: "Movimentação intensa sem bola para tirar zagueiros de posição e arremates de média distância."
        }
      }
    };

    function atualizarPainel() {
      const formacao = document.getElementById("formacao-select").value;
      const preset = document.getElementById("preset-select").value;

      // Atualiza Jogadores no Campo
      const campo = document.getElementById("campo");
      const jogadoresAntigos = campo.querySelectorAll(".jogador");
      jogadoresAntigos.forEach(j => j.remove());

      const posicoes = formacoesPosicoes[formacao];
      posicoes.forEach(j => {
        const div = document.createElement("div");
        div.className = "jogador";
        div.style.top = j.top + "%";
        div.style.left = j.left + "%";
        div.innerText = j.pos;
        div.title = j.pos;
        campo.appendChild(div);
      });

      // Atualiza Cards de Análise
      const dados = analiseMatriz[formacao][preset];
      document.getElementById("info-descricao").innerText = dados.desc;
      document.getElementById("info-pros").innerText = dados.pros;
      document.getElementById("info-contras").innerText = dados.contras;
      document.getElementById("info-combate").innerText = dados.combate;
    }

    window.onload = atualizarPainel;
  </script>
</body>
</html>
"""

components.html(painel_tatico_html, height=520, scrolling=True)
