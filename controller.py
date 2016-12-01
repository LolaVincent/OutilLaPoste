#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vue import *
from model import *

class Controller():
    def __init__(self):
        self.model=Model()
        a=list()
        a.append("TEst")
        self.vue=FenetrePrincipale(self.model.readDirectory(),self.model.readSites())
