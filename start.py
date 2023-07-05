#TODO add arg parser

import click

@click.command()
@click.option("--mode", default="prod", help="mode to run the program (prod/dev)")
@click.option("--save_img", default=False, help="download image locally")
def main() -> None:
    pass