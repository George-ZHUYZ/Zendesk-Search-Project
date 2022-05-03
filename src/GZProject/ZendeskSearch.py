import os
import sys
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_datetime64_ns_dtype
import inflect


# DB query APIs
def print_formatted_result(result):
    n_ordinal = inflect.engine()

    if result.empty:
        print('Search {0} for {1} with a value of {2}\nNo results found'.format(query_table, query_column,
                                                                                query_value[1]))
    else:
        columns = list(result.columns)
        for i in range(len(result)):
            for j in range(len(columns)):
                print('{0}: {1}\n'.format(columns[j], result.iloc[i, j]))
            print('====== End of the %s result ======' % n_ordinal.ordinal(i + 1))


def get_column_type(target_df, column):
    if column in target_df.columns:
        if is_string_dtype(target_df[column]):
            return 'string'
        elif is_numeric_dtype(target_df[column]):
            return 'int'
        elif is_datetime64_ns_dtype(target_df[column]):
            return 'datetime'
        else:
            return 'unknown'
    else:
        return 'unknown'


def equal_query(target_df, column, column_type, value):
    if column_type == 'int':
        try:
            value = int(value)
        except ValueError:
            return pd.DataFrame()

    return target_df[target_df[column] == value]


def like_query(target_df, column, value):
    return target_df[target_df[column].str.contains(value, na=False)]


def parse_query(input_2, input_3, input_4):
    CONST_TABLES_DICT = {1: ['users', 'users'], 2: ['tickets', 'tickets'], 3: ['orgs', 'organizations']}

    target_df = globals()['df_' + CONST_TABLES_DICT[input_2][0] + '_full']

    global query_table
    query_table = CONST_TABLES_DICT[input_2][1]

    global query_column
    query_column = input_3

    global query_value
    query_value = input_4.split('@@')

    if query_column not in target_df.columns or query_value[1] == '':
        # Return empty result if the search column is invalid or the search value is null
        return pd.DataFrame()

    column_type = get_column_type(target_df, query_column)

    if query_value[0] == 'equal':
        return equal_query(target_df, query_column, column_type, query_value[1])
    elif query_value[0] == 'like':
        if column_type == 'int':
            # Return empty result if try to search int column with like values
            return pd.DataFrame()
        return like_query(target_df, query_column, query_value[1])
    # To-DO: Add more type of query functions, and also will support multiple columns query

# End: DB query APIs


def populate_org_dict(target_df):
    result = {}

    for i in range(len(target_df)):
        org_id = target_df.loc[i, 'organization_id']
        org_id = int(org_id) if not pd.isnull(org_id) else 0

        if org_id in result:
            result[org_id] += ', ' + str(target_df.loc[i, '_id'])
        else:
            result[org_id] = str(target_df.loc[i, '_id'])
    return result


def generate_org_full_table(ticket_dict, user_dict):
    try:
        df_ticket_dict = pd.DataFrame(ticket_dict.items(), columns=['_id', 'tickets'])
        df_user_dict = pd.DataFrame(user_dict.items(), columns=['_id', 'users'])
        df_orgs_tmp = df_orgs.copy(deep=True)

        return pd.merge(pd.merge(df_orgs_tmp, df_ticket_dict, how='left', on='_id'), df_user_dict, how='left', on='_id')
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        return False


def generate_user_tkt_full_table(table_name, table_df, org_dict):
    new_column_name = 'users' if table_name == 'tickets' else 'tickets'
    table_df[new_column_name] = [list() for x in range(len(table_df.index))]

    for i in range(len(table_df)):
        organization_id = table_df.loc[i, 'organization_id']
        if organization_id in org_dict:
            table_df.at[i, new_column_name] = org_dict[organization_id].split(', ')

    return table_df


def is_to_quit(input_val):
    if input_val == 'quit':
        print('Quit the Zendesk Search progress ...\n')
        sys.exit(0)


def get_searchable_fields():
    separator = '\n--------------------\n'
    output_msg = separator + 'Search Users with\n' + '\n'.join(list(df_users.columns))
    output_msg += separator + 'Search Tickets with\n' + '\n'.join(list(df_tickets.columns))
    output_msg += separator + 'Search Organizations with\n' + '\n'.join(list(df_orgs.columns))
    print(output_msg + '\n')


def show_main_instructions():
    input_2 = input('Select 1) Users or 2) Tickets or 3) Organizations\n')
    is_to_quit(input_2)

    while input == 'quit' or not int(input_2) in range(1, 4):
        is_to_quit(input_2)
        input_2 = input('Select 1) Users or 2) Tickets or 3) Organizations or type \'quit\' to exit \n')

    input_3 = input('Enter search term\n')
    is_to_quit(input_3)

    input_4 = input('Enter search value\n')
    is_to_quit(input_4)

    # TO-DO: Grab the input 2, 3, 4 values to start search and return the results
    query_result = parse_query(int(input_2), input_3, input_4)
    print_formatted_result(query_result)


def init_instructions():
    print('Welcome to Zendesk Search\n')

    try:
        input_0 = input('Type \'quit\' to exit at any time, Press \'Enter\' to continue\n')
        is_to_quit(input_0)

        input_1 = input('''
                Select search options:
                    * Press 1 to search Zendesk
                    * Press 2 to view a list of searchable fields
                    * Type \'quit\' to exit\n''')
        is_to_quit(input_1)

        if int(input_1) == 1:
            show_main_instructions()
        elif int(input_1) == 2:
            get_searchable_fields()

            input_1_1 = input('Press \'Enter\' to the main steps, or type \'quit\' to exit\n')
            is_to_quit(input_1_1)
            show_main_instructions()
    except SyntaxError:
        pass



print('Start loading local DB ...\n...\n...')

basePath = os.path.dirname(os.path.abspath(__file__))

df_tickets = pd.read_json(basePath + '/tickets.json')
df_users = pd.read_json(basePath + '/users.json')
df_orgs = pd.read_json(basePath + '/organizations.json')

org_to_tkt_dict = populate_org_dict(df_tickets)
df_users_full = generate_user_tkt_full_table('users', df_users.copy(deep=True), org_to_tkt_dict)

org_to_user_dict = populate_org_dict(df_users)
df_tickets_full = generate_user_tkt_full_table('tickets', df_tickets.copy(deep=True), org_to_user_dict)

df_orgs_full = generate_org_full_table(org_to_tkt_dict, org_to_user_dict)

query_table = None
query_column = None
query_value = None

print('Local DB loading completed!\n\n')

init_instructions()
