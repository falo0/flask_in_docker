# import required python modules
import os
import psycopg2
from flask import Flask, request
app = Flask(__name__)

# this function returns a connection to a postgres database
def get_db_connection():
    conn = psycopg2.connect(
                            host='postgres',
                            dbname='olaf',
                            user='olaf',
                            password='1234'
                            )
    return conn


# this function returns html that is shown in the browser
# all certificats in the database will be listed
def get_return_string():
    
    # connect to the database and create a cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # create a 'certificates' table in the database if it does not exist already
    sql = """
    create table if not exists certificates(
        certificate VARCHAR (100) NOT NULL
    );"""
    cur.execute(sql)


    # fetch all rows from the certificates table
    sql = """
    select * from certificates;
    """
    cur.execute(sql)
    rows = cur.fetchall()


    # commit the changes done by the sql code here
    conn.commit()


    # create the html that will be shown in the browser
    # all certificates in the database will be listed
    row_strings = [ '<li>' + str(row[0]) + '</li>' for row in rows]
    cert_list = '<ul>' + ' '.join(row_strings) + '</ul>'
    return_string = """
    Hello Pexonian, trage hier deine Zertifizierungen ein!
    Beispiele:
    <ul>
    <li>Amazon Web Services (AWS) Solutions Architect - Associate</li>
    <li>Microsoft Certified: Azure Fundamentals</li>
    <li>Google Associate Cloud Engineer</li>
    <li>IBM Certified Technical Advocate - Cloud v3</li>
    <li>Cloud Security Alliance: Certificate of Cloud Security Knowledge (CCSK)</li>
    </ul>

    <form method="POST">
    <input name="certificate">
    <input name="btn" type="submit" value="Zertifikat in Datenbank speichern">
    <input name="btn" type="submit" value="alle Zertifikate löschen">
    </form>

    Zertifikate, die in der Datenbank gespeicher sind:
    """ + cert_list
    return return_string

# This function will delete the certificates table
def drop_certificates():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('drop table if exists certificates')
    conn.commit()


# This is what happens when the user first opens the website
@app.route('/')
def welcome():
    return get_return_string()

# This is what happens when the user clicks the button on the website
@app.route('/', methods=['POST'])
def my_form_post():

    if request.form['btn'] == "Zertifikat in Datenbank speichern":
        # get the certificate string that the user typed into the website
        cert_string = request.form['certificate']

        # save the certificate string in the database
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
        insert into certificates (certificate)
        values ('""" + cert_string + """');
        """
        cur.execute(sql)
        conn.commit()
    elif request.form['btn'] == "alle Zertifikate löschen":
        drop_certificates()
    else:
        raise Exception('POST request by unknown html element')

    return get_return_string()


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=os.getenv('PORT'))