import pyodbc
from flask import Flask, render_template,request
import plotly
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go

app = Flask(__name__)
# Index page
@app.route("/")
def show_files():
    cnxn=create_sql_conn()
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM [dbo].[files_data]")
    row = cursor.fetchone()
    files_names = []
    dates = []
    sizes = []
    descriptions = []
    while row:
        files_names.append(row[0])
        dates.append(row[1])
        sizes.append(row[2])
        descriptions.append(row[3])
        row = cursor.fetchone()
    return render_template("first_page.html", list1=zip(files_names,dates,sizes,descriptions))

@app.route("/",methods=['POST'])
def show_plot():
    print("Into Show_Plot method...")
    cnxn=create_sql_conn()
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM [dbo].[files_data]")
    row = cursor.fetchone()
    files_names = []
    dates = []
    sizes = []
    descriptions = []
    while row:
        files_names.append(row[0])
        dates.append(row[1])
        sizes.append(row[2])
        descriptions.append(row[3])
        row = cursor.fetchone()

    received_file_name=request.form['file_name']
    print("File Received = ", received_file_name)
    bar=create_plotly_plot(received_file_name)
    return render_template('first_page.html', plot=bar,list1=zip(files_names,dates,sizes,descriptions))

def create_plotly_plot(received_file_name):
    server = 'visualizationserver.database.windows.net'
    database = 'visualization_data'
    username = 'hmtd1992'
    password = 'Hmtd@1992'
    driver = '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM [dbo].[{}]".format(received_file_name))
    row = cursor.fetchone()
    x = []
    y = []
    while row:
        x.append(row[0])
        y.append(row[1])
        row = cursor.fetchone()
    df = pd.DataFrame({'x': x, 'y': y})# creating a sample dataframe
    #scatter_plot = px.scatter(x=df['x'], y=df['y'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['x'],
        y=df['y'],
        name="Showing EDA for {}".format(received_file_name)
    ))
    fig.update_layout(
        title="EDA of {}".format(received_file_name),
        xaxis_title="Timestamp Values",
        yaxis_title="Signal Values",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    plot_dump = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_dump

def create_sql_conn():
    server = 'visualizationserver.database.windows.net'
    database = 'visualization_data'
    username = 'hmtd1992'
    password = 'Hmtd@1992'
    driver = '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return cnxn

if __name__ == '__main__':
	app.run()