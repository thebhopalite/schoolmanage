from flaskext.mysql import MySQL
from flask import *
from datetime import date
from markPy import mymarks
import os

mysql=MySQL()
app=Flask(__name__)
app.secret_key='bhopal123'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_DB']='school_db'

mysql.init_app(app)

def connection():
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_DB'] = 'school_db'
    mysql.init_app(app)
    return app
app.register_blueprint(mymarks,url_prefix='/marksheet')


@app.route('/')
def login():
    return render_template('front.html')

@app.route('/dologin',methods=['POST'])
def dolog():
    username = request.form['username']
    password = request.form['password']
    info = [username, password]
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("select * from login where username=%s and password=%s",info)
    data = mycur.fetchone()
    if (data):
        session['user'] = data[1]
        return redirect("/addstudent")
    else:
        return redirect('/login')

@app.route('/login')
def dashboard():
    if 'user' in session:
        return render_template('addstudent.html')
    else:
        return redirect("/login")

@app.route('/addstudent')
def addstudent():
    return render_template('addstudent.html')

@app.route('/insertRecord',methods=['POST'])
def insertrecord():
    photo=request.files['photo']
    tcupload=request.files['tcupload']
    casteupload=request.files['casteupload']
    birthupload=request.files['birthupload']
    aadharupload=request.files['aadharupload']
    data=[request.form['enroll'],request.form['fname'],request.form['lname'],request.form['dob'],request.form['sssmid'],
                                                                                             request.form['aadharno'],request.form['religion'],request.form['caste'],
                                                                                             request.form['rte'],request.form['contact'],request.form['address'],request.form['fathername'],
                                                                                             request.form['mothername'],request.form['fatheroccupation'],request.form['motheroccupation'],
                                                                                             request.form['fathermobile'],request.form['accountname'],request.form['accountno'],request.form['ifsc'],
                                                                                             request.form['sclass'],request.form['section'],request.form['session'],request.form['medium'],
                                                                                             request.form['fees'],request.form['vaccination'],request.form['transport'],photo.filename,aadharupload.filename,tcupload.filename,birthupload.filename,casteupload.filename]

    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("INSERT INTO `student`(`enroll`, `fname`, `lname`, `dob`, `sssmid`, `aadharno`, `religion`, `caste`, `rte`,`contact`, `address`, `fathername`, `mothername`,  `fatheroccupation`, `motheroccupation`,`fathermobile`, `accountname`, `accountno`, `ifsc`,  `sclass`, `section`, `session`, `medium`, `fees`,`vaccination`, `transport`, `status`,`photo`,`aadharupload`,`tcupload`,`birthupload`,`casteupload`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'pursing',%s,%s,%s,%s,%s)",data)
    photo.save(os.path.join('static/student/photo', photo.filename))
    tcupload.save(os.path.join('static/student/tc', tcupload.filename))
    casteupload.save(os.path.join('static/student/caste', casteupload.filename))
    birthupload.save(os.path.join('static/student/birth', birthupload.filename))
    aadharupload.save(os.path.join('static/student/aadhar', aadharupload.filename))
    return ("done")
@app.route('/studentlist',methods=['GET'])
def studentlist():
    sclass=request.args.get('sclass')
    mycon=mysql.connect()
    mycur=mycon.cursor()
    info=[sclass,'pursing']
    mycur.execute("select * from student where sclass=%s and status=%s",info)
    data=mycur.fetchall()

    return render_template('studentlist.html',data=data)

@app.route('/profile',methods=['GET'])
def profile():
    enroll=request.args.get('enroll')
    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("select * from student where enroll=%s"%enroll)
    data=mycur.fetchone()
    return render_template('profile.html',data=data)

@app.route('/editStudent',methods=['GET'])
def editStudent():
        enroll=request.args.get('enroll')
        mycon=mysql.connect()
        mycur=mycon.cursor()
        mycur.execute("select * from student where enroll=%s"%enroll)
        data=mycur.fetchone()
        return render_template('editstudent.html',data=data)

@app.route('/updateRecord',methods=['POST'])
def updateRecord():

    data = [request.form['fname'], request.form['lname'], request.form['dob'],
            request.form['sssmid'],request.form['aadharno'], request.form['religion'], request.form['caste'],
            request.form['rte'], request.form['contact'], request.form['address'], request.form['fathername'],
            request.form['mothername'], request.form['fatheroccupation'], request.form['motheroccupation'],
            request.form['fathermobile'], request.form['accountname'], request.form['accountno'], request.form['ifsc'],
            request.form['sclass'], request.form['section'], request.form['session'], request.form['medium'],
            request.form['fees'], request.form['vaccination'], request.form['transport'], request.form['enroll']]
    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("update student set fname=%s,lname=%s,dob=%s,sssmid=%s,aadharno=%s,religion=%s,caste=%s,rte=%s,contact=%s,address=%s,"
                  "fathername=%s,mothername=%s,fatheroccupation=%s,motheroccupation=%s,fathermobile=%s,accountname=%s,accountno=%s,"
                  "ifsc=%s,sclass=%s,section=%s,session=%s,medium=%s,fees=%s,vaccination=%s,transport=%s where enroll=%s",data)
    return redirect(url_for('studentlist',sclass=request.form['sclass']))

@app.route('/deletestudent',methods=['GET'])
def deletestudent():
    enroll=request.args.get('enroll')
    sclass=request.args.get('sclass')
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("update student set status='deleted' where enroll=%s"%enroll)
    return redirect(url_for('studentlist',sclass=sclass))

@app.route('/removedStudent')
def removedStudent():
    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("select * from student where status='deleted'")
    data=mycur.fetchall()
    return render_template('removedStudent.html',data=data)

@app.route('/restorestudent')
def restorestudent():
    enroll = request.args.get('enroll')
    sclass = request.args.get('sclass')
    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("update student set status='pursing' where enroll=%s"%enroll)
    data=mycur.fetchall()
    return redirect(url_for('studentlist', sclass=sclass))


@app.route('/feelist')
def feelist():
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("select s.enroll,s.fname,s.lname,s.fathername,s.sclass,s.section,s.fees,sum(f.amount),s.fees-sum(f.amount) as 'remain',s.session from student s, fees f where s.enroll=f.enroll group by s.enroll")
    data = mycur.fetchall()
    return render_template('feelist.html', data=data)



@app.route('/depositfees',methods=['POST'])
def depositfees():
    enroll=request.form['enroll']
    remain = request.form['remain']
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("select * from student where enroll=%s" % enroll)
    data = mycur.fetchone()
    today = date.today()
    todate = today.strftime("%Y-%m-%d")
    mycur.execute("select receipt from fees order by fid desc limit 1")
    receipt=mycur.fetchone()
    receiptno=receipt[0]+1
    return render_template('depositfees.html',data=data,date=todate,receiptno=receiptno,remain=remain)

@app.route('/payfees',methods=['POST'])
def payfees():
    data2 = [
            request.form['name'],
            request.form['enroll'],
            request.form['sclass'],
            request.form['receipt'],
            request.form['date'],
            request.form['amount'],
            request.form['remark']]
    data = [request.form['name']]
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute(
        "INSERT INTO `fees`(`name`, `enroll`,`sclass`,`receipt`,`date`,`amount`,`remark`)VALUES(%s,%s,%s,%s,%s,%s,%s)",
        data2)
    return render_template('feespaid.html',data2=data2,data=data)



@app.route('/feecard',methods=['POST'])
def feecard():
    enroll=request.form['enroll']
    sclass=request.form['class']
    mycon=mysql.connect()
    mycur=mycon.cursor()
    info=[enroll,sclass]
    mycur.execute("select fid,enroll,name,sclass,receipt,date,amount,remark from fees where enroll=%s and sclass=%s",info)
    details=mycur.fetchall()
    mycur.execute("select sum(f.amount),s.fees as total from fees f, student s where f.enroll=s.enroll and  (s.enroll=%s and s.sclass=%s)",info)
    total=mycur.fetchone()
    return render_template('feecard.html',details=details,total=total)

@app.route('/transaction')
def transaction():

    return render_template('transaction.html')

@app.route('/record',methods=['POST'])
def record():

    fromdate=request.form['fromdate']
    todate=request.form['todate']
    dates=[fromdate,todate]
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("select * from fees where date between %s and %s",dates)
    details=mycur.fetchall()
    return render_template('record.html',details=details)

app.run(debug=True,port=800)
