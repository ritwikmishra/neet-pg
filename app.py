from flask import Flask, redirect, url_for, request, render_template, session, flash, render_template_string
import pandas as pd

app = Flask(__name__)
app.secret_key = 'my random string 123456'
fdict = {
	'2018r1':'2018_round1.ftr',
	'2018mp':'2018_mopup.ftr',
	'2019r1':'2019_round1.ftr',
	'2019mp':'2019_mopup.ftr'
}

def nums(s):
	s = s.replace('\r','')
	return s

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/')
def hello_world():
	return render_template('index.html',df='',q='')

@app.route('/enter_query', methods= ['POST'])
def enter_query():
	if request.method == 'POST':
		q = ""
		# 'S.No.', 'AIR', 'Allotted Quota', 'Alloted Inst', 'Course', 'Alloted Cat', 'Candidate Cat', 'Remarks'
		fname = fdict[request.form['fname']]
		df = pd.read_feather(fname)
		print(df.columns)
		q = q + "DATA: "+fname[:-4]
		df['AIR'] = df['AIR'].apply(nums)
		df['AIR'] = df['AIR'].astype(float)
		airL = request.form['airL']
		airG = request.form['airG']
		aq = request.form['aq']
		place = request.form['place']
		course = request.form['course']
		ac = request.form['ac']
		cc = request.form['cc']
		if(airL):
			df = df[df['AIR']<=int(airL)]
			q = q + " AIR Less Than: "+airL
		if(airG):
			df = df[df['AIR']>=int(airG)]
			q = q + " AIR Greater Than: "+airG
		if(aq):
			df = df[df['Allotted Quota'].str.contains(aq, case=False)]
			q = q + " Allotted Quota: "+aq
		if(place):
			df = df[df['Alloted Inst'].str.contains(place, case=False)]
			q = q + " place: "+place
		if(course):
			df = df[df['Course'].str.contains(course, case=False)]
			q = q + " Course: "+course
		if(ac):
			df = df[df['Alloted Cat'].str.contains(ac, case=False)]
			q = q + " Allotted Cat: "+ac
		if(cc):
			df = df[df['Candidate Cat'].str.contains(cc, case=False)]
			q = q + " Candidate Cat: "+cc
	
		return render_template('index.html',df=df, q=q)




# def my_fun():
# 	return 'My Function!'


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8080, debug=True)
