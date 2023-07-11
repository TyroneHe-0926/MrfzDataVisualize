import click

from crawler.news import aknews_crawler
from crawler.agents import akagents_crawler
from crawler.crawler import Task

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
    
    _runner = get_runner(runner)

    task = Task(
        name = task,
        mode=mode,
        save_img=save_img
    )

    _runner.dispatch(task)

if __name__ == "__main__":
    print(f"{'='*10} Currently Supported Runners: agent/news {'='*10}")
    main()