"""Dashboard module providing main application navigation."""
import flet as ft


def dash_board(page: ft.Page):
    """Builds the application shell (sidebar + content) and opens the dashboard."""
    from services.database import crear_bd
    from views.layouts.app_layout import AppLayout

    # Validation: if the app shell is already mounted (e.g. a view calls
    # dash_board to "go back"), do not rebuild the layout - that would nest a
    # shell inside the content area and create an infinite navigation loop.
    existing_layout = getattr(page, "_app_layout", None)
    if existing_layout is not None:
        existing_layout.open_section("dashboard")
        return

    page.title = "Dagent"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.padding = 0
    page.controls.clear()
    crear_bd()

    layout = AppLayout(page)
    page.add(layout.build())
    layout.open_section("dashboard")
    page.update()


if __name__ == "__main__":
    def _run(page: ft.Page):
        dash_board(page)

    ft.run(_run)
