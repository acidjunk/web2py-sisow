import time
from datetime import datetime
import random
import webbrowser
import urllib


from sisow import _account_from_file
from sisow import SisowAPI
from sisow import Transaction
from sisow import WebshopURLs

@auth.requires_membership('admins')
def index():
    response.view='sisow/index.html'
    title=T('Sisow payment module')
    nav_helper=""
    messages=[]
    messages.append(T("Choose a task"))
    messages.append(LI(A(T("iDEAL beschikbare banken"), _href=URL('sisow','list_banks'))))
    messages.append(LI(A(T("iDEAL betaalformulier"), _href=URL('sisow','formulier'))))    
    return dict(title=title,nav_helper=nav_helper,messages=messages)

def formulier():
    testmode=False
    api = SisowAPI(settings.sisow_merchant_id, settings.sisow_merchant_key, testmode)
    
    title='Sisow iDEAL payment module'
    message = 'U gaat nu een fake betaling doen. Vul daarvoor onderstaande gegevens in!'
    submit=False
    form = SQLFORM.factory(
        Field('description', 'string', label='Omschrijving aankoop', default='Web2py T-shirt (XL)', requires=IS_NOT_EMPTY()),
        Field('amount', 'integer', label='Wat geeft u voor dit kekke item?', default=1099, requires=IS_NOT_EMPTY()),
        Field('bank', 'list:integer', label='Uw bank', requires=IS_IN_SET((item['id'] for item in api.providers),[item['name'] for item in api.providers])))
    if form.process().accepted:
        message='Een moment geduld graag... Uw fake betaling voor \'%s\' wordt gestart.' % (form.vars.description)
        submit=True
    return dict(title=title, message=message, submit=submit, form=form)

@auth.requires_membership('admins')
def list_banks():
    response.view='sisow/index.html'
    title=T('Sisow list of banks')
    nav_helper=""
    messages=[]
    
    testmode=False
    api = SisowAPI(settings.sisow_merchant_id, settings.sisow_merchant_key, testmode)
    messages.append("Available banks")
    # Pick random bank from API
    for item in api.providers:
        messages.append('%s - %s' % (item['id'], item['name']))
    return dict(title=title,nav_helper=nav_helper,messages=messages)
