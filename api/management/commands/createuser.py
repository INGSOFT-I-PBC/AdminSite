from getpass import getpass

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db.utils import IntegrityError

from api.models import Employee, Group, Role, User


class Command(BaseCommand):
    help = "Register a new user on the system"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--username", type=str, default="")
        parser.add_argument(
            "--admin",
            action="store_true",
            help="Set if the user that will be created is an admin",
        )

    def handle(self, *args, **options):
        username = options["username"]
        if options["admin"]:
            create = input(
                r"WARNING: You\'ll create an admin user, proceed? [y/N] "
            ).lower()
            if create != "y":
                print("User not created")
                return
        while username == "":
            username = (
                input("Insert username: ").lower().lstrip().rstrip().replace(" ", "_")
            ).lstrip().rstrip()
        email = input("Email: ")
        name = input("Name: ")
        lastname = input("Lastname: ")
        document = input("ID Document: ")
        user_role = None
        user_group = None
        if options["admin"]:
            user_role = Role.objects.get(codename="sys.admin")
            user_group = Group.objects.get(codename="sys.admin")
            if not user_role:
                raise CommandError(
                    "Admin permission group is not registered on Database"
                )
        else:
            all_groups = Group.objects.all()
            if len(all_groups) == 0:
                raise Exception(
                    "There is no groups registered onto the system, aborting..."
                )
            print("Select a permission group: ")
            for i in range(len(all_groups)):
                group = all_groups[i]
                print(f"[{i}] {group.name} <{group.codename}>")

            while not user_group and len(all_groups) > 0:
                index = input("Insert number: ")
                if not index.isnumeric() or not (0 <= int(index) < len(all_groups)):
                    print("Incorrect value inserted")
                    continue
                user_group = all_groups[int(index)]

            all_roles = Role.objects.all()
            print(
                "*************************",
                "*  Role selection menu  *",
                "*************************",
            )
            role_quantity = len(all_roles)
            if role_quantity == 0:
                raise Exception("There is not roles registered on system, aborting...")
            for i in range(role_quantity):
                role = all_roles[i]
                print(f"- [{i}] {role.name}")

            while not user_role:
                selected = input("Insert selection: ")
                if not selected.isnumeric() or not (0 <= int(selected) < role_quantity):
                    print("Inserted value is not correct")
                    continue
                user_role = all_roles[int(selected)]
        employee_obj = None
        try:
            employee_obj = Employee(
                name=name, lastname=lastname, cid=document, role=user_role
            )
            employee_obj.save()
            password = getpass("Password: ")
            User(
                username=username,
                password=make_password(password),
                email=email,
                employee=employee_obj,
                group=user_group,
            ).save()
        except IntegrityError as e:
            print("ID Document is not valid, already registered")
            print(e)
            if employee_obj is not None:
                employee_obj.delete()
            return
        print(f"Successfully created user '{username}'")
