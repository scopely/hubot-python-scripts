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
SURVEY_URL = environ.get('HUBOT_LICENSE_PLATE_SURVEY_URL', '')

class LicensePlate(HubotScript):

    @hear('plate #? ?([a-z0-9]+)')
    def lookup_plate(self, message, matches):
        lookup_plate = matches[0].replace(' ', '').lower()
        csvrows = self.get_csv_rows(URL)
        mapping = self.get_mapping(csvrows[0])
        partials = []
        for row in csvrows:
            plate = row[mapping[PLATE]].replace(
                ' ', '').replace('#', '').lower()
            make = row[mapping[MAKE]]
            model = row[mapping[MODEL]]
            color = row[mapping[COLOR]]
            name = row[mapping[NAME]].title()
            description = 'Plate {plate} is a {color} {make} {model} owned by {name}'.format(
                plate=plate.upper(), color=color, make=make, model=model, name=name)
            if plate == lookup_plate:
                return description
            if lookup_plate in plate and len(lookup_plate) > 2:
                partials += [description]
        if partials:
            return 'No exact matches, the following plates partially matched:\n{0}'.format('\n'.join(partials))
        return "I don't know who the car with plate {0} belongs to".format(lookup_plate)

    @hear('who (?:owns|drives) (?:a|the) ([^\?]+)')
    def lookup_car(self, message, matches):
        search = matches[0].lower()
        csvrows = self.get_csv_rows(URL)
        mapping = self.get_mapping(csvrows[0])
        matches = []
        for row in csvrows:
            make = row[mapping[MAKE]]
            model = row[mapping[MODEL]]
            color = row[mapping[COLOR]]
            name = row[mapping[NAME]].title()
            search_description = '{color} {make} {model} {color} {model}'.format(
                color=color, make=make, model=model).lower()
            if search in search_description:
                description = '{name} owns a {color} {make} {model}'.format(
                    color=color.title(), make=make.title(), model=model.title(), name=name.title())
                matches += [description]
        if matches:
            return '\n'.join(matches)
        return "I don't know of anyone owning a {search}".format(
            search=search.title())
            
    @respond('new car')
    def link_survey_url(self, message, matches):
        if SURVEY_URL:
            return SURVEY_URL

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
