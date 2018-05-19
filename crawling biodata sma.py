from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

waktu=0.5

url = 'https://arsip.siap-ppdb.com/2017/jakarta/#!/030001/statistik'
driver = webdriver.Firefox()
driver.get(url)
time.sleep(waktu)
listnya = driver.find_elements_by_xpath("//ul[@class='direktori-tbl stat-format js-table']/li/span[@style='white-space: nowrap;']/a[@class='ic act-task tips-tr']")
listnya[l].click()
time.sleep(waktu)
driver.find_elements_by_xpath("//div[@class='nav-cont clear']/div[@class='fr nav clear']/a[@class='paging js-select js-select-limit']")[0].click()
driver.find_elements_by_xpath("//div[@class='tips-modal menu rnd3 js-options']/ul/li/a[contains(text(), '1000')]")[0].click()
driver.get(url)
time.sleep(waktu)

driver.get(url)
time.sleep(waktu)
nilai_sub=[]

# listsiswa = driver.find_elements_by_xpath("//table[@class='tbl-data full stat-format js-table']/tbody/tr/td/a")
listnya = driver.find_elements_by_xpath("//ul[@class='direktori-tbl stat-format js-table']/li/span[@style='white-space: nowrap;']/a[@class='ic act-task tips-tr']")

a_list = [0,1,2,3,5,6]
# waktu=1

# for l in range(12,13):
# for l in range(81,len(listnya)):
for l in range(o,len(listnya)):
    o=l
    nilai=[]
    nilai_pilihan=[]
    listnya = driver.find_elements_by_xpath("//ul[@class='direktori-tbl stat-format js-table']/li/span[@style='white-space: nowrap;']/a[@class='ic act-task tips-tr']")
    listnya[l].click()
    time.sleep(waktu)
    pagesma = driver.page_source
    soupsma = BeautifulSoup(pagesma,"html.parser")
    
    listsiswajumlah = driver.find_elements_by_xpath("//table[@class='tbl-data full stat-format js-table']/tbody/tr/td/a")
    for k in range(len(listsiswajumlah)):
        p=k
        listsiswajumlah = driver.find_elements_by_xpath("//table[@class='tbl-data full stat-format js-table']/tbody/tr/td/a")
#         listsiswa = driver.find_elements_by_xpath("//table[@class='tbl-data full stat-format js-table']/tbody/tr/td/a")
        listsiswajumlah[k].click()
        time.sleep(waktu)

        page = driver.page_source
        soup = BeautifulSoup(page,"html.parser")
        
        biodatalist=soup.findAll('div',{'class':'js-result'})[7].findAll('ul',{'class':'direktori-tbl stat-format section'})
        nilai_sub.append(soupsma.findAll('div',{'class':'namecard js-btn-popup-sekolah-selected'})[1].find('h3').text)
        masukan = soup.findAll('a',{'class':'button full sml-card js-btn-dialog-kompetensi'})[0].find('b').text
        jurusan = re.sub('Jurusan: ','', masukan)
        nilai_sub.append(jurusan)
#         a_list = [0,1,2,3,5,6]
        for i in a_list:
            for j in range(1,len(biodatalist[i].findAll('li'))):
                for m in range(1,len(biodatalist[i].findAll('li')[j].findAll('span'))):
#                     print biodatalist[i].findAll('li')[j].findAll('span')[m].text
                    nilai_sub.append(biodatalist[i].findAll('li')[j].findAll('span')[m].text)
    
        nilai_sub_pilihan=[]
        for i in range(4,5):
            for j in range(1,len(biodatalist[i].findAll('li'))):
                nilai_sub_pilihan=[]
                nilai_sub_pilihan.append(soupsma.findAll('div',{'class':'namecard js-btn-popup-sekolah-selected'})[1].find('h3').text)
                masukan = soup.findAll('a',{'class':'button full sml-card js-btn-dialog-kompetensi'})[0].find('b').text
                jurusan = re.sub('Jurusan: ','', masukan)
                nilai_sub_pilihan.append(jurusan)

                nilai_sub_pilihan.append(biodatalist[0].findAll('li')[3].findAll('span')[1].text)
                nilai_sub_pilihan.append(biodatalist[i].findAll('li')[j].findAll('span',{'style':'width: 150px;'})[0].text)
                nilai_sub_pilihan.append(biodatalist[i].findAll('li')[j].findAll('span',{'class':'c-title'})[0].text)
                nilai_sub_pilihan.append(biodatalist[i].findAll('li')[j].findAll('span',{'class':'c-title'})[1].text)
                nilai_pilihan.append(nilai_sub_pilihan)
#         nilai_pilihan
        
#         biodatalist=soup.findAll('div',{'class':'js-result'})[7].findAll('ul',{'class':'direktori-tbl stat-format section'})
#         for i in range(len(biodatalist)):
#             biodata=biodatalist[i].findAll('li')
#             for j in range(1,len(biodata[i].findAll('span'))):
#                 nilai_sub.append(biodata[i].findAll('span')[j].text)
        nilai.append(nilai_sub)
        increment = soupsma.findAll('table',{'class':'tbl-data full stat-format js-table'})[0].find('tbody').findAll('tr')
        print nilai[k][0]+' - '+nilai[k][1]+' - '+increment[k].find('td').text+' - '+nilai[k][4]
#         print nilai_pilihan
        nilai_sub=[]

        driver.execute_script("window.history.go(-1)")
        time.sleep(waktu)
        
    print l
    
    df = pd.DataFrame(nilai,columns=['Sekolah','Jurusan','Nomor Peserta','Nomor Ujian','Nama Siswa','Jenis Kelamin','Tempat, Tanggal Lahir','Asal Sekolah','Domisili','Nomor Induk Kependudukan (NIK)','Bahasa Indonesia','Bahasa Indonesia','Matematika','Matematika','Bahasa Inggris','Bahasa Inggris','Ilmu Pengetahuan Alam','Ilmu Pengetahuan Alam','Jumlah NUN','Jumlah NUN','No. Pendaftaran','Wilayah','Jalur','Jenjang','Tahap','Lokasi Daftar','Waktu Daftar','Nilai Akhir','Nilai Akhir','Jadwal Seleksi','Pilihan Diterima','Urutan','Status Lapor Diri'])
    nama_sma = soupsma.findAll('div',{'class':'namecard js-btn-popup-sekolah-selected'})[1].find('h3').text
    minat = soup.findAll('a',{'class':'button full sml-card js-btn-dialog-kompetensi'})[0].find('b').text
    df.to_csv('/home/ubuntu/Documents/iben/raw data/sma/biodata/'+str(nama_sma)+'-'+minat+'.csv')
    print '/home/ubuntu/Documents/iben/raw data/sma/biodata/'+str(nama_sma)+'-'+minat+'.csv'
    
    df_pilihan = pd.DataFrame(nilai_pilihan,columns=['Sekolah','Jurusan','Nama Siswa','Pilihan ke','SMA Pilihan','Jurusan Pilihan'])
    df_pilihan.to_csv('/home/ubuntu/Documents/iben/raw data/sma/pilihan/'+str(nama_sma)+'-'+minat+' pilihan.csv')
    print '/home/ubuntu/Documents/iben/raw data/sma/pilihan/'+str(nama_sma)+'-'+minat+' - pilihan.csv'
    
    driver.execute_script("window.history.go(-1)")
    time.sleep(waktu)
