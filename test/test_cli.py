#!/usr/bin/env python3
"""Test CLI to debug the issue"""

import click

@click.group()
def main():
    """Test CLI"""
    pass

@main.command()
@click.argument('times', nargs=-1, required=True)
def schedule(times):
    """Schedule sessions"""
    print(f"Times received: {list(times)}")

if __name__ == "__main__":
    main()