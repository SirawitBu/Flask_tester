"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from textblob import TextBlob

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

class myForm(FlaskForm):
    message= TextAreaField("Input message",render_kw={'style':'width: 800px;height:250px; overflow: auto; ' }) 
    submit= SubmitField("Send")

###
# Routing for your application.
###

@app.route('/',methods=["GET","POST"])
def home():
    """Render website's home page."""
    message = False
    allWord = False
    tag = False
    nTag = False
    kWord = False
    nkWord = False
    vWord = False
    cWord = False
    cSent = False
    cAlp = False
    cAlpNoSp = False
    cPar = False
    check = False
    form=myForm()
    if form.validate_on_submit():
        message=form.message.data
        form.message.data=""
        blob=TextBlob(message)
        allWord=blob.words
        tag=(blob.tags)
        if tag != False:
            nTag=len(tag)      
        kWord=list((blob.word_counts).keys())
        if kWord != False:
            nkWord=len(kWord)
        vWord=list((blob.word_counts).values())
        cWord=len(blob.split())
        cSent=len(blob.sentences)
        cAlp=len(message)
        cAlpNoSp=len(message)-message.count(' ')
        cPar=message.count('\n')+1
    return render_template('base.html',form=form,message=message,allWord=allWord,tag=tag,nTag=nTag,kWord=kWord,nkWord=nkWord,vWord=vWord,cWord=cWord,cSent=cSent,cAlp=cAlp,cAlpNoSp=cAlpNoSp,check=check,cPar=cPar)


@app.route('/duplicate')
def duplicate():
    """Render the website's about page."""
    return render_template('duplicate.html')

@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
