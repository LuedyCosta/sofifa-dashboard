import streamlit as st
import streamlit.components.v1 as components

def renderizar_painel_tatico():
    st.title("📋 Guia Interativo de Formações & Tactical Presets (FC 26)")
    st.markdown("Selecione a formação tática e o estilo de jogo (Tactical Preset) para visualizar a disposição gráfica em campo e a análise detalhada.")

    painel_html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <style>
        body { background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; display: flex; justify-content: center; margin: 0; padding: 10px; }
        .painel-container { display: flex; gap: 20px; background: #1e1e1e; padding: 20px; border-radius: 8px; max-width: 980px; width: 100%; box-sizing: border-box; }
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
        .seletor-grupo label { display: block; margin-bottom: 4px; font-size: 11px; font-weight: bold; color: #ddd; }
        .seletor-grupo select { width: 100%; padding: 6px; background: #333; color: #fff; border: 1px solid #555; border-radius: 4px; font-size: 11px; }
        .card-info { background: #2a2a2a; padding: 10px 12px; border-radius: 6px; border-left: 4px solid #3b82f6; }
        .card-info h3 { margin: 0 0 4px 0; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
        .card-info p { margin: 0; font-size: 11.5px; color: #ccc; line-height: 1.35; }
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
              <label for="formacao-select">Formação Tática:</label>
              <select id="formacao-select" onchange="aoMudarFormacao()">
                <optgroup label="3 Zagueiros">
                  <option value="3142">3-1-4-2</option>
                  <option value="3412">3-4-1-2</option>
                  <option value="3421">3-4-2-1</option>
                  <option value="343">3-4-3 (Flat / Diamond)</option>
                  <option value="3511">3-5-1-1</option>
                  <option value="352">3-5-2</option>
                </optgroup>
                <optgroup label="4 Zagueiros (Losangos / Volantes)">
                  <option value="41212-n">4-1-2-1-2 Narrow</option>
                  <option value="41212-w">4-1-2-1-2 Wide</option>
                  <option value="4132">4-1-3-2</option>
                  <option value="4141">4-1-4-1</option>
                  <option value="4213">4-2-1-3</option>
                  <option value="4222">4-2-2-2</option>
                  <option value="4231-n">4-2-3-1 Narrow</option>
                  <option value="4231-w">4-2-3-1 Wide</option>
                  <option value="424">4-2-4</option>
                  <option value="4312">4-3-1-2</option>
                  <option value="4321">4-3-2-1 (Meta)</option>
                </optgroup>
                <optgroup label="4 Zagueiros (Tradicionais / Três Pontas)">
                  <option value="433-flat">4-3-3 Flat</option>
                  <option value="433-holding">4-3-3 Holding</option>
                  <option value="433-defend">4-3-3 Defend</option>
                  <option value="433-attack">4-3-3 Attack</option>
                  <option value="433-false9">4-3-3 False 9</option>
                  <option value="4411">4-4-1-1</option>
                  <option value="442-flat">4-4-2 Flat</option>
                  <option value="442-holding">4-4-2 Holding</option>
                  <option value="451">4-5-1</option>
                </optgroup>
                <optgroup label="5 Zagueiros">
                  <option value="5122">5-1-2-2</option>
                  <option value="5212">5-2-1-2</option>
                  <option value="5221">5-2-2-1</option>
                  <option value="523">5-2-3</option>
                  <option value="532">5-3-2</option>
                  <option value="541">5-4-1 (Flat / Diamond)</option>
                </optgroup>
              </select>
            </div>
            <div class="seletor-grupo">
              <label for="preset-select">Tactical Preset:</label>
              <select id="preset-select" onchange="atualizarPainel()">
                <option value="short-passing">Short Passing / Build-Up Curto</option>
                <option value="heavy-metal">Heavy Metal Counter / Transição Vertical</option>
                <option value="gegenpress">Gegenpress / Pressão Alta</option>
                <option value="wing-play">Wing-Play / Amplitude Máxima</option>
                <option value="possession">Possession / Controle de Ritmo</option>
                <option value="balanced">Balanced / Metade e Metade</option>
                <option value="tikitaka">Tiki-Taka / Jogo Curto</option>
                <option value="vertical-counter">Vertical Counter / Ataque Direto</option>
                <option value="park-bus">Park the Bus / Bloco Baixo</option>
                <option value="counter">Counter-Attack / Transição Fluida</option>
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
          "3142": [{p:"GOL",t:50,l:6},{p:"ZAG",t:25,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:75,l:20},{p:"VOL",t:50,l:38},{p:"ALA",t:10,l:50},{p:"MC",t:38,l:55},{p:"MC",t:62,l:55},{p:"ALA",t:90,l:50},{p:"ATA",t:38,l:80},{p:"ATA",t:62,l:80}],
          "3412": [{p:"GOL",t:50,l:6},{p:"ZAG",t:25,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:75,l:20},{p:"ALA",t:10,l:50},{p:"MC",t:38,l:45},{p:"MC",t:62,l:45},{p:"ALA",t:90,l:50},{p:"MEI",t:50,l:65},{p:"ATA",t:38,l:82},{p:"ATA",t:62,l:82}],
          "3421": [{p:"GOL",t:50,l:6},{p:"ZAG",t:25,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:75,l:20},{p:"ALA",t:10,l:50},{p:"MC",t:38,l:45},{p:"MC",t:62,l:45},{p:"ALA",t:90,l:50},{p:"MEI",t:35,l:68},{p:"MEI",t:65,l:68},{p:"ATA",t:50,l:82}],
          "343": [{p:"GOL",t:50,l:6},{p:"ZAG",t:25,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:75,l:20},{p:"ALA",t:10,l:50},{p:"MC",t:38,l:45},{p:"MC",t:62,l:45},{p:"ALA",t:90,l:50},{p:"PE",t:15,l:78},{p:"ATA",t:50,l:82},{p:"PD",t:85,l:78}],
          "3511": [{p:"GOL",t:50,l:6},{p:"ZAG",t:25,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:75,l:20},{p:"ALA",t:10,l:50},{p:"VOL",t:38,l:38},{p:"MC",t:50,l:52},{p:"VOL",t:62,l:38},{p:"ALA",t:90,l:50},{p:"CF",t:50,l:68},{p:"ATA",t:50,l:82}],
          "352": [{p:"GOL",t:50,l:6},{p:"ZAG",t:25,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:75,l:20},{p:"ALA",t:10,l:50},{p:"VOL",t:38,l:40},{p:"MC",t:50,l:55},{p:"VOL",t:62,l:40},{p:"ALA",t:90,l:50},{p:"ATA",t:35,l:80},{p:"ATA",t:65,l:80}],
          "41212-n": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:50,l:38},{p:"MC",t:32,l:52},{p:"MC",t:68,l:52},{p:"MEI",t:50,l:66},{p:"ATA",t:38,l:82},{p:"ATA",t:62,l:82}],
          "41212-w": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:50,l:38},{p:"ME",t:15,l:55},{p:"MD",t:85,l:55},{p:"MEI",t:50,l:66},{p:"ATA",t:38,l:82},{p:"ATA",t:62,l:82}],
          "4132": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:50,l:38},{p:"ME",t:15,l:58},{p:"MC",t:50,l:58},{p:"MD",t:85,l:58},{p:"ATA",t:38,l:82},{p:"ATA",t:62,l:82}],
          "4141": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:50,l:38},{p:"ME",t:15,l:55},{p:"MC",t:38,l:55},{p:"MC",t:62,l:55},{p:"MD",t:85,l:55},{p:"ATA",t:50,l:82}],
          "4213": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:38,l:40},{p:"VOL",t:62,l:40},{p:"MEI",t:50,l:62},{p:"PE",t:15,l:78},{p:"ATA",t:50,l:82},{p:"PD",t:85,l:78}],
          "4222": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:38,l:40},{p:"VOL",t:62,l:40},{p:"MEI",t:25,l:62},{p:"MEI",t:75,l:62},{p:"ATA",t:38,l:82},{p:"ATA",t:62,l:82}],
          "4231-n": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:38,l:40},{p:"VOL",t:62,l:40},{p:"MEI",t:25,l:62},{p:"MEI",t:50,l:65},{p:"MEI",t:75,l:62},{p:"ATA",t:50,l:82}],
          "4231-w": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:38,l:40},{p:"VOL",t:62,l:40},{p:"ME",t:15,l:62},{p:"MEI",t:50,l:65},{p:"MD",t:85,l:62},{p:"ATA",t:50,l:82}],
          "424": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:38,l:45},{p:"VOL",t:62,l:45},{p:"PE",t:15,l:78},{p:"ATA",t:38,l:82},{p:"ATA",t:62,l:82},{p:"PD",t:85,l:78}],
          "4312": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"MC",t:28,l:45},{p:"MC",t:50,l:42},{p:"MC",t:72,l:45},{p:"MEI",t:50,l:62},{p:"ATA",t:38,l:80},{p:"ATA",t:62,l:80}],
          "4321": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"MC",t:28,l:45},{p:"MC",t:50,l:40},{p:"MC",t:72,l:45},{p:"CF",t:35,l:65},{p:"CF",t:65,l:65},{p:"ATA",t:50,l:82}],
          "433-flat": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"MC",t:25,l:48},{p:"MC",t:50,l:48},{p:"MC",t:75,l:48},{p:"PE",t:15,l:78},{p:"ATA",t:50,l:82},{p:"PD",t:85,l:78}],
          "433-holding": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:50,l:38},{p:"MC",t:30,l:55},{p:"MC",t:70,l:55},{p:"PE",t:15,l:78},{p:"ATA",t:50,l:82},{p:"PD",t:85,l:78}],
          "433-defend": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:38,l:38},{p:"VOL",t:62,l:38},{p:"MC",t:50,l:55},{p:"PE",t:15,l:78},{p:"ATA",t:50,l:82},{p:"PD",t:85,l:78}],
          "433-attack": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:38,l:40},{p:"VOL",t:62,l:40},{p:"MEI",t:50,l:62},{p:"PE",t:15,l:78},{p:"ATA",t:50,l:82},{p:"PD",t:85,l:78}],
          "433-false9": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:50,l:40},{p:"MC",t:32,l:53},{p:"MC",t:68,l:53},{p:"PE",t:15,l:75},{p:"F9",t:50,l:68},{p:"PD",t:85,l:75}],
          "4411": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"ME",t:15,l:50},{p:"MC",t:38,l:48},{p:"MC",t:62,l:48},{p:"MD",t:85,l:50},{p:"SA",t:50,l:66},{p:"ATA",t:50,l:82}],
          "442-flat": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"ME",t:15,l:50},{p:"MC",t:38,l:45},{p:"MC",t:62,l:45},{p:"MD",t:85,l:50},{p:"ATA",t:38,l:78},{p:"ATA",t:62,l:78}],
          "442-holding": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"ME",t:15,l:50},{p:"VOL",t:38,l:42},{p:"VOL",t:62,l:42},{p:"MD",t:85,l:50},{p:"ATA",t:38,l:78},{p:"ATA",t:62,l:78}],
          "451": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"ME",t:10,l:55},{p:"MEI",t:32,l:60},{p:"MC",t:50,l:45},{p:"MEI",t:68,l:60},{p:"MD",t:90,l:55},{p:"ATA",t:50,l:82}],
          "5122": [{p:"GOL",t:50,l:6},{p:"ALA",t:10,l:25},{p:"ZAG",t:28,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:72,l:20},{p:"ALA",t:90,l:25},{p:"VOL",t:50,l:38},{p:"MC",t:35,l:52},{p:"MC",t:65,l:52},{p:"ATA",t:38,l:80},{p:"ATA",t:62,l:80}],
          "5212": [{p:"GOL",t:50,l:6},{p:"ALA",t:10,l:25},{p:"ZAG",t:28,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:72,l:20},{p:"ALA",t:90,l:25},{p:"VOL",t:38,l:42},{p:"VOL",t:62,l:42},{p:"MEI",t:50,l:62},{p:"ATA",t:38,l:80},{p:"ATA",t:62,l:80}],
          "5221": [{p:"GOL",t:50,l:6},{p:"ALA",t:10,l:25},{p:"ZAG",t:28,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:72,l:20},{p:"ALA",t:90,l:25},{p:"VOL",t:38,l:42},{p:"VOL",t:62,l:42},{p:"PE",t:20,l:72},{p:"PD",t:80,l:72},{p:"ATA",t:50,l:82}],
          "523": [{p:"GOL",t:50,l:6},{p:"ALA",t:10,l:25},{p:"ZAG",t:28,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:72,l:20},{p:"ALA",t:90,l:25},{p:"VOL",t:38,l:45},{p:"VOL",t:62,l:45},{p:"PE",t:15,l:78},{p:"ATA",t:50,l:82},{p:"PD",t:85,l:78}],
          "532": [{p:"GOL",t:50,l:6},{p:"ALA",t:10,l:25},{p:"ZAG",t:28,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:72,l:20},{p:"ALA",t:90,l:25},{p:"MC",t:30,l:48},{p:"MC",t:50,l:45},{p:"MC",t:70,l:48},{p:"ATA",t:38,l:78},{p:"ATA",t:62,l:78}],
          "541": [{p:"GOL",t:50,l:6},{p:"ALA",t:10,l:25},{p:"ZAG",t:28,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:72,l:20},{p:"ALA",t:90,l:25},{p:"ME",t:15,l:50},{p:"MC",t:38,l:48},{p:"MC",t:62,l:48},{p:"MD",t:85,l:50},{p:"ATA",t:50,l:80}]
        };

        const presetPadraoFormacao = {
          "3142": "short-passing", "3412": "heavy-metal", "3421": "gegenpress", "343": "wing-play",
          "3511": "possession", "352": "balanced", "41212-n": "tikitaka", "41212-w": "balanced",
          "4132": "vertical-counter", "4141": "park-bus", "4213": "counter", "4222": "balanced",
          "4231-n": "possession", "4231-w": "gegenpress", "424": "gegenpress", "4312": "short-passing",
          "4321": "heavy-metal", "433-flat": "balanced", "433-holding": "possession", "433-defend": "park-bus",
          "433-attack": "gegenpress", "433-false9": "tikitaka", "4411": "counter", "442-flat": "vertical-counter",
          "442-holding": "balanced", "451": "possession", "5122": "counter", "5212": "vertical-counter",
          "5221": "wing-play", "523": "counter", "532": "park-bus", "541": "park-bus"
        };

        const matrizMatriz = {
          "3142": {
            "short-passing": {
              d: "Utiliza um volante fixo à frente de três zagueiros, uma linha de quatro intermediária com alas e meias centrais, e dois atacantes de referência.",
              p: "Excelente circulação de bola pelo meio e superioridade numérica imediata na construção ofensiva curta.",
              c: "Alas sobrecarregados defensivamente; se perdem a bola, o lado do campo fica totalmente exposto.",
              b: "Explore pontas velozes pelas laterais nas costas dos alas e use triangulações rápidas para isolar os três zagueiros."
            }
          },
          "3412": {
            "heavy-metal": {
              d: "Estrutura agressiva que une um meia armador (CAM) e dois centroavantes logo acima de quatro meio-campistas/alas.",
              p: "Poder ofensivo avassalador por dentro, criando tabelas contínuas na entrada da área adversária.",
              c: "Ausência de um volante fixo de contenção puramente defensivo deixa o miolo vulnerável a infiltrações.",
              b: "Jogue com um meio-campo compacto (como um 4-2-3-1) para fechar o espaço do CAM e force o jogo para as laterais."
            }
          },
          "3421": {
            "gegenpress": {
              d: "Dois meias atacantes flutuando por dentro apoiando um único centroavante, com alas cobrindo a largura do campo.",
              p: "Sufoca o adversário no campo de ataque e gera constante pressão pós-perda com os meias avançados.",
              c: "Estamina dos alas esgota rapidamente e o ataque pode ficar dependente da inspiração individual do centroavante.",
              b: "Quebre a primeira linha de pressão com passes longos e certeiros para os pontas ou alas em velocidade."
            }
          },
          "343": {
            "wing-play": {
              d: "Formação focada em esticar a defesa adversária com pontas abertos colados na linha lateral e forte presença ofensiva.",
              p: "Criação abundante de jogadas de linha de fundo e cruzamentos venenosos para a grande área.",
              c: "Fragilidade defensiva extrema nas diagonais defensivas dos zagueiros externos.",
              b: "Feche a entrada da área com uma linha de quatro zagueiros compactos e anule as opções de cruzamento bloqueando os pontas."
            }
          },
          "3511": {
            "possession": {
              d: "Meio-campo superpovoado com um segundo atacante (CF) atuando como elemento surpresa atrás do centroavante estático.",
              p: "Posse de bola segura, controle territorial absoluto e bloqueio eficiente de passes centrais.",
              c: "Ritmo de jogo lento e previsível se os alas não tiverem ímpeto ofensivo constante.",
              b: "Adote uma postura de bloco médio, feche as linhas de passe interiores e force erros de troca de bola na intermediária."
            }
          },
          "352": {
            "balanced": {
              d: "O esquema clássico de três zagueiros com dois volantes de contenção, um armador e dois atacantes.",
              p: "Equilíbrio perfeito entre solidez defensiva central e volume de jogo ofensivo com a dupla de frente.",
              c: "Os espaços deixados nas costas dos alas exigem cobertura manual impecável dos zagueiros laterais.",
              b: "Ataque pelas pontas com pontas rápidos para forçar o ala rival a recuar, transformando a linha de 3 em uma linha defensiva de 5 pressionada."
            }
          },
          "41212-n": {
            "tikitaka": {
              d: "Losango tradicional no meio-campo com um volante defensivo, dois meias centrais, um CAM e dois atacantes.",
              p: "Domínio absoluto do centro do campo, facilitando triangulações curtas e tabelas mortais.",
              c: "Totalmente nula em amplitude lateral, sofrendo contra equipes que exploram os corredores das pontas.",
              b: "Utilize formações abertas (como 4-3-3 ou 4-4-2) e force o adversário a atacar exclusivamente pelos lados, onde sua defesa está armada."
            }
          },
          "41212-w": {
            "balanced": {
              d: "Variação do losango que puxa os meias centrais para as posições de LM e RM, garantindo largura.",
              p: "Corrige a falha crônica de amplitude do losango fechado sem perder o poder de fogo central.",
              c: "O meio-campo central fica mais desguarnecido, contando apenas com um volante na proteção.",
              b: "Conquiste o controle do meio-campo com três homens no setor e explore o espaço deixado pelo volante solitário."
            }
          },
          "4132": {
            "vertical-counter": {
              d: "Linha de três meias avançados logo acima de um único volante, municiando dois centroavantes rápidos.",
              p: "Transição ofensiva extremamente rápida e vertical rumo ao gol adversário.",
              c: "O volante central fica totalmente isolado no combate defensivo caso o time perca a bola no campo ofensivo.",
              b: "Pressione a saída de bola do volante único e mantenha a zaga atenta a bolas longas nas costas."
            }
          },
          "4141": {
            "park-bus": {
              d: "Linha de quatro meio-campistas compactada com um volante defensivo à frente da zaga e um único atacante isolado.",
              p: "Linha defensiva extremamente próxima, bloqueando qualquer espaço de infiltração pelo centro.",
              c: "Extrema dificuldade para gerar perigo ofensivo ou contra-atacar com volume.",
              b: "Use chutes de longa distância, circule a bola com paciência e explore cruzamentos altos para furar o bloqueio estático."
            }
          },
          "4213": {
            "counter": {
              d: "Duplo pivô de volantes protegendo a zaga, com um CAM municiando um trio de ataque rápido (PE, PD e centroavante).",
              p: "Combinação perfeita de segurança defensiva com velocidade letal nas pontas.",
              c: "O CAM pode se desgastar muito tendo que transitar entre armar o jogo e recompor a linha defensiva.",
              b: "Feche os corredores internos com um meio-campo em bloco médio e evite perder a bola no ataque para não sofrer contra-ataques."
            }
          },
          "4222": {
            "balanced": {
              d: "Dois volantes, dois meias ofensivos centralizados/abertos por dentro e dois centroavantes.",
              p: "Estrutura extremamente simétrica e sólida, excelente para fechar os espaços entrelinhas.",
              c: "Falta profundidade e largura natural nas pontas, exigindo apoio constante dos laterais.",
              b: "Explore os espaços deixados pelos laterais quando eles sobem para tentar dar largura ao time."
            }
          },
          "4231-n": {
            "possession": {
              d: "O clássico esquema de segurança com dois volantes, três meias ofensivos compactos (LAM, CAM, RAM) e um centroavante.",
              p: "Controle absoluto de jogo, posse de bola segura e intransponibilidade no miolo de zaga.",
              c: "Jogo pode se tornar engessado e previsível se o adversário fechar bem a entrada da área.",
              b: "Adote marcação em zona rigorosa e force o adversário a arriscar passes longos inofensivos."
            }
          },
          "4231-w": {
            "gegenpress": {
              d: "Mantém o duplo pivô e o centroavante, mas abre dois pontas legítimos (LM e RM) nas alas com transição rápida.",
              p: "Junta a solidez defensiva dos volantes com a amplitude agressiva dos pontas.",
              c: "Exige extrema dedicação defensiva dos pontas para fechar os espaços junto aos laterais.",
              b: "Supere o duplo pivô trocando passes rápidos em velocidade pelo centro com meias criativos."
            }
          },
          "424": {
            "gegenpress": {
              d: "Quatro atacantes fixos apoiados por apenas dois volantes e a linha de defesa.",
              p: "Pressão sufocante na saída de bola rival e volume ofensivo máximo.",
              c: "Buraco gigantesco no meio-campo; qualquer erro na pressão resulta em contra-ataque livre para o rival.",
              b: "Atraia a pressão tocando a bola curto na defesa e lance imediatamente nas costas dos volantes que sobem sozinhos."
            }
          },
          "4312": {
            "short-passing": {
              d: "Três meio-campistas centrais, um armador central (CAM) e dois centroavantes.",
              p: "Excelente para reter a bola no campo ofensivo e envolver a zaga com passes curtos.",
              c: "Totalmente vulnerável a ataques rápidos pelas laterais do campo.",
              b: "Jogue com pontas rápidos e force o jogo pelas pontas onde o adversário não tem cobertura defensiva natural."
            }
          },
          "4321": {
            "heavy-metal": {
              d: "Três meio-campistas com dois atacantes flutuantes (CFs) logo atrás de um centroavante.",
              p: "O esquema mais eficiente do jogo, unindo infiltrações mortais dos CFs com solidez defensiva ajustável.",
              c: "Exige ajustes manuais precisos nas instruções para não perder o controle das laterais.",
              b: "Utilize um duplo pivô compacto e evite dar espaço para os CFs girarem na entrada da área."
            }
          },
          "433-flat": {
            "balanced": {
              d: "O desenho mais universal do futebol: linha de 4, trio de meio-campo plano, pontas abertos e centroavante.",
              p: "Distribuição homogênea de jogadores por todo o campo, facilitando qualquer estilo de jogo.",
              c: "Pode se tornar vulnerável se os três meias tiverem apenas funções passivas.",
              b: "Supere o meio-campo com superioridade numérica temporária vinda de descidas dos alas ou do segundo atacante."
            }
          },
          "433-holding": {
            "possession": {
              d: "Variação da 4-3-3 com um volante de contenção fixo protegendo a zaga e dois meias à frente.",
              p: "Maior estabilidade defensiva em transições sem perder a largura dos pontas.",
              c: "O setor de criação pode ficar lento se o volante for excessivamente defensivo.",
              b: "Feche os espaços entre o volante fixo e os zagueiros para sufocar a saída de bola curta."
            }
          },
          "433-defend": {
            "park-bus": {
              d: "Dois volantes mais recuados e um meio-campista central, mantendo os pontas e o centroavante avançados.",
              p: "Excelente para segurar resultados contra equipes muito técnicas.",
              c: "Dificuldade acentuada para criar volume de jogo no ataque.",
              b: "Avance sua linha defensiva até o meio-campo e pressione a saída de bola sem medo."
            }
          },
          "433-attack": {
            "gegenpress": {
              d: "Um meio-campista avança para se alinhar ao ataque como um armador, deixando dois volantes na base com pressão alta.",
              p: "Grande presença de jogadores na zona de finalização adversária.",
              c: "Deixa um buraco perigoso na entrelinhas defensiva.",
              b: "Infiltra passes rápidos rasteiros no espaço deixado pelo meia que avançou para o ataque."
            }
          },
          "433-false9": {
            "tikitaka": {
              d: "Centroavante recua para buscar jogo, atraindo zagueiros e abrindo caminho para os pontas.",
              p: "Posse de bola sufocante e extrema dificuldade de marcação individual para os zagueiros rivais.",
              c: "Ausência de um centroavante de referência física na grande área.",
              b: "Mantenha a linha defensiva recuada e por zona, proibindo os zagueiros de saírem da posição para caçar o falso 9."
            }
          },
          "4411": {
            "counter": {
              d: "Duas linhas de quatro compactas com um segundo atacante flutuando atrás do centroavante.",
              p: "Solidez defensiva exemplar combinada com transições rápidas pelos lados.",
              c: "Pouca criatividade central se o segundo atacante for neutralizado.",
              b: "Use meias criativos entrelinhas para quebrar as duas linhas de quatro do adversário."
            }
          },
          "442-flat": {
            "vertical-counter": {
              d: "Duas linhas rígidas de quatro jogadores e uma dupla de ataque tradicional.",
              p: "Simples de executar, extremamente compacta e letal em contra-ataques verticais.",
              c: "O meio-campo central pode ser dominado por esquemas com três ou mais homens no setor.",
              b: "Sobrecargue o setor central com um trio de meio-campo móvel para forçar os alas rivais a fecharem o jogo."
            }
          },
          "442-holding": {
            "balanced": {
              d: "Ajusta os dois meias centrais para funções de volantes de contenção, mantendo as linhas de quatro.",
              p: "Segurança defensiva máxima sem abrir mão da dupla de ataque.",
              c: "Pode faltar aproximação rápida para a construção de jogadas no campo ofensivo.",
              b: "Circule a bola com paciência pelos flancos e explore cruzamentos para vencer a altura dos volantes recuados."
            }
          },
          "451": {
            "possession": {
              d: "Linha de cinco meio-campistas compactos sufocando o adversário com um único centroavante isolado.",
              p: "Impossível de perder a posse de bola no meio-campo se bem executada.",
              c: "Ataque totalmente isolado e dependente de subidas tardias dos meias.",
              b: "Mantenha a calma na defesa, feche os espaços centrais e utilize bolas longas para surpreender a retarguarda alta."
            }
          },
          "5122": {
            "counter": {
              d: "Linha defensiva de cinco com um volante central e dois atacantes de referência na frente.",
              p: "Muralha defensiva intransponível por dentro com duas opções claras de escape no ataque.",
              c: "Meio-campo defensivo isolado do ataque durante longos períodos do jogo.",
              b: "Pressione a saída de bola no campo adversário e force os alas a correrem para trás, desgastando-os fisicamente."
            }
          },
          "5212": {
            "vertical-counter": {
              d: "Três zagueiros e dois alas, protegidos por dois volantes e armados por um CAM para servir dois centroavantes.",
              p: "Excelente equilíbrio entre fechar a defesa e contra-atacar com velocidade central e lateral.",
              c: "Espaços consideráveis entre o duplo pivô e o CAM se o time for empurrado para trás.",
              b: "Mantenha a posse de bola no campo ofensivo e use chutes de longa distância para furar o bloqueio duplo."
            }
          },
          "5221": {
            "wing-play": {
              d: "Defesa de cinco com dois volantes, dois meias/pontas abertos e um centroavante.",
              p: "Proteção lateral reforçada combinada com velocidade agigantada nas pontas.",
              c: "O meio-campo central sofre para conter equipes que tocam a bola rápido por dentro.",
              b: "Centralize o jogo com meias criativos e evite dar espaço para os pontas dispararem nas costas dos alas."
            }
          },
          "523": {
            "counter": {
              d: "Trio de zagueiros, dois alas, dois volantes centrais e um trio de ataque rápido (ponta esquerda, ponta direita e centroavante).",
              p: "Defesa quase intransponível contra investidas centrais e contra-ataques devastadores com três homens na frente.",
              c: "Meio-campo central reduzido a dois jogadores, facilitando o domínio territorial do rival.",
              b: "Domine o círculo central com superioridade numérica de meio-campistas e cadastre a posse de bola."
            }
          },
          "532": {
            "park-bus": {
              d: "Três zagueiros, dois alas, um trio de meio-campo compacto e dois centroavantes.",
              p: "Fechamento absoluto de todos os espaços centrais e lateral próximos à área.",
              c: "Ofensivamente pobre, dependendo de lances esporádicos de velocidade da dupla de ataque.",
              b: "Use cruzamentos venenosos, chutes de fora da área e mantenha uma linha alta para abafar qualquer tentativa de saída rápida."
            }
          },
          "541": {
            "park-bus": {
              d: "O nível máximo de segurança defensiva do FC 26: linha de 5 defensiva e linha de 4 intermediária.",
              p: "Praticamente impossível de ser penetrada por jogadas normais de toque de bola.",
              c: "Zero presença ofensiva; o time inteiro abdica de atacar.",
              b: "Tenha paciência extrema na circulação de bola, explore chutes colocados de longa distância e o recurso de cruzamentos na área para forçar erros defensivos."
            }
          }
        };

        const presetInfoGenerico = {
          "short-passing": {
            d_mod: " Com a mentalidade de Short Passing, o time prioriza apoios curtos e aproximados para ter sempre opções de passe rasteiro.",
            p_mod: " Excelente para manter o controle no campo de ataque sem desperdiçar a bola em lançamentos arriscados.",
            c_mod: " Torna o time vulnerável a pressões altas agressivas caso falhe em um passe curto perto do seu próprio gol.",
            b_mod: " Suba as linhas e exerça pressão sufocante no portador para forçar erros de passe curto na defesa adversária."
          },
          "heavy-metal": {
            d_mod: " Com a estratégia Heavy Metal Counter, a equipe acelera de forma vertical e agressiva imediatamente após recuperar a posse.",
            p_mod: " Transição ultra-rápida que pega a defesa adversária desorganizada antes da recomposição.",
            c_mod: " Alto desgaste físico dos meias/atacantes e maior taxa de perda de posse por tentativas de passes verticais forçados.",
            b_mod: " Mantenha um volante de contenção fixo e reduza o espaço entre a zaga e o meio-campo para travar a aceleração inicial."
          },
          "gegenpress": {
            d_mod: " Sob o estilo Gegenpress, todos os jogadores próximos à bola pressionam imediatamente o adversário no momento em que a posse é perdida.",
            p_mod: " Recuperação da bola no campo de ataque, gerando oportunidades de gol imediatas.",
            c_mod: " Consumo acelerado de estamina e risco de abrir lacunas gigantescas se o adversário quebrar a primeira linha de pressão.",
            b_mod: " Use passes longos diretos para os pontas ou inverta a jogada com lançamentos para fugir do tumulto da pressão."
          },
          "wing-play": {
            d_mod: " Sob a tática Wing-Play, o jogo é ampliado até as linhas laterais, explorando intensamente dobradinhas de pontas e alas.",
            p_mod: " Criação constante de espaço na área através de cruzamentos, esticando a linha defensiva adversária.",
            c_mod: " Desguarnece as diagonais defensivas caso os pontas e alas demorem a recompor.",
            b_mod: " Dobre a marcação nas laterais e certifique-se de ter zagueiros com bom poder de combate aéreo."
          },
          "possession": {
            d_mod: " Com o preset Possession, a equipe trabalha a bola com paciência prolongada, valorizando o domínio do ritmo do jogo.",
            p_mod: " Minimiza o risco de sofrer contra-ataques ao negar a posse de bola ao adversário durante a maior parte do tempo.",
            c_mod: " O ritmo pode se tornar previsível e estéril se não houver movimentação de infiltração sem a bola.",
            b_mod: " Mantenha um bloco médio organizado, feche o centro do campo e force o adversário a dar passes inofensivos para trás."
          },
          "balanced": {
            d_mod: " Com o preset Balanced, o time busca o equilíbrio clássico entre aproximação ofensiva e recomposição defensiva consciente.",
            p_mod: " Manutenção de uma estrutura tática sólida durante os 90 minutos sem expor nenhum setor em excesso.",
            c_mod: " Pode faltar a intensidade ou contundência especial necessária para furar defesas extremamente retrancadas.",
            b_mod: " Explore superioridade numérica em setores específicos ou acelere o jogo com mudanças bruscas de ritmo."
          },
          "tikitaka": {
            d_mod: " Sob a filosofia Tiki-Taka, a equipe cria triangulações incessantes na zona central com trocas de posição rápidas.",
            p_mod: " Elevadíssima taxa de acerto de passe e grande capacidade de envolver a zaga rival com tabelas de um toque.",
            c_mod: " Falta de presença física tradicional dentro da grande área em momentos de cruzamento.",
            b_mod: " Feche a entrada da grande área em zona compacta e evite que seus zagueiros saiam caçando meias fora da posição."
          },
          "vertical-counter": {
            d_mod: " Com a abordagem Vertical Counter, o time recupera a bola e busca imediatamente lançamentos em profundidade para os atacantes.",
            p_mod: " Letalidade extrema contra times que jogam com linha defensiva alta.",
            c_mod: " Tendência a entregar a bola rapidamente se o adversário defender bem a profundidade.",
            b_mod: " Recue a linha de defesa e mantenha a zaga perfilada para rebater bolas longas antes que quiquem na área."
          },
          "park-bus": {
            d_mod: " Com o preset Park the Bus, a equipe recua todas as linhas para as imediações da própria grande área em bloco baixo estático.",
            p_mod: " Bloqueio quase impenetrável por baixo no setor central da área.",
            c_mod: " Abdicação quase total do ataque, criando uma pressão psicológica contínua no campo defensivo.",
            b_mod: " Arrisque chutes colocados/de fora da área (Power Shots) e explore cruzamentos venenosos para forçar erros da zaga."
          },
          "counter": {
            d_mod: " Sob a tática Counter-Attack, o time aceita a pressão no seu campo e dispara em transições fluidas quando recupera a bola.",
            p_mod: " Exploração máxima dos espaços vazios deixados por equipes que atacam com muitos homens.",
            c_mod: " Se a equipe sofrer um gol logo no início, terá dificuldades para propor o jogo ativamente.",
            b_mod: " Pressione a transição defensiva rival no momento da perda (Counter-press) e evite perdas de bola bobas no meio."
          }
        };

        function aoMudarFormacao() {
          const f = document.getElementById("formacao-select").value;
          if (presetPadraoFormacao[f]) {
            document.getElementById("preset-select").value = presetPadraoFormacao[f];
          }
          atualizarPainel();
        }

        function atualizarPainel() {
          const f = document.getElementById("formacao-select").value;
          const p = document.getElementById("preset-select").value;

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

          let base = null;
          if (matrizMatriz[f] && matrizMatriz[f][p]) {
            base = matrizMatriz[f][p];
          } else {
            const padrao = presetPadraoFormacao[f] || "balanced";
            const baseOriginal = (matrizMatriz[f] && matrizMatriz[f][padrao]) ? matrizMatriz[f][padrao] : {
              d: "Formação com estrutura adaptada para o controle tático do campo.",
              p: "Boa distribuição espacial e opções de passe pelas linhas de sustentação.",
              c: "Exige atenção às coberturas nos setores em transição rápida.",
              b: "Ataque os pontos de menor cobertura do setor intermediário."
            };
            const mod = presetInfoGenerico[p] || presetInfoGenerico["balanced"];
            base = {
              d: baseOriginal.d + mod.d_mod,
              p: baseOriginal.p + mod.p_mod,
              c: baseOriginal.c + mod.c_mod,
              b: baseOriginal.b + " " + mod.b_mod
            };
          }

          document.getElementById("info-descricao").innerText = base.d;
          document.getElementById("info-pros").innerText = base.p;
          document.getElementById("info-contras").innerText = base.c;
          document.getElementById("info-combate").innerText = base.b;
        }

        window.onload = aoMudarFormacao;
      </script>
    </body>
    </html>
    """

    components.html(painel_html, height=560, scrolling=True)
