import os
import click
import ML.utils.configuration as configuration
import ML.train as training


@click.group()
def run():
    pass


@run.command()
@click.option('--config', '-cgf',
              type=click.Path(exists=True, resolve_path=True),
              help='Configuration file.')
def train(config):
    cfg = configuration.load_config(config)
    training.train(cfg)


def main():
    run()


if __name__ == '__main__':
    train()
