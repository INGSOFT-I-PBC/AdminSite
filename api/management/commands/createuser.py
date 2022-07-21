from django.core.management.base import BaseCommand, CommandError, CommandParser
from api.models import Employee, Role, User
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password
from getpass import getpass


class Command(BaseCommand):
    help = "Register a new user on the system"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--username", type=str, default="")
        parser.add_argument(
            "--admin", action="store_true", help="Set if the user that will be created is an admin"
        )

    def handle(self, *args, **options):
        username = options["username"]
        if options["admin"]:
            create = input(r"WARNING: You\'ll create an admin user, proceed? [y/N] ").lower()
            if create != "y":
                print("User not created")
                return
        while username == "":
            username = input("Insert username: ").lower().lstrip().rstrip().replace(" ", "_")
        email = input("Email: ")
        name = input("Name: ")
        lastname = input("Lastname: ")
        document = input("ID Document: ")
        user_role = None
        if options["admin"]:
            user_role = Role.objects.get(nick="sys.admin")
            if not user_role:
                raise CommandError("Admin rol is not registered on Database")
        else:
            all_roles = Role.objects.all()
            print("Select a role: ")
            for i in range(len(all_roles)):
                role = all_roles[i]
                print(f"[{i}] {role}")
            while not user_role and len(all_roles) > 0:
                index = input("Insert number: ")
                if not index.isnumeric() or not (0 <= int(index) < len(all_roles)):
                    print("Incorrect value inserted")
                    continue
                user_role = all_roles[int(index)]
        try:
            employee_obj = Employee(name=name, lastname=lastname, cid=document, role=user_role)
            employee_obj.save()
            password = getpass("Password: ")
            User(
                username=username,
                password=make_password(password),
                email=email,
                is_admin=options["admin"],
                employee=employee_obj,
            ).save()
        except IntegrityError as e:
            print("ID Document is not valid, already registered")
            print(e)
            return
        print(f"Successfully created user '{username}'")
