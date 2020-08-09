# Use to create tables in your local DynamoDB.

from horreum.db.terraform import ResourceTemplateDB

TABLE_LIST = [ResourceTemplateDB]
DYNAMODB_URL = "http://localhost:8000"

for table in TABLE_LIST:
    table.Meta.host = DYNAMODB_URL
    if table.exists():
        print(f"Table {table.Meta.table_name} already exists.")
        continue

    table.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    print(f"Table {table.Meta.table_name} created.")
