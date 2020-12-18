from conf.settings import model_tables


def get_table_info(model_name: str):
    return model_tables.get(model_name, None)


def get_table_name(model_name: str):
    return get_table_info(model_name).get('name')


def get_table_columns(model_name: str):
    return get_table_info(model_name).get('columns')


def get_table_column_name(model_name: str, column_name: str):
    cols = get_table_columns(model_name)
    if column_name not in cols:
        raise KeyError(f'No such column name "{column_name}"')
    return cols.get(column_name)


def get_column_address(model_name: str, column_name: str):
    get_table_column_name(model_name, column_name)
    return f'{get_table_name(model_name)}.{get_table_column_name(model_name, column_name)}'
