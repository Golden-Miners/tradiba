import argparse
from typing import Any
import os

def handle_new(args: argparse.Namespace) -> None:
    project_type = args.type
    name = args.name
    
    print(f"Scaffolding new {project_type} project: {name}")
    
    # Simple simulated scaffolding logic
    if not os.path.exists(name):
        os.makedirs(name)
        
    init_file = os.path.join(name, "__init__.py")
    with open(init_file, "w") as f:
        f.write(f"# Tradiba {project_type} project: {name}\n")
        
    print(f"Success! Generated project at ./{name}/")

def register_new_command(subparsers: Any) -> None:
    parser = subparsers.add_parser("new", help="Scaffold a new project")
    parser.add_argument("type", choices=["strategy", "indicator", "broker", "plugin"], help="Type of project")
    parser.add_argument("name", help="Name of the project")
    parser.set_defaults(func=handle_new)
