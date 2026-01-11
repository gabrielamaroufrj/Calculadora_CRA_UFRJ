import flet as ft


def parse_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def parse_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


class Disciplina:
    def __init__(self, on_delete, on_change):
        self.nome = ft.TextField(
            label="Disciplina",
            expand=True
        )

        self.peso = ft.TextField(
            label="Créditos",
            keyboard_type="number",
            on_change=on_change
        )

        self.nota = ft.TextField(
            label="Nota",
            keyboard_type="number",
            on_change=on_change
        )

        self.view = ft.Container(
            padding=10,
            border=ft.border.all(1, "grey300"),
            border_radius=10,
            content=ft.Column(
                controls=[
                    self.nome,
                    ft.Row(
                        controls=[self.peso, self.nota],
                        spacing=10
                    ),
                    ft.TextButton(
                        "Remover disciplina",
                        style=ft.ButtonStyle(color="red"),
                        on_click=lambda e: on_delete(self)
                    )
                ],
                spacing=10
            )
        )


def main(page: ft.Page):
    page.title = "Simulador de CR"
    page.scroll = "adaptive"
    page.padding = 15

    disciplinas = []

    txt_total_creditos = ft.TextField(
        label="Créditos Totais Acumulados",
        keyboard_type="number",
        on_change=lambda e: calcular_cr()
    )

    txt_cr_atual = ft.TextField(
        label="CR Atual",
        keyboard_type="number",
        on_change=lambda e: calcular_cr()
    )

    resultado = ft.Text(
        "Aguardando cálculo...",
        size=18,
        weight="bold"
    )

    lista = ft.Column(spacing=10)

    def calcular_cr():
        total_antigo = parse_int(txt_total_creditos.value)
        cr_atual = parse_float(txt_cr_atual.value)

        soma = 0
        pesos = 0

        for d in disciplinas:
            peso = parse_int(d.peso.value)
            nota = parse_float(d.nota.value)

            if peso > 0:
                soma += peso * nota
                pesos += peso

        if total_antigo + pesos > 0:
            novo_cr = (total_antigo * cr_atual + soma) / (total_antigo + pesos)
        else:
            novo_cr = 0

        resultado.value = f"Novo CR Estimado: {novo_cr:.4f}"
        resultado.color = "green" if novo_cr >= cr_atual else "red"

        page.update()

    def adicionar_disciplina(e=None):
        d = Disciplina(
            on_delete=remover_disciplina,
            on_change=lambda e: calcular_cr()
        )
        disciplinas.append(d)
        lista.controls.append(d.view)
        page.update()

    def remover_disciplina(d):
        disciplinas.remove(d)
        lista.controls.remove(d.view)
        calcular_cr()

    page.add(
        ft.Text("Calculadora de CR", size=24, weight="bold"),
        txt_total_creditos,
        txt_cr_atual,
        ft.FilledButton("Adicionar Disciplina", on_click=adicionar_disciplina),
        ft.Text("Disciplinas:", size=18),
        lista,
        ft.Container(
            content=resultado,
            padding=12,
            bgcolor="grey200",
            border_radius=10
        )
    )

    adicionar_disciplina()


if __name__ == "__main__":
    ft.run(main)

