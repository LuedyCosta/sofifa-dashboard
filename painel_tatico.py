import streamlit as st
import streamlit.components.v1 as components

def renderizar_painel_tatico():
    st.title("📋 Guia Completo de Formações & Tactical Presets (FC26)")
    st.markdown("Análise tática detalhada com todas as formações do FC 26, seus estilos táticos (presets), prós, contras e instruções de como jogar contra.")

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
        .seletor-grupo { background: #2a2a2a; padding: 10px; border-radius: 6px; }
        .seletor-grupo label { display: block; margin-bottom: 4px; font-size: 12px; font-weight: bold; }
        .seletor-grupo select { width: 100%; padding: 6px; background: #333; color: #fff; border: 1px solid #555; border-radius: 4px; font-size: 12px; }
        .preset-badge { background: #3b82f6; color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block; margin-top: 4px; }
        .card-info { background: #2a2a2a; padding: 10px 12px; border-radius: 6px; border-left: 4px solid #3b82f6; }
        .card-info h3 { margin: 0 0 4px 0; font-size: 12px; text-transform: uppercase; }
        .card-info p { margin: 0; font-size: 12px; color: #ccc; line-height: 1.35; }
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
          <div class="seletor-grupo">
            <label for="formacao-select">Selecione a Formação Tática:</label>
            <select id="formacao-select" onchange="atualizarPainel()">
              <optgroup label="Sistemas de 3 Zagueiros">
                <option value="3142">3-1-4-2</option>
                <option value="3412">3-4-1-2</option>
                <option value="3421">3-4-2-1</option>
                <option value="343">3-4-3 (Flat / Diamond)</option>
                <option value="3511">3-5-1-1</option>
                <option value="352">3-5-2</option>
              </optgroup>
              <optgroup label="Sistemas de 4 Zagueiros (Losangos e Volantes)">
                <option value="41212-n">4-1-2-1-2 Narrow (Fechado)</option>
                <option value="41212-w">4-1-2-1-2 Wide (Aberto)</option>
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
              <optgroup label="Sistemas de 4 Zagueiros (Tradição e Amplitude)">
                <option value="433-flat">4-3-3 Flat (Plana)</option>
                <option value="433-holding">4-3-3 Holding</option>
                <option value="433-defend">4-3-3 Defend</option>
                <option value="433-attack">4-3-3 Attack</option>
                <option value="433-false9">4-3-3 False 9</option>
                <option value="4411">4-4-1-1</option>
                <option value="442-flat">4-4-2 Flat</option>
                <option value="442-holding">4-4-2 Holding</option>
                <option value="451">4-5-1</option>
              </optgroup>
              <optgroup label="Sistemas de 5 Zagueiros">
                <option value="5122">5-1-2-2</option>
                <option value="5212">5-2-1-2</option>
                <option value="5221">5-2-2-1</option>
                <option value="523">5-2-3</option>
                <option value="532">5-3-2</option>
                <option value="541">5-4-1 (Flat / Diamond)</option>
              </optgroup>
            </select>
            <div style="margin-top: 6px;">
              <span style="font-size: 11px; color: #aaa;">Tactical Preset Mapeado:</span><br>
              <span id="preset-tag" class="preset-badge">-</span>
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

        const matriz = {
          "3142": {
            preset: "Short Passing / Build-Up Curto",
            d: "Utiliza um volante fixo à frente de três zagueiros, uma linha de quatro intermediária com alas e meias centrais, e dois atacantes de referência.",
            p: "Excelente circulação de bola pelo meio e superioridade numérica imediata na construção ofensiva curta.",
            c: "Alas sobrecarregados defensivamente; se perdem a bola, o lado do campo fica totalmente exposto.",
            b: "Explore pontas velozes pelas laterais nas costas dos alas e use triangulações rápidas para isolar os três zagueiros."
          },
          "3412": {
            preset: "Heavy Metal Counter / Transição Vertical",
            d: "Estrutura agressiva que une um meia armador (CAM) e dois centroavantes logo acima de quatro meio-campistas/alas.",
            p: "Poder ofensivo avassalador por dentro, criando tabelas contínuas na entrada da área adversária.",
            c: "Ausência de um volante fixo de contenção puramente defensivo deixa o miolo vulnerável a infiltrações.",
            b: "Jogue com um meio-campo compacto (como um 4-2-3-1) para fechar o espaço do CAM e force o jogo para as laterais."
          },
          "3421": {
            preset: "Gegenpress / Pressão Alta",
            d: "Dois meias atacantes flutuando por dentro apoiando um único centroavante, com alas cobrindo a largura do campo.",
            p: "Sufoca o adversário no campo de ataque e gera constante pressão pós-perda com os meias avançados.",
            c: "Estamina dos alas esgota rapidamente e o ataque pode ficar dependente da inspiração individual do centroavante.",
            b: "Quebre a primeira linha de pressão com passes longos e certeiros para os pontas ou alas em velocidade."
          },
          "343": {
            preset: "Wing-Play / Amplitude Máxima",
            d: "Formação focada em esticar a defesa adversária com pontas abertos colados na linha lateral e forte presença ofensiva.",
            p: "Criação abundante de jogadas de linha de fundo e cruzamentos venenosos para a grande área.",
            c: "Fragilidade defensiva extrema nas diagonais defensivas dos zagueiros externos.",
            b: "Feche a entrada da área com uma linha de quatro zagueiros compactos e anule as opções de cruzamento bloqueando os pontas."
          },
          "3511": {
            preset: "Possession / Controle de Ritmo",
            d: "Meio-campo superpovoado com um segundo atacante (CF) atuando como elemento surpresa atrás do centroavante estático.",
            p: "Posse de bola segura, controle territorial absoluto e bloqueio eficiente de passes centrais.",
            c: "Ritmo de jogo lento e previsível se os alas não tiverem ímpeto ofensivo constante.",
            b: "Adote uma postura de bloco médio, feche as linhas de passe interiores e force erros de troca de bola na intermediária."
          },
          "352": {
            preset: "Balanced / Metade e Metade",
            d: "O esquema clássico de três zagueiros com dois volantes de contenção, um armador e dois atacantes.",
            p: "Equilíbrio perfeito entre solidez defensiva central e volume de jogo ofensivo com a dupla de frente.",
            c: "Os espaços deixados nas costas dos alas exigem cobertura manual impecável dos zagueiros laterais.",
            b: "Ataque pelas pontas com pontas rápidos para forçar o ala rival a recuar, transformando a linha de 3 em uma linha defensiva de 5 pressionada."
          },
          "41212-n": {
            preset: "Tiki-Taka / Jogo Curto",
            d: "Losango tradicional no meio-campo com um volante defensivo, dois meias centrais, um CAM e dois atacantes.",
            p: "Domínio absoluto do centro do campo, facilitando triangulações curtas e tabelas mortais.",
            c: "Totalmente nula em amplitude lateral, sofrendo contra equipes que exploram os corredores das pontas.",
            b: "Utilize formações abertas (como 4-3-3 ou 4-4-2) e force o adversário a atacar exclusivamente pelos lados, onde sua defesa está armada."
          },
          "41212-w": {
            preset: "Balanced / Transição Lateral",
            d: "Variação do losango que puxa os meias centrais para as posições de LM e RM, garantindo largura.",
            p: "Corrige a falha crônica de amplitude do losango fechado sem perder o poder de fogo central.",
            c: "O meio-campo central fica mais desguarnecido, contando apenas com um volante na proteção.",
            b: "Conquiste o controle do meio-campo com três homens no setor e explore o espaço deixado pelo volante solitário."
          },
          "4132": {
            preset: "Vertical Counter / Ataque Direto",
            d: "Linha de três meias avançados logo acima de um único volante, municiando dois centroavantes rápidos.",
            p: "Transição ofensiva extremamente rápida e vertical rumo ao gol adversário.",
            c: "O volante central fica totalmente isolado no combate defensivo caso o time perca a bola no campo ofensivo.",
            b: "Pressione a saída de bola do volante único e mantenha a zaga atenta a bolas longas nas costas."
          },
          "4141": {
            preset: "Park the Bus / Bloco Baixo Compacto",
            d: "Linha de quatro meio-campistas compactada com um volante defensivo à frente da zaga e um único atacante isolado.",
            p: "Linha defensiva extremamente próxima, bloqueando qualquer espaço de infiltração pelo centro.",
            c: "Extrema dificuldade para gerar perigo ofensivo ou contra-atacar com volume.",
            b: "Use chutes de longa distância, circule a bola com paciência e explore cruzamentos altos para furar o bloqueio estático."
          },
          "4213": {
            preset: "Counter-Attack / Transição Fluida",
            d: "Duplo pivô de volantes protegendo a zaga, com um CAM municiando um trio de ataque rápido (ponta esquerda, ponta direita e centroavante).",
            p: "Combinação perfeita de segurança defensiva com velocidade letal nas pontas.",
            c: "O CAM pode se desgastar muito tendo que transitar entre armar o jogo e recompor a linha defensiva.",
            b: "Feche os corredores internos com um meio-campo em bloco médio e evite perder a bola no ataque para não sofrer contra-ataques."
          },
          "4222": {
            preset: "Balanced / Pressão Média",
            d: "Dois volantes, dois meias ofensivos centralizados/abertos por dentro e dois centroavantes.",
            p: "Estrutura extremamente simétrica e sólida, excelente para fechar os espaços entrelinhas.",
            c: "Falta profundidade e largura natural nas pontas, exigindo apoio constante dos laterais.",
            b: "Explore os espaços deixados pelos laterais quando eles sobem para tentar dar largura ao time."
          },
          "4231-n": {
            preset: "Possession / Controle Defensivo",
            d: "O clássico esquema de segurança com dois volantes, três meias ofensivos compactos (LAM, CAM, RAM) e um centroavante.",
            p: "Controle absoluto de jogo, posse de bola segura e intransponibilidade no miolo de zaga.",
            c: "Jogo pode se tornar engessado e previsível se o adversário fechar bem a entrada da área.",
            b: "Adote marcação em zona rigorosa e force o adversário a arriscar passes longos inofensivos."
          },
          "4231-w": {
            preset: "Counter-Press / Transição Aberta",
            d: "Mantém o duplo pivô e o centroavante, mas abre dois pontas legítimos (LM e RM) nas alas.",
            p: "Junta a solidez defensiva dos volantes com a amplitude agressiva dos pontas.",
            c: "Exige extrema dedicação defensiva dos pontas para fechar os espaços junto aos laterais.",
            b: "Supere o duplo pivô trocando passes rápidos em velocidade pelo centro com meias criativos."
          },
          "424": {
            preset: "Gegenpress / All-In Ofensivo",
            d: "Quatro atacantes fixos apoiados por apenas dois volantes e a linha de defesa.",
            p: "Pressão sufocante na saída de bola rival e volume ofensivo máximo.",
            c: "Buraco gigantesco no meio-campo; qualquer erro na pressão resulta em contra-ataque livre para o rival.",
            b: "Atraia a pressão tocando a bola curto na defesa e lance imediatamente nas costas dos volantes que sobem sozinhos."
          },
          "4312": {
            preset: "Short Passing / Tabela Central",
            d: "Três meio-campistas centrais, um armador central (CAM) e dois centroavantes.",
            p: "Excelente para reter a bola no campo ofensivo e envolver a zaga com passes curtos.",
            c: "Totalmente vulnerável a ataques rápidos pelas laterais do campo.",
            b: "Jogue com pontas rápidos e force o jogo pelas pontas onde o adversário não tem cobertura defensiva natural."
          },
          "4321": {
            preset: "Vertical Tiki-Taka / O Meta Competitivo",
            d: "Três meio-campistas com dois atacantes flutuantes (CFs) logo atrás de um centroavante.",
            p: "O esquema mais eficiente do jogo, unindo infiltrações mortais dos CFs com solidez defensiva ajustável.",
            c: "Exige ajustes manuais precisos nas instruções para não perder o controle das laterais.",
            b: "Utilize um duplo pivô compacto e evite dar espaço para os CFs girarem na entrada da área."
          },
          "433-flat": {
            preset: "Balanced / Equilíbrio Geral",
            d: "O desenho mais universal do futebol: linha de 4, trio de meio-campo plano, pontas abertos e centroavante.",
            p: "Distribuição homogênea de jogadores por todo o campo, facilitando qualquer estilo de jogo.",
            c: "Pode se tornar vulnerável se os três meias tiverem apenas funções passivas.",
            b: "Supere o meio-campo com superioridade numérica temporária vinda de descidas dos alas ou do segundo atacante."
          },
          "433-holding": {
            preset: "Possession / Segurança com Volante",
            d: "Variação da 4-3-3 com um volante de contenção fixo protegendo a zaga e dois meias à frente.",
            p: "Maior estabilidade defensiva em transições sem perder a largura dos pontas.",
            c: "O setor de criação pode ficar lento se o volante for excessivamente defensivo.",
            b: "Feche os espaços entre o volante fixo e os zagueiros para sufocar a saída de bola curta."
          },
          "433-defend": {
            preset: "Deep Block / Retranca com Pontas",
            d: "Dois volantes mais recuados e um meio-campista central, mantendo os pontas e o centroavante avançados.",
            p: "Excelente para segurar resultados contra equipes muito técnicas.",
            c: "Dificuldade acentuada para criar volume de jogo no ataque.",
            b: "Avance sua linha defensiva até o meio-campo e pressione a saída de bola sem medo."
          },
          "433-attack": {
            preset: "High Press / Pressão Ofensiva",
            d: "Um meio-campista avança para se alinhar ao ataque como um armador, deixando dois volantes na base.",
            p: "Grande presença de jogadores na zona de finalização adversária.",
            c: "Deixa um buraco perigoso na entrelinhas defensiva.",
            b: "Infiltra passes rápidos rasteiros no espaço deixado pelo meia que avançou para o ataque."
          },
          "433-false9": {
            preset: "Tiki-Taka / Falso 9 Clássico",
            d: "Centroavante recua para buscar jogo, atraindo zagueiros e abrindo caminho para os pontas.",
            p: "Posse de bola sufocante e extrema dificuldade de marcação individual para os zagueiros rivais.",
            c: "Ausência de um centroavante de referência física na grande área.",
            b: "Mantenha a linha defensiva recuada e por zona, proibindo os zagueiros de saírem da posição para caçar o falso 9."
          },
          "4411": {
            preset: "Balanced Counter / Bloco Duplo",
            d: "Duas linhas de quatro compactas com um segundo atacante flutuando atrás do centroavante.",
            p: "Solidez defensiva exemplar combinada com transições rápidas pelos lados.",
            c: "Pouca criatividade central se o segundo atacante for neutralizado.",
            b: "Use meias criativos entrelinhas para quebrar as duas linhas de quatro do adversário."
          },
          "442-flat": {
            preset: "Direct Counter / O Clássico Eficiente",
            d: "Duas linhas rígidas de quatro jogadores e uma dupla de ataque tradicional.",
            p: "Simples de executar, extremamente compacta e letal em contra-ataques verticais.",
            c: "O meio-campo central pode ser dominado por esquemas com três ou mais homens no setor.",
            b: "Sobrecargue o setor central com um trio de meio-campo móvel para forçar os alas rivais a fecharem o jogo."
          },
          "442-holding": {
            preset: "Balanced / Proteção Dupla",
            d: "Ajusta os dois meias centrais para funções de volantes de contenção, mantendo as linhas de quatro.",
            p: "Segurança defensiva máxima sem abrir mão da dupla de ataque.",
            c: "Pode faltar aproximação rápida para a construção de jogadas no campo ofensivo.",
            b: "Circule a bola com paciência pelos flancos e explore cruzamentos para vencer a altura dos volantes recuados."
          },
          "451": {
            preset: "Possession / Sufocamento Territorial",
            d: "Linha de cinco meio-campistas compactos sufocando o adversário com um único centroavante isolado.",
            p: "Impossível de perder a posse de bola no meio-campo se bem executada.",
            c: "Ataque totalmente isolado e dependente de subidas tardias dos meias.",
            b: "Mantenha a calma na defesa, feche os espaços centrais e utilize bolas longas para surpreender a retaguarda alta."
          },
          "5122": {
            preset: "Counter-Attack / Retranca com Dupla",
            d: "Linha defensiva de cinco com um volante central e dois atacantes de referência na frente.",
            p: "Muralha defensiva intransponível por dentro com duas opções claras de escape no ataque.",
            c: "Meio-campo defensivo isolado do ataque durante longos períodos do jogo.",
            b: "Pressione a saída de bola no campo adversário e force os alas a correrem para trás, desgastando-os fisicamente."
          },
          "5212": {
            preset: "Direct Counter / Transição Rápida",
            d: "Três zagueiros e dois alas, protegidos por dois volantes e armados por um CAM para servir dois centroavantes.",
            p: "Excelente equilíbrio entre fechar a defesa e contra-atacar com velocidade central e lateral.",
            c: "Espaços consideráveis entre o duplo pivô e o CAM se o time for empurrado para trás.",
            b: "Mantenha a posse de bola no campo ofensivo e use chutes de longa distância para furar o bloqueio duplo."
          },
          "5221": {
            preset: "Wing-Play Counter / Alas Ofensivos",
            d: "Defesa de cinco com dois volantes, dois meias/pontas abertos e um centroavante.",
            p: "Proteção lateral reforçada combinada com velocidade agigantada nas pontas.",
            c: "O meio-campo central sofre para conter equipes que tocam a bola rápido por dentro.",
            b: "Centralize o jogo com meias criativos e evite dar espaço para os pontas dispararem nas costas dos alas."
          },
          "523": {
            preset: "Heavy Counter / Muralha e Foguetes",
            d: "Trio de zagueiros, dois alas, dois volantes centrais e um trio de ataque rápido (ponta esquerda, ponta direita e centroavante).",
            p: "Defesa quase intransponível contra investidas centrais e contra-ataques devastadores com três homens na frente.",
            c: "Meio-campo central reduzido a dois jogadores, facilitando o domínio territorial do rival.",
            b: "Domine o círculo central com superioridade numérica de meio-campistas e cadastre a posse de bola."
          },
          "532": {
            preset: "Park the Bus / Bloco Defensivo Rígido",
            d: "Três zagueiros, dois alas, um trio de meio-campo compacto e dois centroavantes.",
            p: "Fechamento absoluto de todos os espaços centrais e lateral próximos à área.",
            c: "Ofensivamente pobre, dependendo de lances esporádicos de velocidade da dupla de ataque.",
            b: "Use cruzamentos venenosos, chutes de fora da área e mantenha uma linha alta para abafar qualquer tentativa de saída rápida."
          },
          "541": {
            preset: "Ultra Park the Bus / Retranca Total",
            d: "O nível máximo de segurança defensiva do FC 26: linha de 5 defensiva e linha de 4 intermediária.",
            p: "Praticamente impossível de ser penetrada por jogadas normais de toque de bola.",
            c: "Zero presença ofensiva; o time inteiro abdica de atacar.",
            b: "Tenha paciência extrema na circulação de bola, explore chutes colocados de longa distância e o recurso de cruzamentos na área para forçar erros defensivos."
          }
        };

        function atualizarPainel() {
          const f = document.getElementById("formacao-select").value;
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

          const d = matriz[f];
          if (d) {
            document.getElementById("preset-tag").innerText = d.preset;
            document.getElementById("info-descricao").innerText = d.d;
            document.getElementById("info-pros").innerText = d.p;
            document.getElementById("info-contras").innerText = d.c;
            document.getElementById("info-combate").innerText = d.b;
          }
        }
        window.onload = atualizarPainel;
      </script>
    </body>
    </html>
    """

    components.html(painel_html, height=560, scrolling=True)
