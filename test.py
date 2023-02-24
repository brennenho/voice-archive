# Used to generate a PDF from a specific URL
# URL entered by user in command line

import pdfkit

url = input("URL: ")
p = input("PRINT (y/n): ")

# Generate a PDF from a URL
def generate_pdf(url, date, count):

    filename = "VOI_" + date + "_0" + str(count)

    try:
        # always returns error, even when operation works
        if p == "y":
            pdfkit.from_url(url + "?print=true", filename + '.pdf')
        # get PDF directly from website
        else:
            pdfkit.from_url(url, filename + '.pdf')
    except:
        # catch error from PDFKIT to prevent it from printing
        pass



generate_pdf(url, "TEST", 1)

