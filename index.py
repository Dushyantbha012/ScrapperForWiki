import requests
from bs4 import BeautifulSoup

def fetchAndSave(url,path):
    r=requests.get(url)
    with open(path,"w") as f:
        f.truncate(0)
        f.write(r.text)
    print("\n File Saved \n")

fetchAndSave("https://en.wikipedia.org/wiki/Titanic","data/titanic.html")

with open("data/titanic.html","r") as f:
    html_doc = f.read()
soup = BeautifulSoup(html_doc,"html.parser")
contentTable = soup.find_all(class_="vector-toc-link")


def getSideContents(soup):
    spans = {}

    for a in soup.find_all("a",class_="vector-toc-link"):
        linkText = a.get("href")
        for div in a.find_all('div', class_='vector-toc-text'):
            for span in div.find_all('span'):
                if not span.has_attr('id') and not span.has_attr('class'):
                    spans[span.string]=linkText
                    print(span.string," : ",linkText)
    return spans



def getTable(soup):
    contents ={};
    tempefdd=[]
    text=[];
    headings=[];
    tableItems=[];
    tbody = soup.find("table",class_="infobox")
    heading = 1;
    for tr in tbody.find_all("tr"):
        contentHeading=""
        contentText="";
        contentImages=[];
        isContent=False
        for th in tr.find_all("th"):
            if(th.string!=None):
                name = str(heading)
                text.append({"heading"+name:th.string})
                heading+=1
        for td in tr.find_all("td"):
            for tdItems in td:
              if(tdItems.name=="span"):
                images=[]
                for a in tdItems.find_all("a",class_="mw-file-description"):
                    img = a.find("img")
                    
                    link = img["srcset"].split(",")[-1][0:-3]
                   
                    image = {"link":link}
                    
                    images.append(image)
                if(len(images)>0):
                    if contents.get("images") is not None:
                        
                        contents["images"] +=images
                    else:
                        contents["images"] =images
        
        tdHeadingItem =tr.find("td",style="font-weight: bold")
        if(tdHeadingItem!=None):
            contentHeading=list(tdHeadingItem.stripped_strings)[-1]
            isContent=True
            
        for trItem in tr.find_all("td",style=""):
            trItemText = ""
            huehue = list(trItem.stripped_strings)
            if(len(huehue)>0):
                tempefdd.append(huehue[-1])
            for img in trItem.find_all("img"):
                link = img["srcset"].split(",")[-1][0:-3]   
                image = {"link":link}    
                
                contentImages.append(image)
            for items in trItem.find_all():
                itemText = ""
                for element in td.descendants:
                    if isinstance(element, str):
                        itemText+=(element.strip())
                contentText=itemText
                
            
                    
        if(isContent):
            contentItem={"contentHeading":contentHeading,"contentImages":contentImages,"contentText":contentText}
            text.append(contentItem)
       
    contents["text"]=text
    return contents             
  
print(getSideContents(soup))