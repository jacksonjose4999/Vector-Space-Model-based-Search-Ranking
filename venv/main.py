import glob, os
from typing import Type

import PyPDF2


def read_files(path):
    os.chdir(path)
    size = 0
    f = ""
    for file in glob.glob("*.pdf"):
        size += 1
        f = file

    docs = [f] * (size)
    j = 0
    for file in glob.glob("*.pdf"):
        print(file)
        docs[j] = file
        j += 1
        # creating a pdf file object
        pdfFileObj = open(file, 'rb')
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # printing number of pages in pdf file
        print(pdfReader.numPages)
        # creating a page object
        for i in range(0, pdfReader.numPages - 1):
            pageObj = pdfReader.getPage(0)
            # extracting text from page
            # print(pageObj.extractText())
            # closing the pdf file object
            pdfFileObj.close()
    print(docs)


def main():
    read_files("/Users/jacksonjose/PycharmProjects/VectorSpaceModel/venv/corpus")


if __name__ == '__main__':
    main()
