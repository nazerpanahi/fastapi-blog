db_table_prefix = ""
db_user_table_name = f"{db_table_prefix}users"
db_comment_table_name = f"{db_table_prefix}comments"

error_user_exists = 'User exists'
error_user_not_exists = 'User not exists'
error_not_authenticated = 'Not Authenticated'
error_incorrect_username = 'Incorrect username or password'
error_incorrect_password = 'Incorrect username or password'
error_not_valid_credentials = 'Could not validate credentials'
error_user_not_found = 'User not found'

error_user_exists_code = 400
error_user_not_exists_code = 400
error_not_authenticated_code = 400
error_incorrect_username_code = 400
error_incorrect_password_code = 400
error_not_valid_credentials_code = 400
error_user_not_found_code = 404
