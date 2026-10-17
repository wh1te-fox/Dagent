"""Shared scaffolding helpers to keep every section visually consistent.

All sections render into the layout's content column, which is the only
place with vertical scrolling; these helpers avoid nested scrolls and
standardize headers, cards, tables, and empty states.
"""
import flet as ft

ACCENT = ft.Colors.BLUE_400
CONTENT_WIDTH = 900
RESULTS_WIDTH = 640
FORM_WIDTH = 460
GREY_BORDER = ft.Colors.with_opacity(0.15, ft.Colors.GREY)


def setup(page, title):
    """Standardizes page-level settings and clears the section content."""
    page.title = title
    page.padding = ft.Padding.symmetric(vertical=32, horizontal=40)
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.controls.clear()
    return page


def header(icon, title, subtitle=None):
    """Standard section header: tinted icon badge + title."""
    title_column = ft.Column(
        [ft.Text(title, size=24, weight=ft.FontWeight.W_900)]
        + ([ft.Text(subtitle, size=13, color=ft.Colors.GREY_600)] if subtitle else []),
        spacing=2,
    )
    return ft.Row(
        [
            ft.Container(
                content=ft.Icon(icon, size=26, color=ACCENT),
                bgcolor=ft.Colors.with_opacity(0.08, ACCENT),
                border_radius=12,
                padding=10,
            ),
            title_column,
        ],
        spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def card(content, width=CONTENT_WIDTH, padding=24):
    """Standard bordered container used for forms, tables, and lists."""
    return ft.Container(
        content=content,
        width=width,
        padding=padding,
        border_radius=12,
        border=ft.Border.all(1, GREY_BORDER),
    )


def input(label, width=350, icon=None):
    """Standard text input: fixed width, rounded border, optional icon."""
    field = ft.TextField(label=label, width=width, border_radius=10)
    if icon:
        field.prefix_icon = icon
    return field


def buttons_row(controls):
    """Standard action buttons row: centered and wrapped for narrow windows."""
    return ft.Row(
        controls=controls,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        run_spacing=10,
        wrap=True,
    )


def result_card(content, width=RESULTS_WIDTH, padding=16):
    """Standard tinted card for list items (products, clients, movements)."""
    return ft.Container(
        content=content,
        width=width,
        padding=padding,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.04, ACCENT),
    )


def stat_card(label, value, icon, color):
    """Standard summary card for counters and totals."""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icon, size=28, color=color),
                ft.Column(
                    [
                        ft.Text(value, size=20, weight=ft.FontWeight.W_900),
                        ft.Text(label, size=12, color=ft.Colors.GREY_600),
                    ],
                    spacing=2,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=16,
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.07, color),
        width=210,
    )


def empty_state(message, icon=ft.Icons.INBOX_OUTLINED):
    """Standard empty/no-results placeholder."""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icon, color=ft.Colors.GREY_500),
                ft.Text(message, color=ft.Colors.GREY_600),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=30,
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY),
    )


def table_wrapper(table, width=None):
    """Wraps wide tables in the only horizontal scroll allowed per section."""
    return ft.Container(
        content=ft.Row([table], scroll=ft.ScrollMode.AUTO),
        width=width or CONTENT_WIDTH,
    )


def spacer(height=16):
    """Standard vertical spacing between blocks."""
    return ft.Container(height=height)


def primary_button(button):
    """Applies the standard accent style to an existing button."""
    button.bgcolor = ACCENT
    button.color = ft.Colors.WHITE
    button.height = 45
    button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    return button


def secondary_button(button):
    """Standard neutral style for action buttons: rounded border and fixed height."""
    button.height = max(button.height or 45, 45)
    button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    return button
