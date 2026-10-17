"""Dashboard view with a general summary of the business data."""
import flet as ft
from views.components import section

LOW_STOCK_LIMIT = 5


def _safe(call, default):
    try:
        return call()
    except Exception:
        return default


def _section_title(icon, text, color=section.ACCENT):
    return ft.Row(
        [
            ft.Icon(icon, color=color),
            ft.Text(text, size=18, weight=ft.FontWeight.BOLD, color=color),
        ],
        spacing=10,
    )


def _dashboard_header(title, subtitle):
    logo_image = ft.Image(
        src="assets/logo.png",
        width=26,
        height=26,
        fit="contain",
    )
    return ft.Row(
        [
            ft.Container(
                content=logo_image,
                bgcolor=ft.Colors.with_opacity(0.08, section.ACCENT),
                border_radius=12,
                padding=10,
            ),
            ft.Column(
                [
                    ft.Text(title, size=24, weight=ft.FontWeight.W_900),
                    ft.Text(subtitle, size=13, color=ft.Colors.GREY_600),
                ],
                spacing=2,
            ),
        ],
        spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def _list_row(icon, title, detail, value, color):
    return section.result_card(
        ft.Row(
            [
                ft.Icon(icon, size=18, color=color),
                ft.Text(title, size=14, expand=True),
                ft.Text(detail, size=12, color=ft.Colors.GREY_600),
                ft.Text(value, size=14, weight=ft.FontWeight.BOLD, color=color),
            ],
            spacing=15,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=section.CONTENT_WIDTH,
        padding=ft.Padding.symmetric(vertical=10, horizontal=16),
    )


def show(page):
    """Renders the dashboard with quick counters and a basic business summary."""
    from services.database import (
        obtener_clientes,
        obtener_creditos,
        obtener_productos,
        obtener_resumen_creditos,
        obtener_ventas,
    )

    section.setup(page, "Dashboard")

    ventas = _safe(obtener_ventas, [])
    productos = _safe(obtener_productos, [])
    clientes = _safe(obtener_clientes, [])
    creditos = _safe(obtener_creditos, [])
    _, _, pendiente, activos = _safe(obtener_resumen_creditos, (0, 0, 0, 0))

    total_ingresos = sum(venta[6] for venta in ventas)
    unidades_vendidas = sum(venta[2] for venta in ventas)
    bajo_stock = [producto for producto in productos if producto[5] <= LOW_STOCK_LIMIT]

    counters_row = ft.Row(
        [
            section.stat_card("Ventas registradas", str(len(ventas)), ft.Icons.RECEIPT_LONG_OUTLINED, section.ACCENT),
            section.stat_card("Productos", str(len(productos)), ft.Icons.INVENTORY_2_OUTLINED, ft.Colors.GREEN_400),
            section.stat_card("Clientes", str(len(clientes)), ft.Icons.PEOPLE_OUTLINE, ft.Colors.AMBER_400),
            section.stat_card("Créditos", f"{activos}/{len(creditos)}", ft.Icons.CREDIT_CARD, ft.Colors.DEEP_PURPLE_400),
        ],
        spacing=15,
        run_spacing=15,
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        width=section.CONTENT_WIDTH,
    )

    money_row = ft.Row(
        [
            section.stat_card("Ingresos totales", f"${total_ingresos:.2f}", ft.Icons.PAYMENTS_OUTLINED, ft.Colors.GREEN_400),
            section.stat_card("Unidades vendidas", str(unidades_vendidas), ft.Icons.STACKED_LINE_CHART, section.ACCENT),
            section.stat_card("Saldo por cobrar", f"${pendiente:.2f}", ft.Icons.REQUEST_QUOTE_OUTLINED, ft.Colors.RED_400),
            section.stat_card("Bajo stock", str(len(bajo_stock)), ft.Icons.WARNING_AMBER_OUTLINED, ft.Colors.ORANGE_400),
        ],
        spacing=15,
        run_spacing=15,
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        width=section.CONTENT_WIDTH,
    )

    if ventas:
        recent_items = [
            _list_row(ft.Icons.RECEIPT, f"{venta[1]} (x{venta[2]})", str(venta[7]), f"${venta[6]:.2f}", ft.Colors.GREEN_400)
            for venta in ventas[:5]
        ]
    else:
        recent_items = [section.empty_state("Aún no hay ventas registradas")]

    if bajo_stock:
        stock_items = []
        for producto in bajo_stock:
            agotado = producto[5] <= 0
            color = ft.Colors.RED_400 if agotado else ft.Colors.ORANGE_400
            stock_items.append(
                _list_row(
                    ft.Icons.INVENTORY_2_OUTLINED,
                    f"{producto[2]} ({producto[1]})",
                    "sin existencias" if agotado else "existencia baja",
                    "AGOTADO" if agotado else f"{producto[5]} uds",
                    color,
                )
            )
    else:
        stock_items = [
            section.empty_state(
                f"Sin productos con existencia menor o igual a {LOW_STOCK_LIMIT}",
                icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
            )
        ]

    page.add(
        _dashboard_header("Resumen general", "Estado actual de las operaciones del negocio"),
        section.spacer(20),
        counters_row,
        section.spacer(12),
        money_row,
        section.spacer(40),
        _section_title(ft.Icons.HISTORY, "Ventas recientes"),
        section.spacer(10),
        ft.Column(recent_items, spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        section.spacer(20),
        _section_title(ft.Icons.PRODUCTION_QUANTITY_LIMITS_OUTLINED, "Productos por agotarse", ft.Colors.ORANGE_400),
        section.spacer(10),
        ft.Column(stock_items, spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        section.spacer(20),
    )
    page.update()
