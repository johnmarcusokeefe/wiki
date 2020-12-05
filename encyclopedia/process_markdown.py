# cd desktop/cs50/project_1/wiki/encyclopedia
# process_markdown.py

import re

# processes the imported markdown
def processfile(markdown):

    htmlblock = ""
    md = markdown.split("\n")
    # processes each line in markdown
    ulstring = "<ul>\n</ul>\n"
    listfound = 0
    for line in md:
 
        para = True
        
        # set action flags
        strong = re.search(r"\*\*", line)
        # tests for correct syntax and returns a value of 0 for even sets
        strongsyntax = len(re.findall(r"\*\*", line))%2
        heading = re.search(r"^\#", line)
        ullist = re.search(r"^\*\s", line)


        # create strong tags from markdown ** if correct syntax/matching tags exist
        if strong and strongsyntax == 0:
            # tests there are even sets of regex 
            if len(re.findall(r"\*\*", line))%2 == 0:
                line = re.sub(r"\s\*\*", " <strong>", line)
                # bold placed from the first word of string
                line = re.sub(r"^\*\*", " <strong>", line)
            if re.search("<strong>", line):
                line = re.sub(r"\*\*", "</strong>", line)
            #built output html
            htmlblock += line
            para = False


        # checks for hash and converts to heading tag 
        if heading:
            hvalue = addStyle(line)
            htmlblock += hvalue
            para = False


        #creates a list element with closing tag on each iteration
        if ullist:
            #remove closing ul tag using index
            ulstring = ulstring[:-6]
            listitem = line[1:]
            ulstring += "<li>"+listitem+"</li>\n</ul>\n"
            listfound = 1
            para = False
        elif listfound == 1:
            # end of list add to html block
            htmlblock += ulstring
            listfound = 0


        if para:
            if len(line) > 0:
                line = "<p>"+line+"</p>"
            htmlblock += line

    
    # search all of htmlblock for links at the end.    
    hlink = re.search( r"\[(.*?)\)" , htmlblock )
    while hlink:
            cleanlink = createlink(hlink.group())
            htmlblock = re.sub(r"\[(.*?)\)", cleanlink, htmlblock, 1)
            hlink = re.search( r"\[(.*?)\)" , htmlblock )
    
    return htmlblock


# match tag to dictionary
def addStyle(linein):
    
    # list of headings which allows a hash count reference
    headings = ["<h1>title</h1>","<h2>title</h2>","<h3>title</h3>","<h4>title</h4>","<h5>title</h5>","<h6>title</h6>"]

    # finds the first space following hashes hence how many hashes
    start = linein.find(" ")

    # use index to exlude the hash character and space
    title = linein[start+1:]
    return re.sub("title", title, headings[start-1])


#assembles a link from markdown text
def createlink(mdfile):

    title = re.search( r"\[(.*?)\]" , mdfile ).group()
    link = re.search( r"\((.*?)\)" , mdfile ).group()
    title = title.strip("[]")
    link = link.strip("()")
    return "<a href="+"'"+link+"'"+">"+title+"</a>"
