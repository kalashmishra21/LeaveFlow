from django.db import migrations


def add_default_leave_types(apps, schema_editor):
    LeaveType = apps.get_model('accounts', 'LeaveType')
    for name, days, description in [
        ('Casual Leave', 12, 'For personal matters'),
        ('Sick Leave', 10, 'For medical reasons'),
        ('Earned Leave', 15, 'Annual earned leave'),
        ('Emergency Leave', 5, 'For emergencies'),
    ]:
        LeaveType.objects.using(schema_editor.connection.alias).get_or_create(
            name=name, defaults={'default_days': days, 'description': description}
        )


class Migration(migrations.Migration):
    dependencies = [('accounts', '0003_chatmessage_attachment_chatmessage_attachment_name_and_more')]
    operations = [migrations.RunPython(add_default_leave_types, migrations.RunPython.noop)]
