from datetime import date
import unittest

from mysite.test.FileSystemStub import FileSystemStub
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import PostRequest
from mysite.core import FileSystem
from mysite.views import import_data
from mysite.viewcore import viewcore
from mysite.viewcore.converter import datum_from_german as datum
from mysite.viewcore import request_handler

# Create your tests here.
class Importd(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init_shouldReturnIndexPage(self):
        self.set_up()
        context = import_data.index(GetRequest())
        print(context)
        assert context['element_titel'] == 'Export / Import'

    _IMPORT_DATA = '''
    #######MaschinenimportStart
    Datum,Kategorie,Name,Wert,Dynamisch
    2017-03-06,Essen,Edeka,-10.0,True
    #######MaschinenimportEnd
    '''
    def test_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA}))
        assert context['element_titel'] == 'Export / Import'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54


    def test_addeUnpassendenKategorie_shouldShowImportMappingPage(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'unbekannt', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA}))
        assert context['element_titel'] == 'Kategorien zuweisen'

    def test_addeUnpassendenKategorie_mitPassendemMapping_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Unpassend', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA, 'Essen_mapping':'als Unpassend importieren'}))
        assert context['element_titel'] == 'Export / Import'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54