#!/usr/bin/env python3
"""Simple debug CLI for testing Click alternative"""

def main():
    print("Debug CLI - Simple test")
    
def schedule(time):
    print(f"Scheduling for: {time}")

def list_schedules():
    print("List command")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'schedule' and len(sys.argv) > 2:
            schedule(sys.argv[2])
        elif cmd == 'list':
            list_schedules()
        else:
            main()
    else:
        main()