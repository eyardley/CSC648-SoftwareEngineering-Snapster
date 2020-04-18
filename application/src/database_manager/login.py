import bcrypt
import base64
import hashlib
from src.database_manager.generate_session import generate_session
import mysql.connector

def login(username, password_plain, ip_address, db, r):
    user_authentication_query = ("SELECT user_id, username, password FROM user WHERE username=%s")

    # query the database for the record of the user
    try:
        db.query(user_authentication_query, (username,))
    except mysql.connector.Error as err:
        # print("Internal server error with database: {}".format(err))
        # FIXME: log this potentially fatal error
        # TODO: what other errors could occur with the connection object?
        error_message = {
            'status': 'database_error',
            'message': 'Internal database error: {}'.format(err)
        }
        return error_message

    # examine the returned record to validate the user entered credentials
    for (user_id, username, password) in db.connection_cursor:

        password_entered = password_plain.encode('utf-8')   # encode the plain text password entered by the user

        # apply bcrypt on entered password and compare with value in database
        if bcrypt.checkpw(base64.b64encode(hashlib.sha256(password_entered).digest()), password.encode('utf-8')):
            # password is a match, now generate session token
            success_message = generate_session(user_id, r)
            if success_message['status'] == 'success':
                success_message['login'] = 'success'
                return success_message
            else:
                return success_message
        else:
            # the user entered the incorrect password
            success_message = {
                'status': 'success',
                'login': 'failed',
            }
            # print('Unsuccessful login attempt by user {}'.format(user_id))
            return success_message



