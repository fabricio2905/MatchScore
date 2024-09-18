import flet as ft

def exibir_chaveamento(torneio_id, controller, page: ft.Page):
    page.title = "Chaveamento do Torneio"
    
    torneio = controller.torneios.get(torneio_id)

    nome_torneio = torneio["nome"]
    premiacao = torneio["premiacao"]

    participantes = controller.obter_participantes(torneio_id)
    if len(participantes) == 8:
        quartas_finais = [
            (participantes[0], participantes[1]),
            (participantes[2], participantes[3]),
            (participantes[4], participantes[5]),
            (participantes[6], participantes[7]),
        ]
    elif len(participantes) == 4:
        semi_finais = [
            (participantes[0], participantes[1]),
            (participantes[2], participantes[3]),
        ]
    elif len(participantes) == 2:
        finais = [
            (participantes[0], participantes[1]),
        ]

    vencedores_quartas = [" ", " ", " ", " "] if len(participantes) == 8 else []
    vencedores_semi = [" ", " "] if len(participantes) >= 4 else []
    vencedor_final = " "

    def editar_vencedor(participante, fase, posicao):
        nonlocal vencedor_final
        confronto_id = None

        if fase == "quartas":
            vencedores_quartas[posicao] = participante
            confronto_id = controller.obter_confronto_id_por_fase(torneio_id, "quartas", posicao)

        elif fase == "semis":
            vencedores_semi[posicao] = participante
            confronto_id = controller.obter_confronto_id_por_fase(torneio_id, "semis", posicao)

        elif fase == "final":
            vencedor_final = participante
            confronto_id = controller.obter_confronto_id_por_fase(torneio_id, "final", posicao)

        if confronto_id:
            controller.atualizar_vencedor(torneio_id, confronto_id, participante)

        reconstruir_interface()

    def criar_fase(partidas, titulo_fase, fase, pos_inicial=0):
        return ft.Column(
            [
                ft.Text(titulo_fase, size=18),
                *[ft.Container(
                    content=ft.Column([
                        ft.ElevatedButton(
                            text=partida[0],
                            on_click=lambda e, p=partida[0], f=fase, pos=pos_inicial + i: editar_vencedor(p, f, pos),
                            width=140,  
                            height=40
                        ),
                        ft.Text("VS"),
                        ft.ElevatedButton(
                            text=partida[1],
                            on_click=lambda e, p=partida[1], f=fase, pos=pos_inicial + i: editar_vencedor(p, f, pos),
                            width=140,  
                            height=40
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=10,
                ) for i, partida in enumerate(partidas)],
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def reconstruir_interface():
        page.controls.clear()

        fases = []

        if len(participantes) == 8:
            semi_finais_local = [
                (vencedores_quartas[0], vencedores_quartas[1]),
                (vencedores_quartas[2], vencedores_quartas[3]),
            ]
            final = (vencedores_semi[0], vencedores_semi[1])

            # Adiciona quartas de finais à esquerda
            fases.append(criar_fase(quartas_finais[:2], "Quartas de Final", "quartas", 0))

            # Adiciona semifinais à esquerda da final
            fases.append(criar_fase(semi_finais_local[:1], "Semifinal", "semis", 0))

            # Adiciona a final no centro
            fases.append(
                ft.Column(
                    [
                        ft.Text("Final", size=18),
                        ft.Container(
                            content=ft.Column([
                                ft.ElevatedButton(
                                    text=final[0] if final[0] != " " else " ",
                                    on_click=lambda e, p=final[0], f="final", pos=0: editar_vencedor(p, f, 0),
                                    width=140,  
                                    height=40
                                ),
                                ft.Text("VS"),
                                ft.ElevatedButton(
                                    text=final[1] if final[1] != " " else " ",
                                    on_click=lambda e, p=final[1], f="final", pos=1: editar_vencedor(p, f, 1),
                                    width=140,  
                                    height=40
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=10,
                        ),
                        ft.Text(f"Vencedor: {vencedor_final if vencedor_final != ' ' else 'A definir'}", size=18),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=200  
                )
            )

            # Adiciona semifinais à direita da final
            fases.append(criar_fase(semi_finais_local[1:], "Semifinal", "semis", 1))

            # Adiciona quartas de finais à direita
            fases.append(criar_fase(quartas_finais[2:], "Quartas de Final", "quartas", 2))

        elif len(participantes) == 4:
            final = (vencedores_semi[0], vencedores_semi[1])

            # Adiciona semifinal à esquerda da final
            fases.append(criar_fase(semi_finais[:1], "Semifinal", "semis", 0))

            # Adiciona a final no centro
            fases.append(
                ft.Column(
                    [
                        ft.Text("Final", size=18),
                        ft.Container(
                            content=ft.Column([
                                ft.ElevatedButton(
                                    text=final[0] if final[0] != " " else " ",
                                    on_click=lambda e, p=final[0], f="final", pos=0: editar_vencedor(p, f, 0),
                                    width=140,  
                                    height=40
                                ),
                                ft.Text("VS"),
                                ft.ElevatedButton(
                                    text=final[1] if final[1] != " " else " ",
                                    on_click=lambda e, p=final[1], f="final", pos=1: editar_vencedor(p, f, 1),
                                    width=140,  
                                    height=40
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=10,
                        ),
                        ft.Text(f"Vencedor: {vencedor_final if vencedor_final != ' ' else 'A definir'}", size=18),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=200 
                )
            )

            #semifinal à direita da final
            fases.append(criar_fase(semi_finais[1:], "Semifinal", "semis", 1))

        elif len(participantes) == 2:
            final = finais[0]
            fases.append(
                ft.Column(
                    [
                        ft.Text("Final", size=18),
                        ft.Container(
                            content=ft.Column([
                                ft.ElevatedButton(
                                    text=final[0],
                                    on_click=lambda e, p=final[0], f="final", pos=0: editar_vencedor(p, f, 0),
                                    width=140,  
                                    height=40
                                ),
                                ft.Text("VS"),
                                ft.ElevatedButton(
                                    text=final[1],
                                    on_click=lambda e, p=final[1], f="final", pos=1: editar_vencedor(p, f, 1),
                                    width=140,  
                                    height=40
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=10,
                        ),
                        ft.Text(f"Vencedor: {vencedor_final if vencedor_final != ' ' else 'A definir'}", size=24),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        page.add(
            ft.Column(
                controls=[
                    ft.Text(nome_torneio, size=28),
                    ft.Text(f"Premiação: {premiacao}", size=18),
                    ft.Row(
                        controls=fases,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()


    reconstruir_interface()
