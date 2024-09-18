import flet as ft
from viewChaveamento import exibir_chaveamento
from controller import TorneioController

def main_view(page: ft.Page):
    controller = TorneioController(db_path="torneio.db")

    page.title = "Match Score"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    error_message = ft.Text(value="", color="red")

    def continuar(e):
        nome = nome_torneio.value
        premiacao = premiacao_input.value
        num_participantes = num_participantes_dropdown.value

        if not nome:
            error_message.value = "O nome do torneio é obrigatório!"
            page.update()
            return
        if not num_participantes:
            error_message.value = "O número de participantes é obrigatório!"
            page.update()
            return

        error_message.value = ""
        page.update()

        torneio_id = controller.criar_torneio(nome, premiacao, int(num_participantes))
        participants_view(torneio_id, int(num_participantes), controller, page)

    nome_torneio = ft.TextField(label="Nome do Torneio")
    premiacao_input = ft.TextField(label="Premiação")
    num_participantes_dropdown = ft.Dropdown(
        label="Número de Participantes",
        options=[
            ft.dropdown.Option("2"),
            ft.dropdown.Option("4"),
            ft.dropdown.Option("8"),
        ]
    )
    continuar_button = ft.ElevatedButton("Continuar", on_click=continuar)

    page.add(
        ft.Column(
            controls=[
                ft.Text("Match Score", size=40),
                nome_torneio,
                premiacao_input,
                num_participantes_dropdown,
                continuar_button,
                error_message
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def participants_view(torneio_id, num_participantes, controller, page: ft.Page):
    participantes_inputs = []

    for i in range(0, num_participantes, 2):
        row_inputs = []
        row_inputs.append(ft.TextField(label=f"Participante {i + 1}", width=500))
        if i + 1 < num_participantes:
            row_inputs.append(ft.TextField(label=f"Participante {i + 2}", width=500))
        participantes_inputs.append(ft.Row(controls=row_inputs, alignment=ft.MainAxisAlignment.CENTER))

    def ir_para_chaveamento(e):
        participantes = [input.value for row in participantes_inputs for input in row.controls]
        for participante in participantes:
            if participante:
                controller.adicionar_participante(torneio_id, participante)
        controller.gerar_confrontos(torneio_id)
        exibir_chaveamento(torneio_id, controller, page)

    continuar_button = ft.ElevatedButton("Ir ao Chaveamento", on_click=ir_para_chaveamento)

    page.controls.clear()
    page.add(
        ft.Column(
            controls=[
                ft.Text("Insira o nome dos participantes", size=30),
                *participantes_inputs,
                continuar_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()
