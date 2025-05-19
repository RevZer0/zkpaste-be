import typer

from src.application import container

cli_app = typer.Typer()

@cli_app.command('delete-expired')
def delete_expired_paste():
    handler = container.handlers.paste_delete_expired.provided()
    handler.handle()


if __name__ == '__main__':
    cli_app()

