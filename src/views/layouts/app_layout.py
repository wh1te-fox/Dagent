"""General application layout: collapsible sidebar, top bar, and content area."""
import flet as ft

EXPANDED_WIDTH = 245
COLLAPSED_WIDTH = 78

BADGE_STYLES = {
    "Pendiente": ft.Colors.AMBER_600,
    "En desarrollo": ft.Colors.DEEP_PURPLE_400,
}


class ContentProxy:
    """Adapter that redirects the view API (page.controls, page.add, etc.)
    to the content area of the layout instead of the whole page."""

    def __init__(self, page, content):
        object.__setattr__(self, "_page", page)
        object.__setattr__(self, "_content", content)

    @property
    def controls(self):
        return self._content.controls

    def add(self, *controls):
        self._content.controls.extend(controls)

    def update(self):
        self._page.update()

    def __getattr__(self, name):
        return getattr(self._page, name)

    def __setattr__(self, name, value):
        if name in ("_page", "_content"):
            object.__setattr__(self, name, value)
        elif name in ("padding", "vertical_alignment", "horizontal_alignment"):
            setattr(self._content, name, value)
        else:
            setattr(self._page, name, value)


class AppLayout:
    """Application shell with navigation sidebar, section header, and content area."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.expanded = True
        self.active_key = "dashboard"
        self.sections = self._build_sections()
        # Register this layout on the page so views can detect that the
        # application shell already exists and avoid rebuilding it (no nesting).
        setattr(page, "_app_layout", self)

    def _build_sections(self):
        """Maps sidebar entries to real views. Entries without an implementation
        are marked with a status badge and render a pending placeholder."""
        from views import dashboard_view, pending_view
        from views.add_client import customer_page
        from views.credits_view import credits_page
        from views.add_product import main as add_product_view
        from views.cash_view import show as cash_view
        from views.inventory_view import inventory_page
        from views.page_sale import input_sale
        from views.report_view import list_report
        from views.search_client import search as client_search_view
        from views.ui_settings import dark_mode

        return [
            {
                "key": "dashboard",
                "label": "Dashboard",
                "icon": ft.Icons.DASHBOARD_OUTLINED,
                "selected_icon": ft.Icons.DASHBOARD,
                "view": dashboard_view.show,
            },
            {
                "key": "pos",
                "label": "Punto de venta",
                "icon": ft.Icons.SHOPPING_CART_OUTLINED,
                "selected_icon": ft.Icons.SHOPPING_CART,
                "view": input_sale,
            },
            {
                "key": "products",
                "label": "Productos",
                "icon": ft.Icons.INVENTORY_2_OUTLINED,
                "selected_icon": ft.Icons.INVENTORY_2,
                "view": add_product_view,
            },
            {
                "key": "inventory",
                "label": "Inventario",
                "icon": ft.Icons.STORAGE_OUTLINED,
                "selected_icon": ft.Icons.STORAGE,
                "view": inventory_page,
            },
            {
                "key": "clients",
                "label": "Clientes",
                "icon": ft.Icons.PEOPLE_ALT_OUTLINED,
                "selected_icon": ft.Icons.PEOPLE_ALT,
                "view": customer_page,
            },
            {
                "key": "client_search",
                "label": "Búsqueda de clientes",
                "icon": ft.Icons.PERSON_SEARCH_OUTLINED,
                "selected_icon": ft.Icons.PERSON_SEARCH,
                "view": client_search_view,
            },
            {
                "key": "credits",
                "label": "Créditos y cuentas por cobrar",
                "icon": ft.Icons.CREDIT_CARD_OUTLINED,
                "selected_icon": ft.Icons.CREDIT_CARD,
                "view": credits_page,
            },
            {
                "key": "cash",
                "label": "Caja",
                "icon": ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
                "selected_icon": ft.Icons.ACCOUNT_BALANCE_WALLET,
                "view": cash_view,
            },
            {
                "key": "reports",
                "label": "Reportes",
                "icon": ft.Icons.ASSESSMENT_OUTLINED,
                "selected_icon": ft.Icons.ASSESSMENT,
                "view": list_report,
            },
            {
                "key": "settings",
                "label": "Configuración",
                "icon": ft.Icons.SETTINGS_OUTLINED,
                "selected_icon": ft.Icons.SETTINGS,
                "view": dark_mode,
            },
        ]

    def build(self):
        """Assembles the shell and returns the root control."""
        self.header_title = ft.Text("", size=20, weight=ft.FontWeight.W_800, expand=True)
        self.content_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        header = ft.Container(
            content=self.header_title,
            padding=ft.Padding.symmetric(vertical=24, horizontal=40),
            border=ft.Border.only(
                bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.12, ft.Colors.GREY))
            ),
        )

        content_area = ft.Container(
            content=ft.Column([header, self.content_column], spacing=0, expand=True),
            expand=True,
        )

        self.sidebar = self._build_sidebar()
        self.shell = ft.Row(
            [self.sidebar, content_area], spacing=0, expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        return self.shell

    # ------------------------------------------------------------------ sidebar

    def _build_sidebar(self):
        toggle_button = ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="Expandir barra lateral" if not self.expanded else "Contraer barra lateral",
            icon_size=20,
            on_click=self._toggle_sidebar,
        )

        # When the sidebar is collapsed there is not enough width for the logo
        # and the name next to the toggle button, so show only the button to
        # avoid overflowing the sidebar border.
        if self.expanded:
            header_children = [
                ft.Image(
                    src="assets/logo.png",
                    width=30,
                    height=30,
                    fit="contain",
                ),
                ft.Text(
                    "Dagent",
                    size=18,
                    weight=ft.FontWeight.W_900,
                    expand=True,
                ),
                toggle_button,
            ]
        else:
            header_children = [toggle_button]

        header = ft.Row(
            header_children,
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        items = ft.Column(
            [self._nav_item(section) for section in self.sections],
            spacing=4,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        return ft.Container(
            width=EXPANDED_WIDTH if self.expanded else COLLAPSED_WIDTH,
            padding=12,
            content=ft.Column([header, ft.Container(height=8), items], spacing=0, expand=True),
            border=ft.Border.only(
                right=ft.BorderSide(1, ft.Colors.with_opacity(0.12, ft.Colors.GREY))
            ),
        )

    def _nav_item(self, section):
        active = section["key"] == self.active_key
        label = section["label"]
        accent = ft.Colors.BLUE_400 if active else ft.Colors.GREY_700

        children = [
            ft.Icon(
                section["selected_icon"] if active else section["icon"],
                color=accent,
                size=22,
            )
        ]

        if self.expanded:
            children.append(
                ft.Text(
                    label,
                    size=14,
                    color=accent,
                    weight=ft.FontWeight.BOLD if active else ft.FontWeight.W_500,
                    max_lines=2,
                    expand=True,
                )
            )
            badge_color = BADGE_STYLES.get(section.get("badge"))
            if badge_color:
                children.append(
                    ft.Container(
                        content=ft.Text(
                            section["badge"],
                            size=10,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.W_700,
                        ),
                        bgcolor=badge_color,
                        border_radius=20,
                        padding=ft.Padding.symmetric(vertical=2, horizontal=8),
                    )
                )

        return ft.Container(
            content=ft.Row(children, spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            tooltip=label if not self.expanded else None,
            bgcolor=(
                ft.Colors.with_opacity(0.12, ft.Colors.BLUE_400) if active else None
            ),
            border_radius=10,
            padding=ft.Padding.symmetric(vertical=11, horizontal=12),
            ink=True,
            on_click=lambda e, key=section["key"]: self.open_section(key),
        )

    def _toggle_sidebar(self, e=None):
        self.expanded = not self.expanded
        self.sidebar = self._build_sidebar()
        self.shell.controls[0] = self.sidebar
        self.page.update()

    # ------------------------------------------------------------------ routing

    def open_section(self, key):
        """Marks the section as active and renders its view in the content area."""
        # Re-entrancy validation: a view could trigger another navigation while
        # it is being rendered. Ignore nested calls so the app never loops.
        if getattr(self, "_opening", False):
            return

        section = next((s for s in self.sections if s["key"] == key), None)
        if section is None:
            return

        self._opening = True
        try:
            self.active_key = key
            self.header_title.value = section["label"]
            self.sidebar = self._build_sidebar()
            self.shell.controls[0] = self.sidebar

            self.content_column.controls.clear()
            proxy = ContentProxy(self.page, self.content_column)
            section["view"](proxy)
            self.page.update()
        finally:
            self._opening = False
