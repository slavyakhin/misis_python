import argparse
import pprint
from src.lab09.group import add_student, list_students, find_students, remove_students, update_student, stats
from src.lab08.models import format_student


DB = "data/lab09/students.csv"


def main():
    """
    cli for students csv db
    """

    parser = argparse.ArgumentParser(description="cli for students csv db")
    parser.add_argument("--db", default=DB, help="path to students csv")

    subparsers = parser.add_subparsers(dest="subcommand")

    # add
    add_parser = subparsers.add_parser("add", description="append student", help="append student")
    add_parser.add_argument("--fio", required=True, help="full name")
    add_parser.add_argument("--birthdate", required=True, default=None, help="ISO 8601 YYYY-MM-DD date")
    add_parser.add_argument("--group", required=True, default=None, help="student's group")
    add_parser.add_argument("--gpa", required=True, default=None, type=float, help="grade point average")

    # list
    list_parser = subparsers.add_parser("list", description="list students", help="list students")
    list_parser.add_argument("--sort", choices=['fio', 'gpa'], default=None, help="optional: sort by fio or gpa")

    # find
    find_parser = subparsers.add_parser("find", description="list students with substr in fio", help="list students with substr in fio")
    find_parser.add_argument("-q", "--substr", dest="substr", required=True, help="fio substring")

    # remove
    remove_parser = subparsers.add_parser("remove", description="remove student by fio, print removed count", help="remove student by fio, print removed count")
    remove_parser.add_argument("--fio", required=True)

    # update
    update_parser = subparsers.add_parser("update", description="find by fio, replace rec fields", help="find by fio, replace rec fields")
    update_parser.add_argument("--fio", required=True, help="target fio")
    update_parser.add_argument("--gpa", help="new gpa")
    update_parser.add_argument("--group", help="new group")
    update_parser.add_argument("--birthdate", help="new birthdate")

    # stats
    stats_parser = subparsers.add_parser("stats", description="print stats", help="print stats")


    args = parser.parse_args()

    match args.subcommand:
        case "add":
            # add_students validates rec
            add_student(args.db, {
                "fio": args.fio,
                "birthdate": args.birthdate,
                "group": args.group,
                "gpa": args.gpa,
                })

        case "list":
            for rec in list_students(args.db, sort_by=args.sort):
                print(format_student(rec))

        case "find":
            for rec in find_students(args.db, args.substr):
                print(format_student(rec))

        case "remove":
            print(remove_students(args.db, args.fio))

        case "update":
            fields = {
                k: v for k, v in [
                ("birthdate", args.birthdate),
                ("group", args.group),
                ("gpa", args.gpa)
                ] if v is not None
            }

            if not update_student(args.db, args.fio, **fields):
                raise ValueError("fio not found")

        case "stats":
            pprint.pp(stats(args.db), indent=2, expand=True)


if __name__ == "__main__":
    main()