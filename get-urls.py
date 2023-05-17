from urllib.request import Request, urlopen

# Categories to crawl for URLS
categories = ["news", "sports", "opinion", "features", "art", "asb", "blog", "covid-19", "culture", "multimedia", "reviews", "verbatims", "uncategorized"]

# Global database of all article IDs to prevent duplicates
iddb = {}

# Find URLS from a category page
def parse(url):
    
    output = ''

    # read website code from specified url
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})

    # split code by "<" into a list
    webpage = str(urlopen(req).read()).split('<')

    # for every value in list
    for s in webpage:

        # search for url base
        index = s.find('https://palyvoice.com')

        #if base found
        if index != -1:

            # split string at start of URL
            s = s[index:]

            # check if number follows palyvoice URL to see if URL is an article
            if s[22].isdigit():
                # find end of URL
                s = s[:s.find("\\'")]
                urlid = s[22:28]
                if urlid not in iddb:
                    output += (s+"\n")
                    iddb[urlid] = True
                    

    return output
    # open text file to write website code for debugging
    #f = open('html.txt', 'w')
    #f.write(str(webpage))
    #f.close()

# Comment line below if you want all links to be stored in a single file
urls = open('urls.txt','a')

for category in categories:

    # Unomment both lines below if you want each category to be stored in a separate file
    # filename = category + '.txt'
    # urls = open(filename, 'a')

    print(category)
    counter = 1
    
    # Get all URLS from category
    while True:
        try:
            # First iteration had a different category URL
            if counter == 1:
                output = parse("https://palyvoice.com/category/"+category+"/")
                print("https://palyvoice.com/category/"+category+"/")
            else:
                output = parse("https://palyvoice.com/category/"+category+"/page/"+str(counter))
                print("https://palyvoice.com/category/"+category+"/page/"+str(counter))

            urls.write(output)
        except Exception as e:
            if "Error 404" in str(e):
                # Finished parsing category
                break
            else:
                print("ERROR:")
                print(e)
                break
        counter += 1
    
    # Uncomment line below if you want each category to be stored in a separate file
    #urls.close()

urls.close()