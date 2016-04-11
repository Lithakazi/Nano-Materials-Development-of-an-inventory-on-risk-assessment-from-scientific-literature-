import io
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from configparser import ConfigParser
import os


# read config file
config = ConfigParser()
config.read(r'datadir.ini')
direct = config.get('Path', 'Corpusdirectoy')
print(direct)
for (dirname, dirs, files) in os.walk(direct):
    # don't want to have this specific data in the code.  rather want to have a config file for each user and this will

    for filename in files:
        # if filename.endswith('.pdf'):  # and filename.endswith(',txt'):

        if not (filename.endswith('.pdf') and filename.endswith('.txt')):

            print(filename)

            # want to do the following only for the PDF files
            if filename.endswith('pdf'):
                # Open a PDF file.
                thefile = os.path.join(direct, filename)
                print(thefile)
                fp = open(thefile, 'rb')
                output = io.StringIO()

                # Create a PDF parser object associated with the file object.
                parser = PDFParser(fp)

                # Create a PDF document object that stores the document structure.
                # Supply the password for initialization.
                document = PDFDocument(parser)

                # Check if the document allows text extraction. If not, abort.
                if not document.is_extractable:
                    raise PDFTextExtractionNotAllowed

                # Create a PDF resource manager object that stores shared resources.
                manager = PDFResourceManager()

                # Create a PDF device object.
                #  device = PDFDevice(manager)

                device = TextConverter(manager, output, laparams=LAParams())

                # Create a PDF interpreter object.
                # converter = TextConverter(manager, output, laparams=LAParams())

                interpreter = PDFPageInterpreter(manager, device)

                # Process each page contained in the document.
                try:
                    for page in PDFPage.create_pages(document):
                        interpreter.process_page(page)
                except:
                    print("Error!")
                device.close()
                text = output.getvalue()

                # # writing to text file
                savefile = os.path.splitext(filename)[0]
                completename = '%s.txt' % savefile
                # filepath = os.path.join(direct, savefile)

                print(completename)
                filepath = os.path.join(direct, completename)
                # opening the file  with a specific encoding that can handle all the characters
                # to avoid errors when creating text files.
                text_file = open(filepath, 'w', encoding='utf-8')
                text_file.write(text)
                text_file.close()
