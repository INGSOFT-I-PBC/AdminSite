from django.db import models
from django.db import models
from .users import Employee
from .common import Status
from django.core.validators import MinValueValidator


class HistorialCaja(models.Model):
    """
    This model represent a History for cash desk closing.

    Args:
        models (Model): A Django's Model

    Attributes:
        cantidad_facturas (IntegerField):
            The quantity of invoice that are registered on a cash desk closing.

        fecha_cierre (DateTimeField):
            The instant in which the cash desk close happened.

        fecha_apertura (DateTimeField):
            The instant in which a cash desk is opening.
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    cantidad_facturas = models.IntegerField()
    created_by = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, db_column="created_by"
    )
    fecha_cierre = models.DateTimeField()
    fecha_apertura = models.DateTimeField()
    num_caja = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    valor_apertura = models.DecimalField(decimal_places=3, max_digits=10)
    valor_cierre = models.DecimalField(decimal_places=3, max_digits=10)

    un_cent = models.IntegerField(
        validators=[MinValueValidator(0)], name="1_centavo", default=0
    )
    cinco_cent = models.IntegerField(
        validators=[MinValueValidator(0)], name="5_centavo", default=0
    )
    diez_cent = models.IntegerField(
        validators=[MinValueValidator(0)], name="10_centavo", default=0
    )
    veinticinco_cent = models.IntegerField(
        validators=[MinValueValidator(0)], name="25_centavo", default=0
    )
    cincuenta_cent = models.IntegerField(
        validators=[MinValueValidator(0)], name="50_centavo", default=0
    )
    un_dolar_moneda = models.IntegerField(
        validators=[MinValueValidator(0)], name="1_dolar_moneda", default=0
    )
    un_dolar_billete = models.IntegerField(
        validators=[MinValueValidator(0)], name="1_dolar_billete", default=0
    )
    cinco_billete = models.IntegerField(
        validators=[MinValueValidator(0)], name="5_billete", default=0
    )
    diez_billete = models.IntegerField(
        validators=[MinValueValidator(0)], name="10_billete", default=0
    )
    veinte_billete = models.IntegerField(
        validators=[MinValueValidator(0)], name="20_billete", default=0
    )
    cincuenta_billete = models.IntegerField(
        validators=[MinValueValidator(0)], name="50_billete", default=0
    )
    dinero_fisico = models.DecimalField(
        validators=[MinValueValidator(0)], max_digits=13, decimal_places=3
    )
    dinero_faltante = models.DecimalField(max_digits=13, decimal_places=3)

    class Meta:
        db_table = "historial_caja"
