import click

from crawler.util.config import Config
from crawler.news import aknews_crawler
from crawler.agents import akagents_crawler

def get_runner(runner: str):
    runners = {
        "agent": akagents_crawler,
        "news": aknews_crawler 
    }

    return runners[runner]

@click.command()
@click.option("--mode", default="prod", help="mode to run the program (prod/dev)")
@click.option("--save_img", default=False, help="download image locally (true/false)")
@click.option("--task", default="crawl", help="runner task (crawl/sync)")
@click.argument("runner")
def main(mode: str, save_img: bool, runner: str, task: str) -> None:

    Config.MODE = mode
    Config.SAVE_IMG = save_img
    
    _runner = get_runner(runner)
    _runner.run(task)

if __name__ == "__main__":
    print(f"{'='*10} Currently Supported Runners: agent/news {'='*10}")
    main()