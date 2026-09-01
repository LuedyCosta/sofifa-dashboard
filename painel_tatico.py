# Arquivo: painel_tatico.py
import streamlit as st
import streamlit.components.v1 as components

def renderizar_painel_tatico():
    st.title("📋 Guia de Formações & Tactical Presets (FC26)")
    st.markdown("Analise a disposição tática em campo, os estilos de construção de jogada e as estratégias completas.")

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
        .jogador { position: absolute; transform: translate(-50%, -50%); width: 26px; height: 26px; background-color: #ffffff; color: #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 9px; transition: all 0.3s ease-in-out; }
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
                <option value="433-holding">4-3-3 Holding</option>
                <option value="442">4-4-2 Tradicional</option>
                <option value="352">3-5-2</option>
              </select>
            </div>
            <div class="seletor-grupo">
              <label for="preset-select">Tactical Preset:</label>
              <select id="preset-select" onchange="atualizarPainel()">
                <option value="padrao">Padrão (Standard)</option>
                <option value="pontas">Jogo pelas Pontas</option>
                <option value="tikitaka">Tiki-Taka / Posse</option>
                <option value="contra-ataque">Contra-Ataque</option>
                <option value="gegenpress">Gegenpressing</option>
                <option value="kick-rush">Chuta e Corre</option>
                <option value="park-bus">Estacionar o Ônibus</option>
              </select>
            </div>
          </div>
          <div class="card-info" style="border-left-color: #3b82f6;"><h3>Explicação Breve</h3><p id="info-descricao">-</p></div>
          <div class="card-info" style="border-left-color: #10b981;"><h3>Vantagens (Prós)</h3><p id="info-pros">-</p></div>
          <div class="card-info" style="border-left-color: #ef4444;"><h3>Desvantagens (Contras)</h3><p id="info-contras">-</p></div>
          <div class="card-info" style="border-left-color: #f59e0b;"><h3>Estratégia de Combate</h3><p id="info-combate">-</p></div>
        </div>
      </div>
      <script>
        const posicoes = {
          "433-holding": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:50,l:38},{p:"MC",t:30,l:55},{p:"MC",t:70,l:55},{p:"PE",t:15,l:78},{p:"CA",t:50,l:82},{p:"PD",t:85,l:78}],
          "442": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"MD",t:15,l:50},{p:"MC",t:38,l:45},{p:"MC",t:62,l:45},{p:"ME",t:85,l:50},{p:"ATA",t:38,l:78},{p:"ATA",t:62,l:78}],
          "352": [{p:"GOL",t:50,l:6},{p:"ZAG",t:25,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:75,l:20},{p:"ALA",t:10,l:50},{p:"VOL",t:38,l:40},{p:"MC",t:50,l:55},{p:"VOL",t:62,l:40},{p:"ALA",t:90,l:50},{p:"ATA",t:35,l:80},{p:"ATA",t:65,l:80}]
        };
        const matriz = {
          "433-holding": {
            "padrao": {d:"Estrutura equilibrada com o volante assegurando a proteção defensiva.",p:"Ocupação homogênea de espaço.",c:"Pode faltar agressividade contra blocos baixos.",b:"Pressionar o volante distribuidor."},
            "pontas": {d:"Pontas abertos buscando o fundo com apoio de laterais.",p:"Isolamento 1v1 nos corredores.",c:"Espaço vago nas costas dos laterais.",b:"Dobrar a marcação nos pontas."},
            "tikitaka": {d:"Triangulações curtas e paciência para infiltração.",p:"Controle absoluto da posse.",c:"Risco de perda na saída de bola.",b:"Bloqueio médio-baixo compacto."},
            "contra-ataque": {d:"Bloco recuado com passe rápido em profundidade.",p:"Letal em espaço aberto.",c:"Isolamento do centroavante.",b:"Manter contra-pressão imediata."},
            "gegenpress": {d:"Pressão sufocante no campo de ataque.",p:"Recuperação perto do gol rival.",c:"Desgaste físico alto e linha defensiva exposta.",b:"Usar ligações diretas."},
            "kick-rush": {d:"Bolas longas buscando o CA ou disputa de pontas.",p:"Bypassa a pressão adversária.",c:"Baixo aproveitamento de posse.",b:"Soberania nos duelos aéreos."},
            "park-bus": {d:"Linha de 4 e volante cimentados na área.",p:"Dificuldade nula de ceder gols por dentro.",c:"Incapacidade de sair ao ataque.",b:"Chutes de média e longa distância."}
          },
          "442": {
            "padrao": {d:"Duas linhas de quatro com dupla de ataque.",p:"Fácil entendimento e solidez.",c:"Inferioridade contra trios de meio.",b:"Explorar entrelinhas no meio-campo."},
            "pontas": {d:"Dobradinhas laterais para cruzamento.",p:"Aproveitamento da dupla de área.",c:"Corredor central exposto.",b:"Atacar por dentro no mano a mano."},
            "tikitaka": {d:"Passes curtos entre linhas de meio e ataque.",p:"Apoio constante entre setores.",c:"Falta de amplitude sem pontas natos.",b:"Afunilar a marcação no centro."},
            "contra-ataque": {d:"Duas linhas baixas e saída vertical rápida.",p:"Muralha defensiva eficiente.",c:"Alto desgaste dos meias abertos.",b:"Balanço defensivo constante."},
            "gegenpress": {d:"Ataque e meias abafam a saída rival.",p:"Força erros na área adversária.",c:"Espaço entre a defesa e meio.",b:"Giro rápido com inversão de jogo."},
            "kick-rush": {d:"Lançamentos diretos para a dupla de frente.",p:"Ganha segundas bolas no ataque.",c:"Pouca criação pelo chão.",b:"Recolher sobras com os volantes."},
            "park-bus": {d:"Linhas ultra compactas perto do gol.",p:"Fechamento total dos corredores.",c:"Presença nula no ataque.",b:"Circulação rápida para descompactar."}
          },
          "352": {
            "padrao": {d:"Três zagueiros e alas cobrindo os lados.",p:"Superioridade numérica no meio.",c:"Costas dos alas vulneráveis.",b:"Atacar os espaços dos alas."},
            "pontas": {d:"Alas atuam avançados como pontas.",p:"Amplitude máxima e cruzamentos.",c:"Sobrecarga física nos alas.",b:"Explorar zagueiros de lado no 1v1."},
            "tikitaka": {d:"Saída com 3 defensores e meio povoado.",p:"Fácil saída sob pressão.",c:"Lentidão se a bola não chegar à frente.",b:"Pressionar com 3 atacantes."},
            "contra-ataque": {d:"Linha de 5 sem a bola e transição direta.",p:"Inviolável pelo centro.",c:"Distância grande para os atacantes.",b:"Chutes de fora da área."},
            "gegenpress": {d:"Pressão com 5 meio-campistas no alto.",p:"Domínio físico no meio.",c:"Um passe certo quebra a linha toda.",b:"Passes verticais longos."},
            "kick-rush": {d:"Zagueiros lançam para a dupla de ataque.",p:"Simplicidade e presença física.",c:"Descarte da criação dos volantes.",b:"Dominar a primeira bola aérea."},
            "park-bus": {d:"Linha de 5 zagueiros + 3 volantes recuados.",p:"Bloqueio total na grande área.",c:"Falta de saída de bola.",b:"Movimentação intensa sem bola."}
          }
        };

        function atualizarPainel() {
          const f = document.getElementById("formacao-select").value;
          const p = document.getElementById("preset-select").value;
          const campo = document.getElementById("campo");
          campo.querySelectorAll(".jogador").forEach(j => j.remove());
          
          posicoes[f].forEach(j => {
            const div = document.createElement("div");
            div.className = "jogador";
            div.style.top = j.t + "%";
            div.style.left = j.l + "%";
            div.innerText = j.p;
            campo.appendChild(div);
          });

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
