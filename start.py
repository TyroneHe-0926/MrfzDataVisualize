import click
from crawler.news import aknews_crawler
from crawler.agents import akagents_crawler

@click.command()
@click.option("--mode", default="prod", help="mode to run the program (prod/dev)")
@click.option("--save_img", default=False, help="download image locally (true/false)")
@click.argument("runner")
def main(mode, save_img, runner) -> None:
    if runner == "agent": akagents_crawler.run(mode=mode, save_img=save_img)

    if runner == "news": aknews_crawler.run(mode=mode, save_img=save_img)

if __name__ == "__main__":
    print(f"{'='*10} Currently Supported Runners: agent/news {'='*10}")
    main()