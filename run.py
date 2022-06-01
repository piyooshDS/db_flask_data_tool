import imp
from flask import Flask, jsonify, render_template, request, url_for
import os
import psycopg2

app = Flask(__name__)


conn = psycopg2.connect(
    host="localhost",
    database="soccer",
    user='postgres',
    password='postgres')

# Open a cursor to perform database operations
cur = conn.cursor()


@app.context_processor
def utility_processor():
    def format_sql():
        try:
            sql_txt = "select tablename from pg_catalog.pg_tables where schemaname='public';"
            cur.execute(sql_txt)
            tables_list = cur.fetchall()
            return tables_list
        except Exception as e:
            conn.rollback()
    return dict(format_price=format_sql)


@app.route("/")
def main_page():
    return render_template("main.html")


@app.route('/run_query', methods=['POST'])
def run_query():
    try:
        query = request.json.get('query')
        print(query)
        from time import time
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        results = cur.fetchall()
        return jsonify({'result': results, 'columns': colnames})
    except Exception as e:
        conn.rollback()
        if str(e).startswith("relation"):
            error_msg = "Invalid table name, no such table in database."
        elif str(e).startswith("syntax"):
            error_msg = "Invalid syntax, Please check the query."
        else:
            error_msg = "Server error occured,Restart the server."
        print(e)
        return jsonify({'error': error_msg})


@app.route('/submit', methods=['POST'])
def submit():
    try:
        query = request.form.get('query')
        if query is None or query=='':
            error_msg = 'Query can not be blank.'
            return render_template("main.html", error=True, error_msg=error_msg)
        from time import time
        # your code here
        tic = time()
        cur.execute(query)
        toc = time()
        qs_time = round((toc - tic)*1000, 3)
        colnames = [desc[0] for desc in cur.description]
        results = cur.fetchall()
        return render_template("main.html", data=True,
                               results=results,
                               colnames=colnames, query=query, time=qs_time)
    except Exception as e:
        if str(e).startswith("relation"):
            error_msg = "Invalid table name, no such table in database."
        elif str(e).startswith("syntax"):
            error_msg = "Invalid syntax, Please check the query."
        else:
            error_msg = "Server error occured,Restart the server."
        print(e)
        conn.rollback()
        return render_template("main.html", error=True, error_msg=error_msg)


@app.route('/get_tables', methods=['POST'])
def get_tables():
    try:
        import pdb
        pdb.set_trace()
        sql_txt = "select tablename from pg_catalog.pg_tables where schemaname='public';"
        cur.execute(sql_txt)
        tables_list = cur.fetchall()
        return render_template("main.html", dtable=True, tables=tables_list)
    except Exception as e:
        conn.rollback()
        print(e)
        return render_template("main.html", dtable=False)


@app.route("/queries")
def queries():
    return render_template("queries.html")


if __name__ == "__main__":
    app.run(debug=True)
