import requests
import pandas as pd
import os
from lxml.html import fromstring
from bs4 import BeautifulSoup
import math

url_base = 'https://www.apmonitor.com/pdc/index.php/Main/'
tbl = pd.read_csv('pages.csv')
print(tbl.head())

def get_file(page_name='ArduinoControl'):
    url = url_base + page_name
    r = requests.get(url, allow_redirects=True)
    tree = fromstring(r.content)
    title = tree.findtext('.//title')
    soup = BeautifulSoup(r.text,features='lxml')
    metas = soup.find_all('meta')
    desc = [meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ][0]
    for i in range(1,10):
        url = url_base + page_name + '?action=sourceblock&num=' + str(i)
        r = requests.get(url, allow_redirects=True)
        pn = page_name+'_'+str(i)+'.py'
        open(pn, 'wb').write(r.content)
        sz = os.path.getsize(pn)
        with open(pn) as f:
            if 'GoogleAnalyticsObject' in f.read():
                n = i-1
                f.close()
                os.remove(pn)
                return title, desc, n
    n = 10
    return title, desc, n

prev=-1
hdr = ['Topic','Quiz','Assignment','TCLab']
for i in range(len(tbl)):
    # append when previous row is the same number
    # when multiple topics or assignments for the same class
    if tbl['Class'][i]==prev:
        wmode = 'a'
    else:
        wmode = 'w'
    prev=tbl['Class'][i]
    k = int(tbl['Class'][i])
    if k<=9:
        mod = 'Module_0' + str(k)
    else:
        mod = 'Module_' + str(k)
    try:
        os.mkdir(mod)
    except:
        pass
    os.chdir(mod)

    f = open('README.md',wmode)
    f.write('## Module ' + str(tbl['Class'][i]) + ' in Process Dynamics and Control\n')
    f.write('- [Course Overview](https://apmonitor.com/pdc)\n')
    f.write('- [Course Schedule](https://apmonitor.com/pdc/index.php/Main/CourseSchedule)\n')    

    for j,x in enumerate(hdr):
        d = str(j+1) + '_' + x
        try:
            os.mkdir(d)
        except:
            pass
        os.chdir(d)
        name = tbl[x][i]
        # check for NaN (empty entry)
        if name!=name:
            os.chdir('../')
            continue
        title,desc,n = get_file(name)
        g = open('README.md',wmode)
        url = url_base + name
        g.write('### ['+title+']('+url+')\n')
        g.write('- Scripts Located: ' + str(n)+'\n')
        g.write('- Page Description: '+desc+'\n')
        g.close()
        
        os.chdir('../')
        f.write('### ' + x + '\n')
        url = url_base + tbl[x][i]
        f.write('- ['+title+']('+url+'): '+str(n)+' scripts. Description: '+desc+'\n')
    f.close()

    os.chdir('../')
    

