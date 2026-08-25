# ÁREA DE COMPARAÇÃO NO LADO ESQUERDO DO GRÁFICO (ÁREA AMARELA)
        col_comp_left, col_chart_right = st.columns([1, 2.5])

        with col_comp_left:
            st.markdown("#### ⚔️ Comparar Jogadores")
            st.caption("Adicione até 3 jogadores para comparar com o selecionado:")

            # CSS para colorir as bordas e rótulos de cada seletor com a cor do gráfico
            st.markdown("""
            <style>
                /* Jogador 1 - Azul */
                div[data-testid="stSelectbox"]:nth-of-type(1) label { color: #3b82f6 !important; font-weight: bold !important; }
                div[data-testid="stSelectbox"]:nth-of-type(1) div[data-baseweb="select"] > div { border: 2px solid #3b82f6 !important; }
                
                /* Jogador 2 - Verde */
                div[data-testid="stSelectbox"]:nth-of-type(2) label { color: #10b981 !important; font-weight: bold !important; }
                div[data-testid="stSelectbox"]:nth-of-type(2) div[data-baseweb="select"] > div { border: 2px solid #10b981 !important; }
                
                /* Jogador 3 - Amarelo */
                div[data-testid="stSelectbox"]:nth-of-type(3) label { color: #f59e0b !important; font-weight: bold !important; }
                div[data-testid="stSelectbox"]:nth-of-type(3) div[data-baseweb="select"] > div { border: 2px solid #f59e0b !important; }
            </style>
            """, unsafe_allow_html=True)

            other_players = ["Nenhum"] + [name for name in player_list if name != target_player_name]
            
            # 3 Selectboxes individuais (com limite de até 3 jogadores)
            comp1 = st.selectbox("🔵 Jogador Comparado 1:", options=other_players, index=0, key="comp_slot_1")
            
            # Habilita o segundo seletor apenas se o primeiro for selecionado
            options_p2 = ["Nenhum"] + [name for name in player_list if name not in [target_player_name, comp1]] if comp1 != "Nenhum" else ["Nenhum"]
            comp2 = st.selectbox("🟢 Jogador Comparado 2:", options=options_p2, index=0, key="comp_slot_2", disabled=(comp1 == "Nenhum"))
            
            # Habilita o terceiro seletor apenas se o segundo for selecionado
            options_p3 = ["Nenhum"] + [name for name in player_list if name not in [target_player_name, comp1, comp2]] if comp2 != "Nenhum" else ["Nenhum"]
            comp3 = st.selectbox("🟡 Jogador Comparado 3:", options=options_p3, index=0, key="comp_slot_3", disabled=(comp2 == "Nenhum"))

            compared_players = [p for p in [comp1, comp2, comp3] if p != "Nenhum"]

        with col_chart_right:
            if selected_stats_map:
                radar_labels = list(selected_stats_map.keys())
                theta_labs = radar_labels + [radar_labels[0]]

                fig = go.Figure()

                # 1. Jogador Principal (Red)
                radar_values = [get_val(p, csv_col) for csv_col in selected_stats_map.values()]
                r_vals = radar_values + [radar_values[0]]

                fig.add_trace(go.Scatterpolar(
                    r=r_vals,
                    theta=theta_labs,
                    mode='lines+markers',
                    fill='none',
                    line=dict(color='#ef4444', width=3),
                    marker=dict(size=8, color='#ef4444'),
                    name=f"{p['Name']} (Principal)"
                ))

                # Mapeamento fixo de cores correspondente aos seletores (Azul, Verde, Amarelo)
                slot_colors = {'comp_slot_1': '#3b82f6', 'comp_slot_2': '#10b981', 'comp_slot_3': '#f59e0b'}
                active_slots = [('comp_slot_1', comp1), ('comp_slot_2', comp2), ('comp_slot_3', comp3)]

                # 2. Jogadores Selecionados para Comparação
                for slot_key, comp_name in active_slots:
                    if comp_name != "Nenhum":
                        comp_row = df[df['Name'] == comp_name].iloc[0]
                        comp_radar_values = [get_val(comp_row, csv_col) for csv_col in selected_stats_map.values()]
                        comp_r_vals = comp_radar_values + [comp_radar_values[0]]
                        color = slot_colors[slot_key]

                        fig.add_trace(go.Scatterpolar(
                            r=comp_r_vals,
                            theta=theta_labs,
                            mode='lines+markers',
                            fill='none',
                            line=dict(color=color, width=2.5, dash='solid'),
                            marker=dict(size=7, color=color),
                            name=f"{comp_row['Name']} ({comp_row['OVR']})"
                        ))

                fig.update_layout(
                    title=dict(
                        text=f"Análise Comparativa Radar: {p['Name']} (OVR: {p['OVR']})",
                        font=dict(color='#ffffff', size=16)
                    ),
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            tickfont=dict(color='#cbd5e1'),
                            gridcolor='#334155'
                        ),
                        angularaxis=dict(
                            tickfont=dict(color='#ffffff', size=13),
                            gridcolor='#334155'
                        )
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=480,
                    margin=dict(l=30, r=30, t=50, b=40),
                    legend=dict(
                        font=dict(color='#f8fafc'),
                        orientation="h",
                        yanchor="bottom",
                        y=-0.18,
                        xanchor="center",
                        x=0.5
                    )
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Marque pelo menos uma estatística para exibir o gráfico.")
