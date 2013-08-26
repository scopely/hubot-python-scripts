# Description:
#   Looks up owner of a car from license plate by looking at a google doc
#
# Dependencies:
#   None
#
# Configuration:
#   LICENSE_PLATE_DOC
#
# Commands:
#   plate ASDF123
#
# Author:
#   maxgoedjen

import os
from os import environ
import csv

import requests

from scripts.hubot_script import *

URL = environ.get('HUBOT_LICENSE_PLATE_DOC', '')
MAKE = 'What is the make of your vehicle?'
MODEL = 'What is the model of your vehicle?'
COLOR = 'What color is your vehicle?'
PLATE = 'What is your license plate #?'
NAME = environ.get('HUBOT_LICENSE_PLATE_NAMEFIELD', '')


class LicensePlate(HubotScript):

    @hear('plate #? ?([a-z0-9]+)')
    def lookup_plate(self, message, matches):
        lookup_plate = matches[0].replace(' ', '').lower()
        csvrows = self.get_csv_rows(URL)
        mapping=self.get_mapping(csvrows[0])
        for row in csvrows:
            plate = row[mapping[PLATE]].replace(' ', '').replace('#', '').lower()
            if plate == lookup_plate:
                make = row[mapping[MAKE]]
                model = row[mapping[MODEL]]
                color = row[mapping[COLOR]]
                name = row[mapping[NAME]].title()
                return 'Plate {plate} is a {color} {make} {model} owned by {name}'.format(
                    plate=plate, color=color, make=make, model=model, name=name)
        return "I don't have any record of plate {plate}".format(plate=lookup_plate)

    def get_csv_rows(self, url):
        r = requests.get(url)
        text = unicode(r.text)
        csv_reader = csv.reader(text.splitlines())
        rows = list(csv_reader)
        return rows

    def get_mapping(self, row):
        mapping = {}
        fields = [MAKE, MODEL, COLOR, PLATE, NAME]
        for field in fields:
            mapping[field] = row.index(field)
        return mapping
