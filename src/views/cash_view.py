"""Cash view with a daily cut summary based on registered sales."""
import flet as ft
from datetime import date
from services.database import obtener_ventas
from views.components import section


def show(page):
    """Renders the daily cash cut computed from the registered sales."""
    section.setup(page, "Caja")

    hoy = date.today().isoformat()
    ventas_hoy = obtener_ventas("fecha", hoy)
    ventas_mes = obtener_ventas("mes")
    ventas_semana = obtener_ventas("semana")

    total_hoy = sum(sale[6] for sale in ventas_hoy)
    total_semana = sum(sale[6] for sale in ventas_semana)
    total_mes = sum(sale[6] for sale in ventas_mes)

    summary_row = ft.Row(
        [
            section.stat_card("Cobrado hoy", f"${total_hoy:.2f}", ft.Icons.PAYMENTS_OUTLINED, ft.Colors.GREEN_400),
            section.stat_card(f"Ventas de hoy ({len(ventas_hoy)})", str(sum(sale[2] for sale in ventas_hoy)), ft.Icons.SHOPPING_CART_OUTLINED, section.ACCENT),
            section.stat_card("Última semana", f"${total_semana:.2f}", ft.Icons.CALENDAR_VIEW_WEEK, ft.Colors.AMBER_400),
            section.stat_card("Este mes", f"${total_mes:.2f}", ft.Icons.CALENDAR_MONTH_OUTLINED, ft.Colors.DEEP_PURPLE_400),
        ],
        spacing=15,
        run_spacing=15,
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    movements_column = ft.Column([], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    if not ventas_hoy:
        movements_title = None
        movements_column.controls.append(
            section.empty_state("Aún no hay ventas registradas hoy", ft.Icons.EVENT_BUSY_OUTLINED)
        )
    else:
        movements_title = ft.Row(
            [
                ft.Icon(ft.Icons.HISTORY, color=section.ACCENT),
                ft.Text("Últimos movimientos del día", size=20, weight=ft.FontWeight.BOLD, color=section.ACCENT),
            ],
            spacing=10,
        )
        for sale in reversed(ventas_hoy[-10:]):
            movements_column.controls.append(
                section.result_card(
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.RECEIPT, size=18, color=section.ACCENT),
                            ft.Text(f"{sale[1]} (x{sale[2]})", size=14, expand=True),
                            ft.Text(f"{sale[7]}", size=12, color=ft.Colors.GREY_600),
                            ft.Text(
                                f"${sale[6]:.2f}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_400,
                            ),
                        ],
                        spacing=15,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
            )

    controls = [
        section.header(ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, "Corte de caja", f"Resumen del día {hoy} según las ventas registradas"),
        section.spacer(16),
        summary_row,
        section.spacer(16),
    ]
    if movements_title:
        controls.extend([movements_title, section.spacer(8)])
    controls.append(movements_column)

    page.add(*controls)
    page.update()
