'''
Created on 20.01.2012

@author: DuncanMCLeod
'''

import re

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
        return False


    def getSubitemsWithName(self, name):
        items = []
        for item in self.subitems:
            if item.getName()==name:
                items.append(item)
            
        return items


class RSS20():
    def __init__(self):
        print("TODO:")


    def addSelfClosedItem(self, item, itemString):
        index=1
        print(itemString)
        print(itemString[0:str.find(itemString, " ", index)])
        item = item.addItem(item, itemString[0:str.find(itemString, " ", index)], "")
        while(index>0):
            nextSpaceBegin = str.find(itemString, " ", index)
            nextSpaceEnd   = str.find(itemString, " ", nextSpaceBegin+1)
            if ( str.find(itemString, '"', nextSpaceBegin) < nextSpaceEnd ) :
                # find next SpaceChar after the next Two Gaensefuesschen
                nextOne = str.find(itemString, '"', nextSpaceBegin)
                nextSecond = str.find(itemString, '"', nextOne+1)
                nextSpaceEnd = str.find(itemString, " ", nextSecond)
                
            pattern = "="
            matcher = re.search(pattern, itemString[nextSpaceBegin+1:nextSpaceEnd])
            if ( matcher != None):
                delimiter = matcher.span()
                print(repr(delimiter))
                name    = itemString[nextSpaceBegin+1:nextSpaceBegin+delimiter[0]+1]
                content = itemString[nextSpaceBegin+delimiter[1]+2:nextSpaceEnd-1]
                print("#"+ name + "#  -->  #" + content +"#")
                item = item.addItem(item, name, content)
                item = item.closeItem()

                
            else:
                print("bloed gelaufen")
            index = nextSpaceEnd
            
            #item = item.addItem(item, name, content)
            #item = item.closeItem()

        item = item.closeItem()
        return item


    def getRSSObject(self, rssString):
        index = 1
        item = RSSItem(0, "BODY", "")
        while(index>0):
            elem, index, isCDATAelem = self.getNextElem(rssString, index)
            elem = elem.lstrip().rstrip()
            if("</"==elem[0:2]):
                # Ende eines Items
                item = item.closeItem()
            else:
                # Anfang eines Items
                if("/>"==elem[elem.__len__()-2:elem.__len__()]):
                    # sich selbst schliessend
                    endNameIndex = str.find(elem, ">", 1)
                    endNameIndex = endNameIndex - 1

                    name = elem[1:endNameIndex]
                    content = ""
                    
                    item = self.addSelfClosedItem(item, name)
                else:
                    if (isCDATAelem == False):
                        endNameIndex = str.find(elem, ">", 1)
                    else:
                        endNameIndex = str.find(elem, ">", 1)
                
                    name = elem[1:endNameIndex]
                    content = elem[endNameIndex+1:elem.__len__()]
                    item = item.addItem(item, name, content)
                    
        return item


    def getNextCDATAelem(self, rssString, fromIndex):
        CLOSE = False
        OPEN  = True
        bracketOpen =  str.find(rssString, "[", fromIndex)
        bracketClose = str.find(rssString, "]", fromIndex)
        if ( bracketOpen < bracketClose ):
            if ( bracketOpen >= 0 ):
                return bracketOpen+1, OPEN
            else:
                return bracketClose+1, CLOSE
        else:                
            if ( bracketClose >= 0):
                return bracketClose+1, CLOSE
            elif ( bracketOpen >= 0 ):
                return bracketOpen+1, OPEN
            else:
                return -2, OPEN


    def extractCDATA(self, rssString, fromIndex):
        i = fromIndex
        fromIndex =  str.find(rssString, "[", fromIndex)
        countBrackets = 0
        while (fromIndex > 0):
            lastIndex = fromIndex 
            fromIndex, isOpen = self.getNextCDATAelem(rssString, fromIndex)
            if fromIndex > 0:
                lastIndex = fromIndex 
                
            if isOpen:
                countBrackets = countBrackets+1
            else:
                countBrackets = countBrackets-1
                if (countBrackets == 0):
                    fromIndex=0

        return lastIndex


    def getNextElem(self, rssString, indexStart):
        badStrings = ["<br>"]
        isCDATAelem = False
        elemBegin = str.find(rssString, "<", indexStart)
        elemEnd1    = str.find(rssString, "<", elemBegin+1)
        elemEnd2    = str.find(rssString, "/>", elemBegin+1)
        if (elemEnd1 > elemEnd2 and elemEnd2 > -1):
            elemEnd = elemEnd2+2
        else:
            elemEnd = elemEnd1
            elemCDATA    = str.find(rssString, "<![CDATA[", elemBegin+1)
            if elemEnd == elemCDATA and elemCDATA > 0:
                isCDATAelem = True
                elemCDATEend = self.extractCDATA(rssString, elemCDATA)
                elemEnd1    = str.find(rssString, "<", elemCDATEend+1)
                elemEnd2    = str.find(rssString, "/>", elemCDATEend+2)
                if (elemEnd1 > elemEnd2 and elemEnd2 > -1):
                    elemEnd = elemEnd2
                else:
                    elemEnd = elemEnd1
                
                    
                    
        elemStr = rssString[elemBegin:elemEnd]
        # Test auf ungewuenschte HTML-Codierungsstrings
        for badstring in badStrings:
            if (badstring==elemStr):
                return self.getNextElem(rssString, elemEnd)
        # Test auf ungewuenschte HTML-Codierungsstrings_v2
        if (elemStr[0:9]=="<![CDATA["):
            print ("CDATA an prominenter Stelle")
            return self.getNextElem(rssString, self.getNextIndexAfterCDATA(rssString, elemBegin))
        if (elemStr[0:3]=="<p>"):
            # TODO:
            print("TODO: REMOVE '<p>")
        return elemStr, elemEnd, isCDATAelem


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
            print("|TITLE: "+titleitem.getContent() + " _ LINK: " + linkitem.getContent())
            for rssitem in items:
                titleitem = rssitem.getSubitemWithName("title")
                linkitem  = rssitem.getSubitemWithName("link")
                enclosureitem  = rssitem.getSubitemWithName("enclosure")
                if (titleitem and linkitem and enclosureitem):
                    print("|--TITLE: "+titleitem.getContent())
                    print("|--LINK:  " + linkitem.getContent())
                    print("|--ENCL:  " + enclosureitem.getContent())
                    print("|")
