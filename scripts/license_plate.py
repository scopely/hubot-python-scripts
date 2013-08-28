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

    @hear('drives (?:a|the) ([a-z]+ )?([a-z]+) (.+)')
    def lookup_car(self, message, matches):
        lookup_color, lookup_make, lookup_model = matches
        lookup_make, lookup_model = lookup_make.lower(), lookup_model.lower().strip()
        if lookup_color:
            lookup_color = lookup_color.lower().strip()
        csvrows = self.get_csv_rows(URL)
        mapping = self.get_mapping(csvrows[0])
        matches = []
        for row in csvrows:
            make = row[mapping[MAKE]].lower()
            model = row[mapping[MODEL]].lower()
            color = row[mapping[COLOR]].lower()
            plate = row[mapping[PLATE]].lower()
            name = row[mapping[NAME]].title()
            if make == lookup_make and model == lookup_model:
                description = '{name} owns a {color} {make} {model} with plate {plate}'.format(
                    color=color.title(), make=make.title(), model=model.title(), name=name.title(), plate=plate.upper())
                if lookup_color:
                    if color == lookup_color:
                        matches += [description]
                else:
                    matches += [description]
        if matches:
            return '\n'.join(matches)
        if lookup_color:
            return "I don't know of anyone owning a {color} {make} {model}".format(
                color=lookup_color.title(), make=lookup_make.title(), model=lookup_model.title())
        return "I don't know of anyone owning a {make} {model}".format(
            make=lookup_make.title(), model=lookup_model.title())

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
