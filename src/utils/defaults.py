
variables = {
    'DATABASE':{
        'name':'dehskavu22md39',
        'host':'ec2-3-218-75-21.compute-1.amazonaws.com',
        'user':'cbolmnrxydramg',
        'passw':'f6dd6b3e65549a0cf705fcaacd383de68a39edb1413bd69fd60be6c91e1fc8b7'
    },
    'SCRAPING':{
        'base':'https://finance.yahoo.com/quote/',
        'tag':'.SA',
        'xp_name':'//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1',
        'xp_change':'//*[@id="quote-header-info"]/div[3]/div[1]/div/span[2]',
        'xp_price':'//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]'
    }
    # 'SCRAPING':{
    #     'base':'https://markets.ft.com/data/equities/tearsheet/summary?s=',
    #     'tag':':SAO',
    #     'xp_name':'/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[1]/h1[1]',
    #     'xp_price':'/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[3]/ul/li[1]/span[2]'
    # }
}