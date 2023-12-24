import click


@click.command()
@click.option('--option1', is_flag=True, help='Enable Option 1')
@click.option('--option2', is_flag=True, help='Enable Option 2')
def menu(option1, option2):
    """This script demonstrates a simple CLI menu."""
    click.echo('Welcome to the CLI Menu!')

    while True:
        click.echo('\nMenu:')
        click.echo('1. Option 1')
        click.echo('2. Option 2')
        click.echo('3. Quit')

        choice = click.prompt('Enter your choice (1, 2, or 3)', type=int)

        if choice == 1:
            click.echo('You selected Option 1')
            if option1:
                click.echo('Option 1 is enabled!')
        elif choice == 2:
            click.echo('You selected Option 2')
            if option2:
                click.echo('Option 2 is enabled!')
        elif choice == 3:
            click.echo('Goodbye!')
            break
        else:
            click.echo('Invalid choice. Please enter 1, 2, or 3.')
