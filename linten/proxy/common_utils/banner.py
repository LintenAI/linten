from typing import Final

# Linten ASCII banner
LINTEN_BANNER: Final = """   ██╗     ██╗████████╗███████╗██╗     ██╗     ███╗   ███╗
   ██║     ██║╚══██╔══╝██╔════╝██║     ██║     ████╗ ████║
   ██║     ██║   ██║   █████╗  ██║     ██║     ██╔████╔██║
   ██║     ██║   ██║   ██╔══╝  ██║     ██║     ██║╚██╔╝██║
   ███████╗██║   ██║   ███████╗███████╗███████╗██║ ╚═╝ ██║
   ╚══════╝╚═╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝"""


def show_banner():
    """Display the Linten CLI banner."""
    try:
        import click

        click.echo(f"\n{LINTEN_BANNER}\n")
    except ImportError:
        print("\n")  # noqa: T201
