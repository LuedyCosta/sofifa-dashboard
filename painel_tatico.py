# Arquivo: painel_tatico.py
import streamlit.components.v1 as components

def renderizar_painel_tatico():
    painel_tatico_html = """
    # Arquivo: painel_tatico.py
import streamlit.components.v1 as components

def renderizar_painel_tatico():
    painel_tatico_html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
    <meta charset="UTF-8">
    <style>
        body {
            background-color: #000000;
            color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .pitch {
            background-color: #15803d;
            border: 3px solid #ffffff;
            border-radius: 10px;
            width: 100%;
            max-width: 600px;
            height: 420px;
            position: relative;
            box-sizing: border-box;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        .center-line {
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 2px;
            background-color: rgba(255, 255, 255, 0.7);
        }
        .center-circle {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 90px;
            height: 90px;
            border: 2px solid rgba(255, 255, 255, 0.7);
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }
        .penalty-area-top {
            position: absolute;
            top: 0;
            left: 25%;
            width: 50%;
            height: 60px;
            border: 2px solid rgba(255, 255, 255, 0.7);
            border-top: none;
        }
        .penalty-area-bottom {
            position: absolute;
            bottom: 0;
            left: 25%;
            width: 50%;
            height: 60px;
            border: 2px solid rgba(255, 255, 255, 0.7);
            border-bottom: none;
        }
        .player {
            width: 34px;
            height: 34px;
            background-color: #ef4444;
            color: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: bold;
            position: absolute;
            transform: translate(-50%, -50%);
            border: 2px solid #ffffff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.6);
            transition: transform 0.2s;
        }
        .player:hover {
            transform: translate(-50%, -50%) scale(1.15);
            cursor: pointer;
            background-color: #10b981;
        }
        .gk {
            background-color: #f59e0b;
        }
    </style>
    </head>
    <body>
        <div class="pitch">
            <!-- Linhas do Campo -->
            <div class="center-line"></div>
            <div class="center-circle"></div>
            <div class="penalty-area-top"></div>
            <div class="penalty-area-bottom"></div>
            
            <!-- Goleiro -->
            <div class="player gk" style="bottom: 3%; left: 50%;">GL</div>
            
            <!-- Linha Defensiva -->
            <div class="player" style="bottom: 22%; left: 18%;">LE</div>
            <div class="player" style="bottom: 18%; left: 38%;">ZAG</div>
            <div class="player" style="bottom: 18%; left: 62%;">ZAG</div>
            <div class="player" style="bottom: 22%; left: 82%;">LD</div>
            
            <!-- Meio-Campo -->
            <div class="player" style="bottom: 42%; left: 32%;">VOL</div>
            <div class="player" style="bottom: 42%; left: 68%;">VOL</div>
            <div class="player" style="top: 35%; left: 50%;">MEI</div>
            
            <!-- Ataque -->
            <div class="player" style="top: 18%; left: 20%;">PE</div>
            <div class="player" style="top: 12%; left: 50%;">ATA</div>
            <div class="player" style="top: 18%; left: 80%;">PD</div>
        </div>
    </body>
    </html>
    """
    components.html(painel_tatico_html, height=500, scrolling=False)
    """
    components.html(painel_tatico_html, height=520, scrolling=True)
