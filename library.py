import requests
from bs4 import BeautifulSoup as soup
import urllib3
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
urllib3.disable_warnings()


class Azercell(QObject):
    numberList = ""
    url = "https://azercellim.com/az/search/"
    ssl = False
    h = {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
     "accept-encoding":"gzip, deflate, br",
     "accept-language":"tr-TR,tr;q=0.9,az-TR;q=0.8,az;q=0.7,en-US;q=0.6,en;q=0.5",
     "cache-control":"max-age=0",
     "content-length":"65",
     "content-type":"application/x-www-form-urlencoded",
     "dnt":"1",
     "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
           }
    prefix = ""
    log = Signal(str)
    debug = Signal(str)
    filePath = "numberList.txt"


    
    def extractData(self,number,page = 0, only_numb = True, count = 0):
        find = {}
        num = [number[0],                                     # Split part1                                  
        number[1],number[2],                                  # Split part2 
        number[3],number[4],                                  # Split part3
        number[5],number[6]]                                  # Split part4
        p = {
        "num1":num[0],                                        # Number Splitter 1
        "num2":num[1],                                        # Number Splitter 2
        "num3":num[2],                                        # Number Splitter 3
        "num4":num[3],                                        # Number Splitter 4
        "num5":num[4],                                        # Number Splitter 5
        "num6":num[5],                                        # Number Splitter 6
        "num7":num[6],                                        # Number Splitter 7
        "prefix":self.prefix,                                          # Prefix
        "send_search":"1"}                                    # Page
        try:
            self.r = requests.post(self.url+str(page),data=p,verify=self.ssl,headers=self.h)    # Request Send
        except requests.exceptions.ConnectionError as net:
            self.debug.emit(f"Internet xətası: {net}\n")
        source = soup(self.r.content,"lxml")
        if(only_numb):
            find = source.findAll("div", attrs={"class":"phonenumber"})
        else:
            try:
                find = source.findAll("div", attrs={"class":"info"})
                find = find[count].find("p")
                find = str(find).replace(" ","")
                find = find.splitlines()
                find = find[1][:-1]
            except IndexError as e:
                find = ''
                
        return find

    def control(self, price, min, max):
        if(min < price < max):
            return True
        else:
            return False

    def splitPrice(self, number, min = 0, max = 5):
        page = 1
        count = 0
        price = ""
        finded = 0
        temp_price = ""
        temp_numbers = ""
        trying = 0
        print(number,min,max)
        while True:
            price = self.extractData(number=number, only_numb=False,page=page, count=count)
            numbers = self.extractData(number=number, only_numb=True,page=page)
            try:
                numbers = str(numbers[count])[38:-11]
                numbers = numbers.replace("<span>eSIM</s","")
                numbers = numbers.replace("</a>","")
            except IndexError:
                self.debug.emit("\nNomre tapilmadi\n")
                break
            if(count == 7):
                count = 0
                page +=1
            else:
                pass
            if(price == ''):
                print("Quit1")
                break
                
            else:
                if(self.control(price=float(price), min=min, max=max)):
                    self.log.emit(f"\nTapılan: {finded}")
                    self.debug.emit(f"{numbers} - {price} ₼\n")
                    print(f"Tapılan: {finded}")
                    temp_price+=price+"\n"
                    temp_numbers += self.splitter(numbers)+"\n"
                    finded+=1
                else:
                    pass

                count+=1
            trying+=1
            self.log.emit(f"\nTəkrarlama: {trying}\nSəhifə: {page}\nNömrə sayı: {count}\n")
            print(f"Təkrarlama: {trying}\nSəhifə: {page}")
        fileNumbers = open(self.filePath,"w")
        fileNumbers.write(temp_numbers)
        self.debug.emit(f"\nFayl Yazıldı: {self.filePath}")



    def soupData(self, find):
        rawData = ""
        for findData in find:
            rawData=rawData +"\n"+str(findData.text).replace("\n","")
        return rawData 

    def getNumbers(self, number, prefix = "10"):
        self.prefix = prefix
        counter_page = 1
        temp_data = ""
        price = ""
        while True:
            temp_data += self.soupData(self.extractData(number, counter_page))
            price += self.extractData(number, counter_page, only_numb=False, count = counter_page-1)+"\n"
            if(len(self.extractData(number, counter_page)) == 0):
                print(f"Səhifə sayı: {counter_page}")
                print(price)
                break
            else:
                print(f"Page: {counter_page}")
            counter_page+=1
        print(len(temp_data.splitlines()))
        self.numberList=temp_data

    def splitter(self, numbers):
        return "("+numbers[0:2]+") "+numbers[2:5]+" "+numbers[5:7]+" "+numbers[7:9]

    def numbers(self):
        return self.numberList

    