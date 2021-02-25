import logging
import os
import sys
from logging import getLogger
from os import path

import click
import cv2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


@click.command()
@click.option('--input', required=True)
@click.option('--output', required=True)
@click.option('--verbose', '-v', count=True)
def convertImageToText(input, output, verbose):
    checkValidFile = input.lower().endswith(('.png', '.jpeg', '.pdf'))
    logger = getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if checkValidFile is False or path.exists(input) is False:
        if (verbose):
            logger.error('Invalid File')
    else:
        image = cv2.imread(input)

        if (input.lower().endswith(('.pdf'))):
            converFromPdfName = 'convert_from_pdf.jpeg'
            images = convert_from_path(input)

            for img in images:
                img.save(converFromPdfName)
                image = cv2.imread(converFromPdfName)
                os.remove(converFromPdfName)

        rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, rgbImage)
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)

        if (verbose):
            logger.info('Convert successfully')

        sys.stdout = open(output + '.txt', 'w')
        click.echo(text)


convertImageToText()
