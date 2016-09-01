from django.shortcuts import render,HttpResponse,get_object_or_404
from Reit.models import Reit_Indicator, Industry_Info

# Create your views here.


def home(request):
    context=dict()
    return render(request, 'home.html', context)

def search_name(request):

    context=dict()
    update_name_list()
    exchange_list = Reit_Indicator.objects.all()
    context['exchange_list'] = exchange_list

    return render(request, 'search_name.html', context)

def search_name_info(request):
    try:
        ticker=request.GET['selected_reit']
        reit_info=get_object_or_404(Reit_Indicator, identifier=ticker)
    except:
        pass

    context=dict()
    context['reit_info']=reit_info
    info_list=get_info_list(reit_info)
    context['info_list']=info_list

    try:
        pe_comp = float(info_list[8][1])
    except:
        pe_comp='text'


    pe_avg = get_overall_avg()

    context['pe_comp']=pe_comp
    context['pe_avg']=pe_avg

    return render(request, 'search_name_info.html', context)


def update_name_list():
    try:
        exchange_list=get_name_list()
    except:
        return None

    for reit in exchange_list:
        name=reit[0]
        ticker=reit[1]
        try:
            c=Reit_Indicator.objects.get(identifier=ticker)
            continue
        except:
            new_c=Reit_Indicator(identifier=ticker, long_name=name)
            new_c.save()
    return None

def get_name_list():
    url="https://www.reit.com/investing/investor-resources/reit-directories/reits-by-ticker-symbol?field_rtc_stock_exchange_tid=5119"
    import pandas
    data_table = pandas.read_html(url)
    length=len(data_table[0].index)
    nyse_reit=list()

    for k in range(0,2):
        for i in range(0,length):
            lol=data_table[0][k][i].rsplit(' ',1)
            nyse_reit.append(lol)

    url="https://www.reit.com/investing/investor-resources/reit-directories/reits-by-ticker-symbol?field_rtc_stock_exchange_tid=5120"
    data_table = pandas.read_html(url)
    length=len(data_table[0].index)
    nasdaq_reit=list()

    for j in range(0,2):
        for l in range(0,length):
            try:
                lol=data_table[0][j][l].rsplit(' ',1)
            except:
                pass
            nasdaq_reit.append(lol)

    reit_name_list=nyse_reit+nasdaq_reit
    return reit_name_list

def get_info_list(reit_info_object):
    import urllib.request as ul
    from bs4 import BeautifulSoup


    search_name=''
    search_ticker=str(reit_info_object.identifier)
    for i in reit_info_object.long_name:
        if i==' ':
            search_name+='+'
        else:
            search_name+=i

    try:
        url='https://www.google.com/finance?q='+search_ticker
        url_response=ul.urlopen(url)
        soup1=BeautifulSoup(url_response)
        search_price=float(soup1.find('span', class_='pr').get_text())
        price_delta_list=(soup1.find('span', class_='ch bld').get_text()).split('\n')
        search_price_delta=float(price_delta_list[0])
        search_price_delta_perc=price_delta_list[1]
        search_description=soup1.find('div', class_='companySummary').get_text()[:-21]
    except:
        url='https://www.google.com/finance?q='+search_name
        url_response=ul.urlopen(url)
        soup1=BeautifulSoup(url_response)
        search_price=float(soup1.find('span', class_='pr').get_text())
        price_delta_list=(soup1.find('span', class_='ch bld').get_text()).split('\n')
        search_price_delta=float(price_delta_list[0])
        search_price_delta_perc=price_delta_list[1]
        search_description=soup1.find('div', class_='companySummary').get_text()[:-21]

    import pandas
    data_table=pandas.read_html(url)[0]
    data_table1=pandas.read_html(url)[1]

    index_list=list()
    index_list.append(('Current Price', search_price))
    index_list.append(('Price Change', search_price_delta))
    index_list.append(('% change', search_price_delta_perc))

    index=data_table[0]
    value=data_table[1]

    for i in range(len(value)):
        index_list.append((index[i], value[i]))

    index1=data_table1[0]
    value1=data_table1[1]
    for j in range(len(value1)):
        index_list.append((index1[j], value1[j]))

    index_list.append(('Description', search_description))
    return index_list



def search_range(request):
    context=dict()
    industry_list = ['Retail','Residential','Office','Industrial','Hotel/Motel','Diversified','Healthcare Facilities']
    context['industry_list'] = industry_list
    return render(request, 'search_range.html', context)


def serach_range_matrix(request):
    context=dict()

    ind_name=request.GET['Industry']
    ind_list=get_industry_info(ind_name)
    avg_list=get_industry_avg(ind_name)
    context['industry_list']=avg_list
    context['ind_name']=ind_name
    matrix_list = [['P/E','pe'], ['Net Profit Margin','npm'], ['Return on Equity','roe'], ['Dividend Yield','dy'], ['Total D/E','tde']]
    context['matrix_list'] = matrix_list

    return render(request, 'search_range_matrix.html', context)

def get_industry_info(industry_name):
    dico = [['Diversified','440'],['Healthcare Facilities','442'],['Hotel/Motel','443'],['Industrial','444'],['Office','441'],['Residential','445'], ['Retail','446']]
    k=''
    k=str(industry_name)
    for item in dico:
        if k==item[0]:
            link_id=item[1]
            url="https://biz.yahoo.com/p/"+link_id+"conameu.html"
            import pandas
            data_table = pandas.read_html(url,header=0)[3]
            residential_reit=data_table['Description']
            pe=data_table['P/E']
            npm=data_table['NetProfit Margin % (mrq)']
            roe=data_table['ROE %']
            dy=data_table['Div. Yield %']
            tde=data_table['Long-Term Debt toEquity']
            all_reit_list=list()
            for i in range(3,len(residential_reit)):
                all_reit_list.append([residential_reit[i],float(pe[i]),float(npm[i]),float(roe[i]),float(dy[i]),float(tde[i])])
    return all_reit_list

def get_industry_avg(industry_name):
    dico = [['Diversified','440'],['Healthcare Facilities','442'],['Hotel/Motel','443'],['Industrial','444'],['Office','441'],['Residential','445'], ['Retail','446']]
    k=''
    k=str(industry_name)
    for item in dico:
        if k==item[0]:
            link_id=item[1]
            url="https://biz.yahoo.com/p/"+link_id+"conameu.html"
            import pandas
            data_table = pandas.read_html(url,header=0)[3]
            #residential_reit=data_table['Description']
            pe=data_table['P/E']
            npm=data_table['NetProfit Margin % (mrq)']
            roe=data_table['ROE %']
            dy=data_table['Div. Yield %']
            tde=data_table['Long-Term Debt toEquity']
            industry_average=[k+' '+" REITs Average", float(pe[1]),float(npm[1]),float(roe[1]),float(dy[1]),float(tde[1])]
    return industry_average

def get_overall_avg():
    dico = [['Diversified','440'],['Healthcare Facilities','442'],['Hotel/Motel','443'],['Industrial','444'],['Office','441'],['Residential','445'], ['Retail','446']]
    industry_avg=list()
    for item in dico:
        link_id=item[1]
        url="https://biz.yahoo.com/p/"+link_id+"conameu.html"
        import pandas
        data_table = pandas.read_html(url,header=0)[3]
        #residential_reit=data_table['Description']
        pe=data_table['P/E']
        npm=data_table['NetProfit Margin % (mrq)']
        roe=data_table['ROE %']
        dy=data_table['Div. Yield %']
        tde=data_table['Long-Term Debt toEquity']
        industry_avg.append([float(pe[1]),float(npm[1]),float(roe[1]),float(dy[1]),float(tde[1])])

    overall_avg=list()

    pe_avg=0

    #for i in range(0,5):
    for items in industry_avg:
        pe_avg+=items[0]


    pe_avg=pe_avg/7
    return pe_avg

def search_range_detail(request):
    context=dict()
    variable=str(request.GET['matrix'])
    kpi=variable.split('_')[0]
    matrix_list = [['P/E','pe'], ['Net Profit Margin','npm'], ['Return on Equity','roe'], ['Dividend Yield','dy'], ['Total D/E','tde']]
    kpi_display=''
    for item in matrix_list:
        if item[1]==kpi:
            kpi_display=item[0]
    industry_name=variable.split('_')[1]
    detail_list=perf(industry_name,kpi)
    context['detail_list']=detail_list
    context['kpi']=kpi_display
    context['ind_name']=industry_name
    return render(request, 'search_range_detail.html', context)



def perf(industry_name, kpi):
    import math
    top=list()
    result=list()
    dico = [['Diversified','440'],['Healthcare Facilities','442'],['Hotel/Motel','443'],['Industrial','444'],['Office','441'],['Residential','445'], ['Retail','446']]
    dico2 = [['pe',1],['npm',2],['roe',3],['dy',4],['tde',5]]
    k=''
    k=str(industry_name)
    for l in dico:
        if k==l[0]:
            a=get_industry_avg(k)
            b=get_industry_info(k)

            d=list()

            for j in b:
                c=list()
                c.append(j[0])
                for i in range(1,6):
                    z=j[i]-a[i]
                    if math.isnan(float(z))==True:
                        c.append(0)
                    else:
                        c.append(round((j[i]-a[i]),2))
                d.append(c)
    for m in dico2:
        if kpi==m[0]:
            a=m[1]
            if a==1 or a==5:
                r=sorted(d,key=lambda s : s[a],reverse=False)
            else:
                r=sorted(d,key=lambda s : s[a],reverse=True)

            for t in range(0,5):
                top.append(r[t])

            for item in top:
                for item2 in b:
                    if item[0]==item2[0]:
                        item3=0
                        for item3 in range(0,6):
                            nan_val=item2[item3]
                            try:
                                if math.isnan(float(nan_val))==True:
                                    item2[item3]='-- '
                            except:
                                pass
                        result.append(item2)
    return result





#def get