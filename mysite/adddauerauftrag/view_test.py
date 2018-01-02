'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + "/../")

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from adddauerauftrag import views
from core import DBManager
from core.DatabaseModule import Database
from viewcore import viewcore
from viewcore.converter import datum
from viewcore import request_handler


class TesteAddDauerauftragView(unittest.TestCase):
    testdb = None

    def set_up(self):
        print("create new database")
        testdb = DBManagerStub.setup_db_for_test()
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = views.index(GetRequest())
        assert context['approve_title'] == 'Dauerauftrag hinzufügen'

    def test_editCallFromUeberischt_presetValuesCorrect(self):
        self.set_up()

        testdb = viewcore.database_instance()
        testdb.dauerauftraege.add(datum('10.10.2010'), datum('10.10.2011'), '0kategorie', '0name', 'monatlich', 10)
        context = views.index(PostRequest({'action':'edit', 'edit_index':'0'}))
        assert context['approve_title'] == 'Dauerauftrag aktualisieren'

        preset = context['default_item']
        assert preset['Name'] == '0name'
        assert preset['Startdatum'] == '10.10.2010'
        assert preset['Endedatum'] == '10.10.2011'
        assert preset['Kategorie'] == '0kategorie'
        assert preset['Wert'] == '10,00'
        assert preset['typ'] == 'Einnahme'

        testdb.dauerauftraege.add(datum('10.10.2010'), datum('10.10.2011'), '0kategorie', '0name', 'monatlich', -10)
        context = views.handle_request(PostRequest({'action':'edit', 'edit_index':'1'}))
        preset = context['default_item']
        assert preset['typ'] == 'Ausgabe'



    def test_add_dauerauftrag(self):
        self.set_up()
        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "startdatum":"1.1.2017",
             "endedatum":"6.1.2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))


        testdb = viewcore.database_instance()
        assert len(testdb.dauerauftraege.content) == 1
        assert testdb.dauerauftraege.content.Wert[0] == -1 * float("2.00")
        assert testdb.dauerauftraege.content.Name[0] == "testname"
        assert testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert testdb.dauerauftraege.content.Startdatum[0] == datum("1.1.2017")
        assert testdb.dauerauftraege.content.Endedatum[0] == datum("6.1.2017")
        assert testdb.dauerauftraege.content.Rhythmus[0] == "monatlich"

    def test_add_dauerauftrag_einnahme(self):
        self.set_up()
        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "startdatum":"1.1.2017",
             "endedatum":"6.1.2017",
             "kategorie":"Essen",
             "typ":"Einnahme",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))

        testdb = viewcore.database_instance()
        assert len(testdb.dauerauftraege.content) == 1
        assert testdb.dauerauftraege.content.Wert[0] == float("2.00")
        assert testdb.dauerauftraege.content.Name[0] == "testname"
        assert testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert testdb.dauerauftraege.content.Startdatum[0] == datum("1.1.2017")
        assert testdb.dauerauftraege.content.Endedatum[0] == datum("6.1.2017")
        assert testdb.dauerauftraege.content.Rhythmus[0] == "monatlich"

    def test_edit_dauerauftrag(self):
        self.set_up()

        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "startdatum":"1.1.2017",
             "endedatum":"6.1.2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))


        print("dbs: " , viewcore.DATABASES)
        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "edit_index":"0",
             "startdatum":"2.1.2017",
             "endedatum":"5.1.2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        testdb = viewcore.database_instance()
        assert len(testdb.dauerauftraege.content) == 1
        assert testdb.dauerauftraege.content.Wert[0] == -1 * float("2.50")
        assert testdb.dauerauftraege.content.Name[0] == "testname"
        assert testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert testdb.dauerauftraege.content.Startdatum[0] == datum("2.1.2017")
        assert testdb.dauerauftraege.content.Endedatum[0] == datum("5.1.2017")

    def test_edit_dauerauftrag_ausgabe_to_einnahme(self):
        self.set_up()

        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "startdatum":"1.1.2017",
             "endedatum":"6.1.2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))


        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "edit_index":"0",
             "startdatum":"2.1.2017",
             "endedatum":"5.1.2017",
             "kategorie":"Essen",
             "typ":"Einnahme",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        testdb = viewcore.database_instance()
        assert len(testdb.dauerauftraege.content) == 1
        assert testdb.dauerauftraege.content.Wert[0] == float("2.50")
        assert testdb.dauerauftraege.content.Name[0] == "testname"
        assert testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert testdb.dauerauftraege.content.Startdatum[0] == datum("2.1.2017")
        assert testdb.dauerauftraege.content.Endedatum[0] == datum("5.1.2017")


    def test_edit_dauerauftrag_should_only_fire_once(self):
        self.set_up()

        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "startdatum":"1.1.2017",
             "endedatum":"6.1.2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))
        next_id = request_handler.current_key()
        views.index(PostRequest(
            {"action":"add",
             "ID":next_id,
             "edit_index":"0",
             "startdatum":"2.1.2017",
             "endedatum":"5.1.2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        views.index(PostRequest(
            {"action":"add",
             "ID":next_id,
             "edit_index":"0",
             "startdatum":"2.1.2017",
             "endedatum":"5.1.2017",
             "kategorie":"overwritten",
             "typ":"Ausgabe",
             "rhythmus":"overwritten",
             "name":"overwritten",
             "wert":"0,00"
             }
         ))

        testdb = viewcore.database_instance()
        assert len(testdb.dauerauftraege.content) == 1
        assert testdb.dauerauftraege.content.Wert[0] == -1 * float("2.50")
        assert testdb.dauerauftraege.content.Name[0] == "testname"
        assert testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert testdb.dauerauftraege.content.Startdatum[0] == datum("2.1.2017")
        assert testdb.dauerauftraege.content.Endedatum[0] == datum("5.1.2017")


    def test_add_dauerauftrag_should_only_fire_once(self):
        self.set_up()

        next_id = request_handler.current_key()
        views.index(PostRequest(
            {"action":"add",
             "ID":next_id,
             "startdatum":"2.1.2017",
             "endedatum":"5.1.2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        views.index(PostRequest(
            {"action":"add",
             "ID":next_id,
             "startdatum":"2.1.2017",
             "endedatum":"5.1.2017",
             "kategorie":"overwritten",
             "typ":"Ausgabe",
             "rhythmus":"overwritten",
             "name":"overwritten",
             "wert":"0,00"
             }
         ))

        testdb = viewcore.database_instance()
        assert len(testdb.dauerauftraege.content) == 1
        assert testdb.dauerauftraege.content.Wert[0] == -1 * float("2.50")
        assert testdb.dauerauftraege.content.Name[0] == "testname"
        assert testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert testdb.dauerauftraege.content.Startdatum[0] == datum("2.1.2017")
        assert testdb.dauerauftraege.content.Endedatum[0] == datum("5.1.2017")


if __name__ == '__main__':
    unittest.main()
