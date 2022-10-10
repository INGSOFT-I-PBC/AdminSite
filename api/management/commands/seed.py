from argparse import ArgumentParser
from random import random, randint

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models import Model
from faker import Faker
from faker.providers.company import Provider as CompanyProvider
from faker.providers.geo.en_US import Provider as GeoProvider
from faker.providers.misc.en_US import MiscProvider
from faker.providers.person.es_MX import PersonProvider

from api.models import Warehouse, common, Employee, Role, Group, User, Category, CategoryParam, Item, ItemMetaData

faker = Faker()
active_status = common.Status.objects.filter(name="active").first()


class Command(BaseCommand):
    help = "Seed database for testing and development"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--warehouses", action="store_true")
        parser.add_argument("--items", action="store_true")
        parser.add_argument("--items-category", action="store_true")
        parser.add_argument("--users", action="store_true")
        parser.add_argument("--cities", action="store_true")
        parser.add_argument("--province", action="store_true")
        parser.add_argument("--times", type=int, action="store")
        parser.add_argument("--force-meta", action="store_true")

    def handle(self, *args, **options):
        self.stdout.write("Starting seeding...")
        if options['times'] < 1:
            self.stderr.write('bad value for times')
            return
        self.stdout.write(f"{options}")
        for i in range(options['times']):
            if options['warehouses']:
                self.stdout.write('generating warehouse')
                generate_warehouses(self)
            if options['items']:
                self.stdout.write('generating items')
                generate_items(self, options['force_meta'])
            if options['users']:
                self.stdout.write('generating users')
                generate_users(self)
            if options['items_category']:
                self.stdout.write('generating items categories')
                generate_categories(self)

        # run_seed(self)
        self.stdout.write("done.")


def run_seed(self):
    warehouse_list = []
    active = common.Status.objects.filter(name="active").first()
    for i in range(20):
        warehouse = Warehouse(
            name=f"Warehouse #{i}", longitude=random(), latitude=random() * randint(-10, 10), status=active
        )
        warehouse.save()


def generate_warehouses(cmd: Command):
    cp = CompanyProvider(faker)
    g = GeoProvider(faker)
    Warehouse(
        name=cp.company(),
        latitude=g.latitude(),
        longitude=g.longitude(),
        status=active_status
    ).save()


def generate_users(cmd):
    p = PersonProvider(faker)

    role = Role.objects.filter(codename='general.user').first()
    group = Group.objects.filter(codename='generic.user').first()
    if group is None:
        group = Group(
            codename='generic.user',
            name='Usuario General',
        )
        group.save()

    while True:
        name = p.name()
        lastname = p.last_name()

        cid = ''
        usrname = name.lower()[0] + lastname.lower().replace(' ', '')
        for i in range(10):
            cid += f'{p.random_digit()}'
        emp = None
        usr = None
        try:
            emp = Employee(
                name=name,
                lastname=lastname,
                role=role,
                is_active=True,
                cid=cid
            )
            emp.save()
            usr = User(
                is_active=True,
                employee=emp,
                password=make_password('123456789'),
                username=usrname,
                email=f'{usrname}@jhon-doe.com',
                group=group,
            )
            usr.save()
            break
        except IntegrityError as e:
            if emp is not None and emp.id is not None:
                emp.delete()
            if usr is not None and usr.id is not None:
                usr.delete()


def generate_items(cmd, force_meta=False):
    if force_meta:
        categories = Category.objects.filter(categoryparam__isnull=False)
    else:
        categories = Category.objects.all()
    if categories.count() == 0:
        generate_categories(cmd)
        categories = Category.objects.all()

    cat = categories[randint(0, categories.count() - 1)]
    root = Employee.objects.filter(name='root').first()
    if root is None:
        root = Employee(
            name='root',
            lastname='sysuser',
            is_active=True,
            role=Role.objects.filter(codename='sys.admin').first(),
            cid='999'
        )
        root.save()
        User(
            employee=root,
            username='root',
            is_active=True,
            email='root@system',
            password=make_password('123456789'),
            group=Group.objects.filter(codename='sys.admin').first(),
        ).save()
    while True:
        item = None
        try:
            name: str = faker.word()
            item = Item(
                category=cat,
                name=name,
                status=active_status,
                brand=faker.word(),
                iva=random() * 0.12836234,
                price=(random() + 0.001753) * randint(5, 1000),
                model=faker.word(),
                codename=f'{name}.{faker.word()}.{cat.name}'.lower().replace(' ', '_'),
                created_by=root
            )
            item.save()
            break
        except IntegrityError as e:
            safe_delete(item)
            cmd.stdout.write(f'err-item: {e}')
    catpam = CategoryParam.objects.filter(category=cat)

    for param in catpam:
        value = None
        imd = None
        try:
            field_type = param.field_type
            match field_type:
                case 'str' | 'string' | 's':
                    value = faker.word()
                case 'number' | 'int' | 'float' | 'f' | 'i' | 'n':
                    value = f'{faker.random_int()}'
                case other:
                    value = 'undefined'
            imd = ItemMetaData(
                item=item,
                param=param,
                value=value
            )
            imd.save()
        except IntegrityError as e:
            safe_delete(imd)
            cmd.stdout.write(f'cannot generate meta data: {e}')


def generate_categories(cmd):
    types = ['str', 'number']
    p = MiscProvider(faker)
    cat = None
    cp = None
    try:
        cat = Category(
            name=faker.word(),
            description=faker.sentence(),
            short_name=faker.word(),
            status=active_status,
        )
        cat.save()
        for i in range(randint(1, 10)):
            field_type = types[p.random_int(0, 1)]
            default = faker.word() if field_type == 'str' else f"{p.random_int()}"
            cp = CategoryParam(
                required=False,
                category=cat,
                field=faker.word(),
                field_type=field_type,
                default_value=default,
            )
            cp.save()
    except IntegrityError as e:
        safe_delete(cp)
        safe_delete(cat)
        cmd.stdout.write(f'err while generating category: {e}')


def generate_cities(cmd):
    pass


def safe_delete(obj: Model):
    if obj is not None and obj.pk is not None:
        obj.delete()
