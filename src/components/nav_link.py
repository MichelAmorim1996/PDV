from components import ft

@ft.component
def NavLink(label, path):
    active = ft.is_route_active(path)
    return ft.Container(
        content=ft.Text(
            label,

            weight=(
                ft.FontWeight.BOLD
                if active
                else ft.FontWeight.NORMAL
            ),

            color=(
                ft.Colors.BLUE
                if active
                else ft.Colors.ON_SURFACE
            ),
            size=20
        ),

        bgcolor=(
            ft.Colors.BLUE_50
            if active
            else None
        ),

        padding=ft.Padding.symmetric(
            horizontal=16,
            vertical=8
        ),

        border_radius=8,

        on_click=lambda:
            ft.context.page.navigate(path),
    )