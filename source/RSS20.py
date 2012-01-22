'''
Created on 20.01.2012

@author: DuncanMCLeod
'''

class RSSItem():
    def __init__(self, parentItem, name, content):
        self.parentItem = parentItem
        self.name = name
        self.content = content
        self.subitems = []


    def addItem(self, parentItem, name, content):
        item = RSSItem(self, name, content)
        self.subitems.append(item)
        return item


    def closeItem(self):
        return self.parentItem


    def getItems(self):
        return self.subitems


    def getName(self):
        return self.name


    def getContent(self):
        return self.content


    def getItemWithName(self, name):
        if self.name==name:
            # Ick bins selbst
            return self
        else:
            # pruefe alle meine UnterItems
            for item in self.subitems:
                tempItem = item.getItemWithName(name)
                if tempItem:
                    return tempItem

        return False
        

    def getSubitemWithName(self, name):
        for item in self.subitems:
            if item.getName()==name:
                return item


    def getSubitemsWithName(self, name):
        items = []
        for item in self.subitems:
            if item.getName()==name:
                items.append(item)
            
        return items


class RSS20():
    def __init__(self):
        print("TODO:")


    def getRSSObject(self, rssString):
        print("TODO:")
        index = 1
        item = RSSItem(0, "BODY", "")
        print(item.name+"__"+item.content)
        while(index>0):
            elem, index = self.getNextElem(rssString, index)
            elem = elem.lstrip().rstrip()
            if("</"==elem[0:2]):
                # Ende eines Items
                item = item.closeItem()
            else:
                # Anfang eines Items
                endNameIndex = str.find(elem, ">", 1)
                if("/>"==elem[elem.__len__()-2:elem.__len__()]):
                    # sich selbst schliessend
                    endNameIndex = endNameIndex - 1

                    name = elem[1:endNameIndex]
                    content = ""
                    
                    item = item.addItem(item, name, content)
                    item = item.closeItem()
                else:
                    name = elem[1:endNameIndex]
                    content = elem[endNameIndex+1:elem.__len__()]
                    
                    item = item.addItem(item, name, content)
                    
        #self.debugItem(item)
        self.debugItem2(item)
        return item


    def getNextElem(self, rssString, indexStart):
        badStrings = ["<br>"]
        elemBegin = str.find(rssString, "<", indexStart)
        elemEnd1    = str.find(rssString, "<", elemBegin+1)
        elemEnd2    = str.find(rssString, "/>", elemBegin+1)
        if (elemEnd1 > elemEnd2 and elemEnd2 > -1):
            elemEnd = elemEnd2+2
        else:
            elemEnd = elemEnd1
        elemStr = rssString[elemBegin:elemEnd]
        # Test auf ungewünschte HTML-Codierungsstrings
        for badstring in badStrings:
            if (badstring==elemStr):
                return self.getNextElem(rssString, elemEnd)
        # Test auf ungewünschte HTML-Codierungsstrings_v2
        if (elemStr[0:9]=="<![CDATA["):
            return self.getNextElem(rssString, self.getNextIndexAfterCDATA(rssString, elemBegin))
        if (elemStr[0:3]=="<p>"):
            # TODO:
            print("TODO: REMOVE '<p>")
        return elemStr, elemEnd


    def getNextIndexAfterCDATA(self, rssString, elemBegin):
        firstBracket = str.find(rssString, "[", elemBegin) + 1
        numberOfBrackets = 1
        while (numberOfBrackets>0):
            bracketOpen   = str.find(rssString, "[", firstBracket)
            bracketClose  = str.find(rssString, "]", firstBracket)
            if (bracketOpen < bracketClose) and (bracketOpen > 0):
                numberOfBrackets = numberOfBrackets+1
                firstBracket = bracketOpen + 1
            else:
                numberOfBrackets = numberOfBrackets-1
                firstBracket = bracketClose + 1
        firstBracket = str.find(rssString, ">", firstBracket) + 1
        return firstBracket 


    def debugItem(self, item, i=1):
        items = item.getItems()
        emptyStr = ""
        ii = i
        while ii > 0:
            emptyStr = emptyStr + "  "
            ii = ii-1
        
        print(emptyStr + "ANZAHL SUBITEMS: " + str(items.__len__()))
        for item in items:
            print(emptyStr + item.getName() + " -> " + item.getContent())
            self.debugItem(item, i+1)


    def debugItem2(self, item):
        channelItem = item.getItemWithName("channel")
                
        if channelItem:
            titleitem = channelItem.getSubitemWithName("title")
            linkitem  = channelItem.getSubitemWithName("link")
            items = channelItem.getSubitemsWithName("item")
            print("TITLE: "+titleitem.getContent() + " _ LINK: " + linkitem.getContent())
            for rssitem in items:
                titleitem = rssitem.getSubitemWithName("title")
                linkitem  = rssitem.getSubitemWithName("link")
                print("   TITLE: "+titleitem.getContent() + " _ LINK: " + linkitem.getContent())
            


if __name__ == '__main__':
    import sys
    import os
    sys.path.append("/home/actionluzifer/Dokumente/sourcen/workspace/pypoca")
    files=os.listdir("/home/actionluzifer/Dokumente/sourcen/workspace/pypoca")
    for file in files:
        if ("start.py" in file):
            file = file.replace(".py", "")
            pluginImport = __import__(file, globals(), locals(), [], 0)
            pluginImport.starten()