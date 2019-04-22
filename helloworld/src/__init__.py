import xml.sax
from xml.dom.minidom import parse

"""sax方式解析"""
class moviesHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.currentData = ""
        self.type=""
        self.format = ""
        self.year = ""
        self.rating = ""
        self.stars = ""
        self.desc = ""

    def startElement(self, tag, attrs):
        self.currentData = tag
        if tag == "movie":
            print("***movie***")
            print("Title :",attrs["title"])

    def endElement(self,tag):
        if tag == "movie":
            print("***movie***")
        if tag == "type":
            print("type:",self.type)
        elif tag == "format":
            print("format:",self.format)
        elif tag == "year":
            print("year:",self.year)
        elif tag == "rating":
            print("rating:",self.rating)
        elif tag == "stars":
            print("stars:",self.stars)
        elif tag == "description":
            print("description:",self.desc)

    def characters(self,content):
        if self.currentData == "type":
            self.type = content
        elif self.currentData == "format":
            self.format = content
        elif self.currentData == "year":
            self.year =content
        elif self.currentData == "rating":
            self.rating =content
        elif self.currentData =="stars":
            self.stars =content
        elif self.currentData =="description":
            self.desc =content

# domTree方式解析
class xmlDomParse:
    def __init__(self,file):
        self.file = file

    def parse(self):
        DomTree = xml.dom.minidom.parse(self.file)
        collection = DomTree.documentElement
        if collection.hasAttribute("self"):
            print("the root self : %s"%(collection.getAttribute("shelf")))
        movies = collection.getElementsByTagName("movie")
        for movie in movies:
            print("***movie***")
            if movie.hasAttribute("title"):
                print("Tile:",movie.getAttribute("title"))
            type = movie.getElementsByTagName("type")[0]
            print("type:",type.childNodes[0].data)


if ( __name__ == "__main__"):
    """open("../resource/movies.xml","r+")"""

    # parser = xml.sax.make_parser()
    # parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # Handler = moviesHandler()
    # parser.setContentHandler(Handler)
    # parser.parse("../resource/movies.xml")


    # domParse = xmlDomParse("../resource/movies.xml")
    # domParse.parse()






