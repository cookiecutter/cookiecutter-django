from django.db import migrations

def add_fruits(apps, schema_editor):
    Fruit = apps.get_model('fruit', 'Fruit')
    db_alias = schema_editor.connection.alias

    Fruit.objects.using(db_alias).create(
        name="Apple", description="Round, usually red or green", 
        detail_link="https://en.wikipedia.org/wiki/Apple",
        detail="An apple is an edible fruit produced by an apple tree (Malus domestica). Apple trees are cultivated worldwide and are the most widely grown species in the genus Malus. The tree originated in Central Asia, where its wild ancestor, Malus sieversii, is still found today. Apples have been grown for thousands of years in Asia and Europe and were brought to North America by European colonists. Apples have religious and mythological significance in many cultures, including Norse, Greek and European Christian tradition.\n\nSource: Wikipedia article \"Apple\", released under the Creative Commons Attribution-Share-Alike License 3.0.")

    Fruit.objects.using(db_alias).create(
        name="Pear", description="Tapered top, light green",
        detail_link="https://en.wikipedia.org/wiki/Pear",
        detail="The pear tree and shrub are a species of genus Pyrus, in the family Rosaceae, bearing the pomaceous fruit of the same name. Several species of pear are valued for their edible fruit and juices while others are cultivated as trees. The tree is medium-sized and native to coastal as well as mildly temperate regions of Europe, north Africa and Asia. Pear wood is one of the preferred materials in the manufacture of high-quality woodwind instruments and furniture.\n\nSource: Wikipedia article \"Pear\", released under the Creative Commons Attribution-Share-Alike License 3.0.")

    Fruit.objects.using(db_alias).create(
        name="Strawberry", description="Bright red, soft, covered in tiny seeds",
        detail_link="https://en.wikipedia.org/wiki/Strawberry",
        detail="The garden strawberry (or simply strawberry) is a widely grown hybrid species of the genus Fragaria, collectively known as the strawberries, which are cultivated worldwide for their fruit. The fruit is widely appreciated for its characteristic aroma, bright red color, juicy texture, and sweetness. It is consumed in large quantities, either fresh or in such prepared foods as jam, juice, pies, ice cream, milkshakes, and chocolates. Artificial strawberry flavorings and aromas are also widely used in products such as candy, soap, lip gloss, perfume, and many others.\n\nSource: Wikipedia article \"Strawberry\", released under the Creative Commons Attribution-Share-Alike License 3.0.")

def remove_fruits(apps, schema_editor):
    Fruit = apps.get_model('fruit', 'Fruit')
    db_alias = schema_editor.connection.alias
    Fruit.objects.filter(name='Apple').using(db_alias).delete()
    Fruit.objects.filter(name='Pear').using(db_alias).delete()
    Fruit.objects.filter(name='Strawberry').using(db_alias).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_fruits, remove_fruits),

    ]