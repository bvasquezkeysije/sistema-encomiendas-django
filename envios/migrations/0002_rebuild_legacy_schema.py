from django.db import migrations


def _table_columns(schema_editor, table_name: str) -> set[str]:
    connection = schema_editor.connection
    if table_name not in connection.introspection.table_names():
        return set()
    with connection.cursor() as cursor:
        description = connection.introspection.get_table_description(cursor, table_name)
    return {col.name for col in description}


def _drop_table(schema_editor, table_name: str) -> None:
    vendor = schema_editor.connection.vendor
    if vendor == "postgresql":
        schema_editor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
    else:
        schema_editor.execute(f'DROP TABLE IF EXISTS "{table_name}"')


def rebuild_legacy_schema(apps, schema_editor):
    # Legacy symptom in production: rutas_ruta exists without 'codigo'.
    rutas_columns = _table_columns(schema_editor, "rutas_ruta")
    legacy_schema = "rutas_ruta" in schema_editor.connection.introspection.table_names() and "codigo" not in rutas_columns
    if not legacy_schema:
        return

    Cliente = apps.get_model("clientes", "Cliente")
    Ruta = apps.get_model("rutas", "Ruta")
    Empleado = apps.get_model("envios", "Empleado")
    Encomienda = apps.get_model("envios", "Encomienda")
    HistorialEstado = apps.get_model("envios", "HistorialEstado")

    # Drop dependent tables first.
    _drop_table(schema_editor, HistorialEstado._meta.db_table)

    # M2M through table for Empleado.rutas_asignadas (auto-generated).
    m2m_table = Empleado._meta.get_field("rutas_asignadas").remote_field.through._meta.db_table
    _drop_table(schema_editor, m2m_table)

    _drop_table(schema_editor, Encomienda._meta.db_table)
    _drop_table(schema_editor, Empleado._meta.db_table)
    _drop_table(schema_editor, Ruta._meta.db_table)
    _drop_table(schema_editor, Cliente._meta.db_table)

    # Recreate schema aligned with current model state.
    schema_editor.create_model(Cliente)
    schema_editor.create_model(Ruta)
    schema_editor.create_model(Empleado)
    schema_editor.create_model(Encomienda)
    schema_editor.create_model(HistorialEstado)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("envios", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(rebuild_legacy_schema, reverse_code=noop_reverse),
    ]

