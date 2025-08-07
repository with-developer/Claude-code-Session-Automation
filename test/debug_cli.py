#!/usr/bin/env python3

import click

@click.group()
def main():
    pass

@main.command() 
@click.argument('time')
def schedule(time):
    print(f"Scheduling for: {time}")

@main.command()
def list():
    print("List command")

if __name__ == '__main__':
    main()