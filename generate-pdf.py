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

    except:
        # Catch error from PDFKit
        pass

    # Move PDF to subdirectory
    shutil.move(filename + '.pdf', 'pdfs/' + date[:4] + '/' + filename + '.pdf')


def get_date(url):
    # read website code from specified url
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
    # split code by "<" into a list
    webpage = str(urlopen(req).read()).split('<')

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

# open backed-up database file -> used if program crashes
db = open('dates.pkl', 'rb')

# global dictionary with number of articles published per day
dates = {}
try:
    # attempt to load backed-up database
    dates = pickle.load(db)
except Exception as e:
    # if there is nothing in the database file, set the database to empty
    if "Ran out of input" in str(e):
        dates = {}
    else:
        # There was an error in importing the previous database
        print("ERROR:" + e)

# close database back-up file
db.close()


# Uncomment the lines below if backing up category-by-category
# category = "sports" # CHANGE CATEGORY HERE if backing up category-by-category
# filename = "links/" + category + ".txt"

# Comment line below if backing up category-by-category
filename = 'links/urls.txt'

# open file with urls
f = open(filename,'r')

# iterate through each line in the url file
for line in f:
    # strip whitespace
    line = line.strip()
    # get the data published
    date = get_date(line)

    try:
        # check if there has already been articles published
        if date != False:
            if dates.get(date):
                dates[date] = dates[date] + 1
            else:
                dates[date] = 1

        print(line)
        # call function to generate pdf from url
        generate_pdf(line, date, dates[date])

        # backup date database immediately after generating a url in the case of a crash
        db = open('dates.pkl', 'wb')
        pickle.dump(dates, db)
        db.close()

        # iteration successful
        print("[SUCCESS]: Dates saved successfully")
    except:
        print("[ERROR]: " + line)

        # store failed url in a separate file to assist debugging and re-running
        failed = open("failed.txt", 'a')
        failed.write(line)
        failed.close()

print("PROGRAM COMPLETE")


f.close()