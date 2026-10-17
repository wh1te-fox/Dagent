"""Credits and accounts receivable management view module."""
import flet as ft
from views.components import section
from views.menu_interface import dash_board
from services.database import (
    obtener_creditos,
    obtener_resumen_creditos,
    registrar_abono,
)


def credits_page(page: ft.Page):
    """Renders the credits list with balances and payment registration."""
    section.setup(page, "Créditos y Cuentas por Cobrar")

    search_field = section.input("Buscar por cliente o descripción", icon=ft.Icons.SEARCH)

    message_text = ft.Text("", size=14)
    results_column = ft.Column(
        [],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def cargar_stats():
        total, cobrado, pendiente, activos = obtener_resumen_creditos()
        return [
            section.stat_card("Total a crédito", f"${total:.2f}", ft.Icons.REQUEST_QUOTE, ft.Colors.DEEP_PURPLE_400),
            section.stat_card("Total cobrado", f"${cobrado:.2f}", ft.Icons.PAID, ft.Colors.GREEN_400),
            section.stat_card("Saldo pendiente", f"${pendiente:.2f}", ft.Icons.BALANCE, ft.Colors.RED_400),
            section.stat_card("Créditos con saldo", str(activos), ft.Icons.CREDIT_CARD, section.ACCENT),
        ]

    summary_row = ft.Row([], spacing=15, run_spacing=15, wrap=True, alignment=ft.MainAxisAlignment.CENTER)

    def make_credit_card(cred):
        cred_id, _cli_id, nombre, apellido, monto, descripcion, fecha, pagado = cred
        cliente = f"{nombre} {apellido}" if nombre else "Sin asignar"
        saldo = monto - pagado
        if pagado >= monto - 1e-9:
            saldo = 0.0

        card_container = section.result_card(ft.Column(spacing=8))

        paid_badge = ft.Container(
            content=ft.Text(
                "PAGADO",
                size=10,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.W_700,
            ),
            bgcolor=ft.Colors.GREEN_500,
            border_radius=20,
            padding=ft.Padding.symmetric(vertical=3, horizontal=10),
        )
        date_text = ft.Text(fecha[:10], size=13, color=ft.Colors.GREY_600)

        abono_input = section.input("Monto a abonar", width=200)

        def save_click(e):
            try:
                monto_val = float(abono_input.value.strip()) if abono_input.value else 0
                registrar_abono(cred_id, monto_val)
                message_text.value = f"Abono registrado a {cliente}"
                message_text.color = "green"
                perform_search()
            except (ValueError, TypeError) as error:
                abono_input.error_text = str(error)
                page.update()

        abono_input = section.input("Monto a abonar", width=200)

        def build_edit_mode(e=None):
            abono_input.error_text = None
            abono_input.label = f"Monto a abonar (Saldo: ${saldo:.2f})"
            card_container.content = ft.Column([
                ft.Row([
                    ft.Text(f"Crédito de {cliente} - Saldo: ${saldo:.2f}", size=13, color=ft.Colors.GREY_700),
                ], alignment=ft.MainAxisAlignment.END),
                ft.Row([abono_input], alignment=ft.MainAxisAlignment.END),
                ft.Row([
                    section.primary_button(ft.Button("Guardar", on_click=save_click, icon=ft.Icons.SAVE)),
                    section.secondary_button(ft.Button("Cancelar", on_click=lambda e: build_view_mode(), icon=ft.Icons.CANCEL)),
                ], alignment=ft.MainAxisAlignment.END, spacing=10),
            ], spacing=8)
            page.update()

        def build_view_mode():
            actions = []
            if saldo > 0:
                actions.append(
                    section.secondary_button(ft.Button("Registrar abono", on_click=build_edit_mode, icon=ft.Icons.PAYMENTS))
                )
            info = [
                ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, color=ft.Colors.DEEP_PURPLE_400),
                        ft.Text(cliente, weight=ft.FontWeight.BOLD, size=16),
                    ], spacing=10),
                    paid_badge if saldo <= 0 else date_text,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text(descripcion or "Sin descripción", size=13, color=ft.Colors.GREY_700, expand=True),
                    ft.Text(f"Crédito: ${monto:.2f}", size=13, color=section.ACCENT, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Abonado: ${pagado:.2f}", size=13, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        f"Saldo: ${saldo:.2f}",
                        size=13,
                        color=ft.Colors.RED_700 if saldo > 0 else ft.Colors.GREEN_700,
                        weight=ft.FontWeight.BOLD,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ]
            if actions:
                info.append(section.buttons_row(actions))
            card_container.content = ft.Column(info, spacing=8)

        build_view_mode()
        return card_container

    def perform_search(e=None):
        termino = (search_field.value or "").strip().lower()
        message_text.value = ""
        results_column.controls.clear()

        creditos = obtener_creditos()

        if termino:
            creditos = [
                c for c in creditos
                if termino in f"{c[2]} {c[3]}".lower() or termino in (c[5] or "").lower()
            ]

        summary_row.controls = cargar_stats()

        if not creditos:
            message_text.value = "No se encontraron créditos"
            message_text.color = "red"
            results_column.controls.append(
                section.empty_state("No hay créditos registrados", ft.Icons.CREDIT_CARD_OFF)
            )
        else:
            message_text.value = f"Se encontraron {len(creditos)} crédito(s)"
            message_text.color = "green"
            for cred in creditos:
                card = make_credit_card(cred)
                results_column.controls.append(ft.Row([card], alignment=ft.MainAxisAlignment.CENTER))

        page.update()

    search_field.on_change = perform_search

    def go_dashboard(e):
        dash_board(page)

    def go_nuevo_credito(e):
        from views.add_credit import credit_page
        credit_page(page)

    btn_nuevo = section.secondary_button(ft.Button("Registrar Nuevo Crédito", on_click=go_nuevo_credito, icon=ft.Icons.ADD_CIRCLE, height=45))
    btn_close = section.secondary_button(ft.Button("Cerrar", on_click=go_dashboard, icon=ft.Icons.ARROW_BACK, height=45))

    page.add(
        section.header(
            ft.Icons.CREDIT_CARD,
            "Créditos y Cuentas por Cobrar",
            "Registra abonos y da seguimiento a las cuentas por cobrar",
        ),
        section.spacer(16),
        summary_row,
        section.spacer(16),
        section.buttons_row([btn_nuevo, btn_close, search_field]),
        section.spacer(10),
        message_text,
        section.spacer(10),
        results_column,
    )

    perform_search()
    page.update()
