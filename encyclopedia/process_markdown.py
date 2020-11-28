# cd desktop/cs50/project_1/wiki/encyclopedia
# process_markdown.py

import re

def processfile(md):

    htmlblock = ""
    # processes each line in markdown
    ulstring = "<ul>\n</ul>\n"
    listfound = 0
    for line in md:

        line = line[:-1]    
        para = True
        
        strong = re.search(r"\*\*", line)
        #returns hash/heading value to line break
        heading = re.search(r"\#", line)
        ullist = re.search(r"\*(.*?)", line)


        # create styles from markdown
        if strong:
            flag = 1
            while flag == 1:
                line = re.sub(r"\*\*", "<strong>", line, 1)
                line = re.sub(r"\*\*", "</strong>", line, 1)
                if re.search(r"\*\*", line):
                    flag = 1
                else: 
                    flag = 0
                print(line)
            
            htmlblock += line


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
