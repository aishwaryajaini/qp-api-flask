from flask import jsonify
from decimal import Decimal
import pymysql
import base64

"""args_tuple is used to avoid syntax errors while inserting BLOB data. A tuple of arguments is sent to the 
keyword argument 'args_tuple'. If args_tuple is not None, the query function is given 
the tuple of arguments to use in the query which is a format string.
return_json is True by default , if set to false it returns a list of dictionaries for debugging"""

def query(querystr, args_tuple=None, return_json=True):

    #create connection object
    connection = pymysql.connect(host='localhost',
                                 user='harish',
                                 password='',
                                 db='testapi',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    #start connection, create cursor and execute query from cursor
    connection.begin()
    cursor = connection.cursor()

    #if query string is a string to be formatted, we pass args_tuple to insert in the string
    #using args_tuple is useful because syntax errors arise when trying to insert blob directly
    if args_tuple:
        cursor.execute(querystr,args_tuple)
    else:
        cursor.execute(querystr)

    #convert any decimal values to strings using encode function defined at the bottom
    result = encode(cursor.fetchall())
    connection.commit() #commit the changes made
    
    #close the cursor and connection
    cursor.close()
    connection.close()
    
    
    if return_json == True:
        return jsonify(result) #convert the query result to JSON
    else:
        return result #returns non JSON format of the query result for debugging


def getBase64Str(value):
    return base64.b64encode(value).decode('utf-8')

# encode function converts decimals to strings 
# and also converts BLOB files 
# which are in 'bytes' datatype to a base64 encoded string
def encode(data):
    #iterate through rows
    for row in data:
        for key, value in row.items():
            if isinstance(value, Decimal):
                row[key] = str(value)
            elif isinstance(value, bytes):
                row[key] = getBase64Str(value)
                
    return data
