import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

import django

django.setup()

from queryIntention.models import MemberFeature


def populate_from_csv(csv_name='static/datafiles/sample10.csv'):
    print('populating sample data from file: {}'.format(csv_name))
    with open(csv_name) as f:
        field_names = f.readline().strip().split(',')
        for line in f:
            values = line.strip().split(',')
            fields = zip(field_names, values)
            key_value_pairs = dict()
            for field_name, value in fields:
                if field_name == 'memberId':
                    key_value_pairs[field_name] = int(value)
                elif value != 'NULL':
                    key_value_pairs[field_name] = float(value)

            member_feature = MemberFeature.objects.create(**key_value_pairs)
            member_feature.save()


if __name__ == '__main__':
    populate_from_csv()
