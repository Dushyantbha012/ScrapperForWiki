import requests
from bs4 import BeautifulSoup

def fetchAndSave(url,path):
    r=requests.get(url)
    with open(path,"w") as f:
        f.truncate(0)
        f.write(r.text)
    print("\n File Saved \n")

fetchAndSave("https://en.wikipedia.org/wiki/Titanic","data/main.html")

with open("data/main.html","r") as f:
    html_doc = f.read()
soup = BeautifulSoup(html_doc,"html.parser")

def getSideContents(soup):
    spans = {}

    for a in soup.find_all("a",class_="vector-toc-link"):
        linkText = a.get("href")
        for div in a.find_all('div', class_='vector-toc-text'):
            for span in div.find_all('span'):
                if not span.has_attr('id') and not span.has_attr('class'):
                    spans[span.string]=linkText
                    
    return spans



def getTable(soup):
    contents ={};
    tempefdd=[]
    text=[];
   
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
                    
                    image={} 
                    link="https://en.wikipedia.org/"+a["href"]
                    fetchAndSave(link,"data/temp.html")
                    with open("data/temp.html","r") as f:
                        html_doc = f.read()
                    ImgPage = BeautifulSoup(html_doc,"html.parser")

                    imgDiv = ImgPage.find("div",class_="fullImageLink",id="file")
                    if(imgDiv!=None):
                    
                        ImgLink = imgDiv.find("a")["href"][2:]
                        image= {"link":ImgLink}
                    images.append(image)
                if(len(images)>0):
                    if contents.get("images") is not None:
                        
                        contents["images"] +=images
                    else:
                        contents["images"] =images
        
        tdHeadingItem =tr.find("th")
        if(tdHeadingItem!=None):
            contentHeading=list(tdHeadingItem.stripped_strings)[-1]
            isContent=True
            
        for trItem in tr.find_all("td",style=""):
            trItemText = ""
            huehue = list(trItem.stripped_strings)
            if(len(huehue)>0):
                tempefdd.append(huehue[-1])
            for img in trItem.find_all("img"):
                link = img.parent["href"]
                tempLink = "https://en.wikipedia.org/"+link
                image={} 
                fetchAndSave(tempLink,"data/temp.html")
                with open("data/temp.html","r") as f:
                    html_doc = f.read()
                ImgPage = BeautifulSoup(html_doc,"html.parser")

                imgDiv = ImgPage.find("div",class_="fullImageLink",id="file")
                if(imgDiv!=None and imgDiv.find("a").has_attr("href")):
                    
                    link = imgDiv.find("a")["href"]
               
                description = "";
                descBox = ImgPage.findAll("td",class_="description")
                for d in descBox:
                    description = d.get_text(separator=" ")+" "
                image= {"link":link,"description":description}
                contentImages.append(image)
            itemText = trItem.get_text(separator=" ")
                   
                        
            contentText+=itemText
                
            
                    
        if(isContent):
            contentItem={"contentHeading":contentHeading,"contentImages":contentImages,"contentText":contentText}
            
            text.append(contentItem)
        contents["text"]=text
    return contents             
  
 
def getMainText(soup):
    sups = []
    contentImages=[]
    links = []
    content = []

    for sup in soup.find_all("sup",class_="reference"):
        a = sup.find("a")
        if(a!=None):
            if a.text!=None and a.has_attr("href"):
                temp = {a.text:a["href"]}
                sups.append(temp)
        sup.decompose()
        
    bodyContent = soup.find("div",id="bodyContent");
    figureTags = bodyContent.find_all("figure");
    for figure in figureTags:
        aLink = figure.find("a")
        if(aLink!=None ):
            if(aLink.has_attr("href")):
                link = aLink["href"]
                tempLink = "https://en.wikipedia.org/"+link
                image={} 
                fetchAndSave(tempLink,"data/temp.html")
                with open("data/temp.html","r") as f:
                    html_doc = f.read()
                ImgPage = BeautifulSoup(html_doc,"html.parser")
                imgDiv = ImgPage.find("div",class_="fullImageLink",id="file")
                if(imgDiv!=None and imgDiv.find("a").has_attr("href")):

                    link = imgDiv.find("a")["href"][2:]
                description = "";
                descBox = ImgPage.findAll("td",class_="description")
                for d in descBox:
                    description = d.get_text(separator=" ")+" "
                
                image= {"link":link,"description":description}

                contentImages.append(image)
        figure.decompose()
    bodyContent = soup.find("div",id="bodyContent")
    anchorTags = bodyContent.find_all("a")
    for anchor in anchorTags:
        if(anchor.has_attr("href") and anchor.text!=None):
            linkAddr = anchor["href"]
            
            if(linkAddr[:5]=="/wiki"):
                linkAddr="https://en.wikipedia.org"+linkAddr
            links.append({anchor.get_text(separator=" "):linkAddr})
    
    items = bodyContent.find_all(["p","h1","h2","h3","h4","h5","h6"])
    for item in items:
        itemContent ={}
        if(item.name!="p"):
            if(item.text!=None):
                itemContent["heading"]=item.get_text(separator=" ")
        else:
            if(item.text!=None):
                itemContent["paragraph"]=item.get_text(separator=" ")
        content.append(itemContent)
        
    return {"sups":sups,"contentImages":contentImages,"links":links,"content":content}

getMainText(soup)
