#Find your merchantid and key in the Sisow Control Panel.
settings.sisow_merchant_id='merchantid'
settings.sisow_merchant_key='merchantkey'
settings.sisow_url='https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/'

def run_demo(amount=666, issuerid=06, description='Eerste_aankoop', purchaseid=1, entrance=1234, testmode=True ):
    merchantid=settings.sisow_merchant_id
    merchantkey=settings.sisow_merchant_key           
    returnurl=URL('sisow', 'index', args='returnurl', scheme=True)
    cancelurl=URL('sisow', 'index', args='cancelurl', scheme=True)
    callbackurl=URL('sisow', 'index', args='callbackurl', scheme=True)
    notifyurl=URL('sisow', 'index', args='notifyurl', scheme=True)
    
    api = SisowAPI(merchantid, merchantkey, testmode)

##UNNEEDED; we'll let users chose their bank and not randomize the process
#    if issuerid is None:
#        # Pick random bank from API
#        bank = random.choice(tuple(api.providers))
#    else:
#        for bank in api.providers:
#            if bank['id'] == issuerid:
#                break
#    print "Picked %(name)s (%(id)s)" % bank

    # Build transaction
    t = Transaction(purchaseid, amount, issuerid, entrance, description)
    print t
    
    #Send transaction
    urls = WebshopURLs(returnurl, cancelurl, notifyurl, callbackurl)
    response = api.start_transaction(t, urls)
    if not response.is_valid(merchantid, merchantkey):
        raise ValueError('Invalid SHA1')

    # Browser part
    url_ideal = urllib.url2pathname(response.issuerurl)
    print url_ideal
    webbrowser.open(url_ideal)

    while True:
        status = api.get_transaction_status(response.trxid)
        if not status.is_valid(merchantid, merchantkey):
            raise ValueError('Invalid SHA1')
        print datetime.now().strftime('%H:%M:%S'), status.status
        if status.status != 'Open':
            break
        time.sleep(5)
