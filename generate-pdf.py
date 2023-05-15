import pdfkit
from urllib.request import Request, urlopen
import shutil
import pickle

# Used for naming files
monthsToDigits = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}

# Generate a PDF from a URL

def generate_pdf(url, date, count):

    # Generate filename
    filename = "VOI_" + date + "_0" + str(count)

    try:
        # Generate PDF from URL
        pdfkit.from_url(url + "?print=true", filename + '.pdf')
        
        #pdfkit.from_url(url, filename + '.pdf')
    except:
        # Catch error from PDFKit
        pass

    # Move PDF to subdirectory
    shutil.move(filename + '.pdf', 'pdfs/' + date[:4] + '/' + filename + '.pdf')


def get_date(url):
    # read website code from specified url
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
    # split code by "{" into a list
    webpage = str(urlopen(req).read()).split('<')
    # f = open('html.txt','w')
    # f.write(str(webpage))
    # f.close()

    # for every value in list
    for s in webpage:

        # search for url base
        index = s.find('span class="time-wrapper">')

        #if base found
        if index != -1:
            s = s[index:]
            s = s[26:]
            datearray = s.split(' ')
            day = datearray[1].strip(',')
            if len(str(day)) == 1:
                day = '0' + day
            return datearray[2] + monthsToDigits[datearray[0]] + day

    return False

# global dictionary with number of articles published per day
db = open('dates.pkl', 'rb')
dates = {}
try:
    dates = pickle.load(db)
except Exception as e:
    if "Ran out of input" in str(e):
        dates = {}
    else:
        print("ERROR:" + e)
db.close()

category = "sports" # CHANGE CATEGORY HERE
#filename = "links/" + category + ".txt"

filename = 'links/urls.txt'

# generate PDF for each URL
f = open(filename,'r')

for line in f:
    line = line.strip()
    date = get_date(line) # date published

    try:

        # check if there has already been articles published
        if date != False:
            if dates.get(date):
                dates[date] = dates[date] + 1
            else:
                dates[date] = 1

        print(line)
        generate_pdf(line, date, dates[date])
        db = open('dates.pkl', 'wb')
        pickle.dump(dates, db)
        db.close()
        print("[SUCCESS]: Dates saved successfully")
    except:
        print("[ERROR]: " + line)
        failed = open("failed.txt", 'a')
        failed.write(line)
        failed.close()

print("[COMPLETE]")


f.close()