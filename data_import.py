import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alcomarket.settings")
django.setup()

from goods.models import Good


def import_data_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter='\t')
        for row in csv_reader:
            obj = Good(
                name=row['name'],
                description=row['description'],
                volume=row['volume'],
                stock=row['stock'],
                price=row['price'],
            )
            obj.save()


if __name__ == "__main__":
    csv_file_path = "data/goods.csv"
    import_data_from_csv(csv_file_path)
