from flask import Flask, request, render_template, session, url_for, redirect, flash
from androidsqlquery import selectallpass, sqlqueryidsearch, sqlqueryaddnewrecord, sqlqueryupdatepass, \
     sqlquerydeletepass
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

app.secret_key = 'any random string'
 
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def main():
    allpass = selectallpass()
    session.pop('deleted', None)
    return render_template('main.html', allpass = allpass)

@app.route('/backtomain', methods=['POST'])
def backtomain():
    if 'allpass' in session:
        allpass = selectallpass() #session['allpass']
        return render_template('main.html', allpass = allpass)

@app.route('/addnew', methods=['POST'])
def addnewrecord():
    return render_template('addnew.html')

@app.route('/addnewproc', methods=['POST'])
def addnewprocfunc():
    rf = request.form
    if request.method == 'POST':
        alldata = (rf['t_itle'],
                   rf['u_ser'],
                   rf['p_ass'],
                   rf['a_uth'],
                   rf['e_mail'],
                   rf['u_rl'],
                   rf['n_otes'])
        
        sqlqueryaddnewrecord(alldata)
        session.pop('allpass', None)
        allpass = selectallpass()
        session['allpass'] = allpass
        return render_template('main.html', allpass = allpass)
        
@app.route('/updateproc', methods=['POST'])
def updateprocfunc():
    rf = request.form
    if request.method == 'POST':
        alldata = (rf['myid'],
                   rf['u_ser'],
                   rf['p_ass'],
                   rf['a_uth'],
                   rf['e_mail'],
                   rf['n_otes'])
        sqlqueryupdatepass(alldata)
        onepass = sqlqueryidsearch(alldata[0])
        #return redirect(url_for('backtomain'))
        return render_template('viewpass.html', onepass=onepass)


@app.route('/getsinglepass', methods=['POST'])
def getsinglepass():
    if request.method == 'POST':
        idselected = request.form['I_d']
        onepass = sqlqueryidsearch(idselected)
        print(idselected)
        return render_template('viewpass.html', onepass=onepass)
@app.route('/deletemode', methods=['POST'])
def deletemainfunc():
    allpass = selectallpass()
    session['allpass'] = allpass
    return render_template('deletemode.html', allpass = allpass)

@app.route('/deleteproc', methods=['POST'])
def deleteprocfunc():
    if request.method == 'POST':
        session.pop('allpass', None)
        idselected = request.form['I_d']
        session['deleted'] = sqlqueryidsearch(idselected)[1]
        sqlquerydeletepass(idselected)
        allpass = selectallpass()
        session['allpass'] = allpass
        deleted = 'the \'' + str(session['deleted']) + '\' deleted'
        return render_template('deletemode.html', allpass = allpass, deleted=deleted)

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=False, host='0.0.0.0', port=5000)