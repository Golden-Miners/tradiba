import argparse
import sys
from tradiba.dev.cli.new import register_new_command
from tradiba.dev.cli.doctor import register_doctor_command
from tradiba.dev.cli.validate import register_validate_command
from tradiba.dev.cli.benchmark import register_benchmark_command
from tradiba.dev.cli.release import register_release_command

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tradiba",
        description="Tradiba Developer CLI Tool"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    register_new_command(subparsers)
    register_doctor_command(subparsers)
    register_validate_command(subparsers)
    register_benchmark_command(subparsers)
    register_release_command(subparsers)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
        
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
