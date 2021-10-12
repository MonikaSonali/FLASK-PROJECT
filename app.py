from flask import Flask, redirect, url_for, render_template, request
import pandas as pd
app = Flask(__name__)


@app.route('/')
def landingPage():
    return render_template('index.html')

@app.route('/getDF')
def getDF():
    df = pd.read_csv("dump.csv")
    df = df[df['id'] != 'id']
    df.reset_index(inplace=True)
    df.drop(['index'], axis=1, inplace=True)
    df.sort_values(['observationDateTime'], ascending=False, inplace=True)
    df = df.drop_duplicates()
    df.reset_index(inplace=True)
    df.drop(['index'], axis=1, inplace=True)
    # return df.to_html(classes="table table-striped")
    return df

@app.route('/cases/<licensePlate>')
def cases(licensePlate):

    df = getDF()
    df5 = df[df['license_plate'] == licensePlate].sort_values(by=['observationDateTime'])
    df5['Counter'] = 0
    df5.reset_index(inplace=True)
    df5.drop(['index'], axis=1, inplace=True)
    indices = []
    for ind in df5.index:
        indices.append(ind)
    for ind in range(0, len(indices)-1):
        if df5['serviceOnDuty'].iloc[ind] == "YES" and df5['serviceOnDuty'].iloc[ind+1] == "NO":
               df5['Counter'].iloc[ind] += 1

    return render_template('result.html', lp=df5['license_plate'].iloc[0], cases=df5['Counter'].sum())
    return df5['license_plate'].iloc[0], df5['Counter'].sum()


@app.route('/getData', methods=['POST', 'GET'])
def submit():

       if request.method == 'POST':
           licensePlateNumber = request.form['lpnumber']
           print("REQUEST --- ", request.form['lpnumber'], request.args.get('lpnumber'))
           
       return redirect(url_for('cases', licensePlate=licensePlateNumber))

if __name__ == '__main__':
    app.run(debug=True)




