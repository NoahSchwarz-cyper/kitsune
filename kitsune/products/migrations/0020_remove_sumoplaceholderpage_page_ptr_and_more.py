# Generated by Django 4.2.16 on 2024-10-14 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0019_alter_singleproductindexpage_body"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sumoplaceholderpage",
            name="page_ptr",
        ),
        migrations.DeleteModel(
            name="SingleProductIndexPage",
        ),
        migrations.DeleteModel(
            name="SumoPlaceholderPage",
        ),
    ]
