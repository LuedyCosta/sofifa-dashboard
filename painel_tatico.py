import streamlit as st
import streamlit.components.v1 as components

def renderizar_painel_tatico():
    st.title("📋 Guia de Formações & Tactical Presets (FC26)")
    st.markdown("Analise a disposição tática em campo, os estilos de construção de jogada e as estratégias completas extraídas da análise avançada.")

    painel_html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <style>
        body { background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; display: flex; justify-content: center; margin: 0; padding: 10px; }
        .painel-container { display: flex; gap: 20px; background: #1e1e1e; padding: 20px; border-radius: 8px; max-width: 950px; width: 100%; box-sizing: border-box; }
        .campo-futebol { width: 100%; max-width: 450px; aspect-ratio: 105 / 68; background-color: #1b4d3e; position: relative; border: 2px solid white; border-radius: 4px; overflow: hidden; flex-shrink: 0; }
        .linha-meio { position: absolute; top: 0; bottom: 0; left: 50%; border-left: 2px dashed rgba(255, 255, 255, 0.7); }
        .circulo-central { position: absolute; top: 50%; left: 50%; width: 20%; aspect-ratio: 1/1; border: 2px solid rgba(255, 255, 255, 0.7); border-radius: 50%; transform: translate(-50%, -50%); }
        .grande-area-esq, .grande-area-dir { position: absolute; top: 20%; bottom: 20%; width: 15%; border: 2px solid rgba(255, 255, 255, 0.7); }
        .grande-area-esq { left: 0; border-left: none; }
        .grande-area-dir { right: 0; border-right: none; }
        .jogador { position: absolute; transform: translate(-50%, -50%); width: 26px; height: 26px; background-color: #ffffff; color: #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 8px; transition: all 0.3s ease-in-out; }
        .informacoes { flex: 1; display: flex; flex-direction: column; gap: 10px; }
        .seletor-duplo { display: flex; gap: 10px; }
        .seletor-grupo { flex: 1; background: #2a2a2a; padding: 10px; border-radius: 6px; }
        .seletor-grupo label { display: block; margin-bottom: 4px; font-size: 12px; font-weight: bold; }
        .seletor-grupo select { width: 100%; padding: 6px; background: #333; color: #fff; border: 1px solid #555; border-radius: 4px; font-size: 12px; }
        .card-info { background: #2a2a2a; padding: 10px 12px; border-radius: 6px; border-left: 4px solid #3b82f6; }
        .card-info h3 { margin: 0 0 4px 0; font-size: 12px; text-transform: uppercase; }
        .card-info p { margin: 0; font-size: 12px; color: #ccc; line-height: 1.3; }
      </style>
    </head>
    <body>
      <div class="painel-container">
        <div class="campo-futebol" id="campo">
          <div class="linha-meio"></div>
          <div class="circulo-central"></div>
          <div class="grande-area-esq"></div>
          <div class="grande-area-dir"></div>
        </div>
        <div class="informacoes">
          <div class="seletor-duplo">
            <div class="seletor-grupo">
              <label for="formacao-select">Formação:</label>
              <select id="formacao-select" onchange="atualizarPainel()">
                <option value="433-false9">4-3-3 False 9</option>
                <option value="4312">4-3-1-2</option>
                <option value="424">4-2-4</option>
                <option value="4321">4-3-2-1</option>
                <option value="541-flat">5-4-1 Flat</option>
                <option value="532">5-3-2</option>
              </select>
            </div>
            <div class="seletor-grupo">
              <label for="preset-select">Tactical Preset:</label>
              <select id="preset-select" onchange="atualizarPainel()">
                <option value="tikitaka">Tiki-Taka / Posse</option>
                <option value="short-passing">Short Passing / Posse Estéril</option>
                <option value="gegenpress">Gegenpress / Pressão Pós-Perda</option>
                <option value="heavy-metal">Heavy Metal Counter / Transição Vertical</option>
                <option value="park-bus">Park the Bus (Estacionar o Ônibus)</option>
                <option value="counter">Counter-Attack Retrancado</option>
              </select>
            </div>
          </div>
          <div class="card-info" style="border-left-color: #3b82f6;"><h3>Explicação Breve</h3><p id="info-descricao">-</p></div>
          <div class="card-info" style="border-left-color: #10b981;"><h3>Vantagens (Prós)</h3><p id="info-pros">-</p></div>
          <div class="card-info" style="border-left-color: #ef4444;"><h3>Desvantagens (Contras)</h3><p id="info-contras">-</p></div>
          <div class="card-info" style="border-left-color: #f59e0b;"><h3>Como Jogar Contra</h3><p id="info-combate">-</p></div>
        </div>
      </div>
      <script>
        const posicoes = {
          "433-false9": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:50,l:40},{p:"MC",t:32,l:53},{p:"MC",t:68,l:53},{p:"PE",t:15,l:75},{p:"F9",t:50,l:68},{p:"PD",t:85,l:75}],
          "4312": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"MC",t:30,l:45},{p:"MC",t:50,l:40},{p:"MC",t:70,l:45},{p:"MEI",t:50,l:62},{p:"ATA",t:38,l:80},{p:"ATA",t:62,l:80}],
          "424": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"MC",t:38,l:45},{p:"MC",t:62,l:45},{p:"PE",t:15,l:78},{p:"ATA",t:38,l:82},{p:"ATA",t:62,l:82},{p:"PD",t:85,l:78}],
          "4321": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"MC",t:28,l:45},{p:"MC",t:50,l:40},{p:"MC",t:72,l:45},{p:"MEI",t:35,l:65},{p:"MEI",t:65,l:65},{p:"ATA",t:50,l:82}],
          "541-flat": [{p:"GOL",t:50,l:6},{p:"ALA",t:10,l:25},{p:"ZAG",t:28,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:72,l:20},{p:"ALA",t:90,l:25},{p:"ME",t:15,l:50},{p:"MC",t:38,l:48},{p:"MC",t:62,l:48},{p:"MD",t:85,l:50},{p:"ATA",t:50,l:80}],
          "532": [{p:"GOL",t:50,l:6},{p:"ALA",t:10,l:25},{p:"ZAG",t:28,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:72,l:20},{p:"ALA",t:90,l:25},{p:"MC",t:30,l:48},{p:"MC",t:50,l:45},{p:"MC",t:70,l:48},{p:"ATA",t:38,l:78},{p:"ATA",t:62,l:78}]
        };

        const matriz = {
          "433-false9": {
            "tikitaka": {
              d: "O centroavante recua para a zona de armação (fazendo o papel de falso 9), atraindo a zaga adversária e abrindo o corredor central para a infiltração em diagonal dos pontas (LW/RW).",
              p: "Superioridade numérica constante no meio-campo, posse de bola sufocante e extrema dificuldade para o adversário encaixar a marcação individual.",
              c: "Falta de presença física na área em cruzamentos tradicionais; exige jogadores com altíssimo índice de passe e visão de jogo.",
              b: "Utilize uma linha defensiva profunda e marque por zona com um volante fixo (estilo 4-2-3-1). Não permita que seus zagueiros abandonem a linha defensiva para perseguir o falso 9."
            }
          },
          "4312": {
            "short-passing": {
              d: "Compactação máxima no corredor central, unindo um losango de meias a uma dupla de ataque dinâmica focada em passes de curto alcance.",
              p: "Trocas de passes rápidas e imprevisíveis na entrada da área rival, gerando tabelas curtas imparáveis quando encaixadas.",
              c: "Zero amplitude ofensiva natural. A equipe sofre imensamente contra defesas que fecham o meio.",
              b: "Jogue com formações abertas (como um 4-4-2 ou 4-2-3-1 Wide) e force o adversário a jogar pelas laterais, onde ele não tem opções de profundidade."
            }
          },
          "424": {
            "gegenpress": {
              d: "Quatro jogadores na linha de frente sufocando a saída de bola do adversário em bloco alto, apoiados por transições verticais rápidas.",
              p: "Pressão sufocante que induz o adversário ao erro na defesa, gerando chances claras de gol logo após a roubada.",
              c: "Desorganização crônica do meio-campo. Apenas dois jogadores protegem a transição defensiva, abrindo enormes buracos.",
              b: "Atraia a pressão tocando a bola de pé em pé com calma na defesa e lance imediatamente bolas longas nas costas dos alas/laterais que sobem em desespero."
            }
          },
          "4321": {
            "heavy-metal": {
              d: "O meta competitivo por excelência. Dois meias atacantes fechados funcionam como foguetes acionados instantaneamente após a recuperação da posse.",
              p: "Velocidade letal na transição, compactação defensiva sólida em bloco médio e infiltrações imprevisíveis por dentro.",
              c: "Requer controle manual impecável para não perder o corredor lateral quando o adversário cria largura.",
              b: "Feche o centro com um duplo pivô rigoroso e use laterais com instruções de não subir ao mesmo tempo para conter os meias infiltrais."
            }
          },
          "541-flat": {
            "park-bus": {
              d: "Bloco super compacto com uma linha defensiva de cinco e uma linha de quatro logo à frente, anulando totalmente a profundidade rival.",
              p: "Impenetrável por dentro, privando o adversário de qualquer espaço para finalizações limpas na grande área.",
              c: "Ofensivamente estéril. Praticamente não há jogadores no campo de ataque para construir contra-ataques estruturados.",
              b: "Tenha paciência na circulação de bola, utilize chutes de longa distância (Power Shots) e explore cruzamentos venenosos com alas abertos para forçar erros de desatenção."
            }
          },
          "532": {
            "counter": {
              d: "Três zagueiros protegidos por um trio de meio-campo e dois alas que fecham a casinha, contando com dois atacantes rápidos isolados na frente.",
              p: "Excelente equilíbrio entre fechar os espaços defensivos e ter uma dupla de escape veloz para puxar contragolpes.",
              c: "Vulnerável ao controle de posse prolongado no campo defensivo do adversário, sofrendo com o desgaste físico dos alas.",
              b: "Mantenha a linha defensiva alta para impedir que os atacantes recebam lançamentos livres e use pressão pós-perda para sufocar a saída deles."
            }
          }
        };

        const presetRecomendado = {
          "433-false9": "tikitaka",
          "4312": "short-passing",
          "424": "gegenpress",
          "4321": "heavy-metal",
          "541-flat": "park-bus",
          "532": "counter"
        };

        function atualizarPainel() {
          const f = document.getElementById("formacao-select").value;
          let p = document.getElementById("preset-select").value;
          
          if (!matriz[f][p]) {
            p = presetRecomendado[f];
            document.getElementById("preset-select").value = p;
          }

          const campo = document.getElementById("campo");
          campo.querySelectorAll(".jogador").forEach(j => j.remove());
          
          if (posicoes[f]) {
            posicoes[f].forEach(j => {
              const div = document.createElement("div");
              div.className = "jogador";
              div.style.top = j.t + "%";
              div.style.left = j.l + "%";
              div.innerText = j.p;
              campo.appendChild(div);
            });
          }

          const d = matriz[f][p];
          document.getElementById("info-descricao").innerText = d.d;
          document.getElementById("info-pros").innerText = d.p;
          document.getElementById("info-contras").innerText = d.c;
          document.getElementById("info-combate").innerText = d.b;
        }
        window.onload = atualizarPainel;
      </script>
    </body>
    </html>
    """

    components.html(painel_html, height=550, scrolling=True)
