import argparse
import sys

from .services import TaskService
from .storage import JsonStorage


def build_parser():
    parser = argparse.ArgumentParser(prog="taskflow")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Añadir una tarea")
    add.add_argument("title")
    add.add_argument("--priority", default="medium")
    add.add_argument("--due", default=None)

    ls = sub.add_parser("list", help="Listar tareas")
    ls.add_argument("--pending", action="store_true")
    ls.add_argument("--by-priority", action="store_true")

    done = sub.add_parser("done", help="Completar tarea")
    done.add_argument("id", type=int)

    rm = sub.add_parser("delete", help="Borrar tarea")
    rm.add_argument("id", type=int)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    service = TaskService(JsonStorage())

    if args.command == "add":
        task = service.add(args.title, args.priority, args.due)
        print(f"Tarea #{task.id} creada")
    elif args.command == "list":
        tasks = service.list(
            include_done=not args.pending, sort_by_priority=args.by_priority
        )
        for t in tasks:
            mark = "x" if t.done else " "
            print(f"[{mark}] #{t.id} ({t.priority}) {t.title}")
    elif args.command == "done":
        service.complete(args.id)
        print(f"Tarea #{args.id} completada")
    elif args.command == "delete":
        service.delete(args.id)
        print(f"Tarea #{args.id} borrada")
    return 0


if __name__ == "__main__":
    sys.exit(main())
