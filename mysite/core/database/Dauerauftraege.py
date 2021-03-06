'''
Created on 18.08.2017

@author: sebastian
'''

from datetime import datetime, date

from mysite.core.Frequency import FrequencsFunctions
from mysite.core.database.DatabaseObject import DatabaseObject
import pandas as pd


class Dauerauftraege(DatabaseObject):

    content = pd.DataFrame({}, columns=['Endedatum', 'Kategorie', 'Name', 'Rhythmus', 'Startdatum', 'Wert'])

    def parse(self, raw_table):
        raw_table['Startdatum'] = raw_table['Startdatum'].map(lambda x: datetime.strptime(x, "%Y-%m-%d").date())
        raw_table['Endedatum'] = raw_table['Endedatum'].map(lambda x: datetime.strptime(x, "%Y-%m-%d").date())
        self.content = self.content.append(raw_table, ignore_index=True)
        self.content = self.content.sort_values(by=['Startdatum'])

    def einnahmenausgaben_until_today(self, startdatum,
                                      endedatum, frequenzfunktion, name, wert, kategorie):
        '''
        compute all einnahmenausgaben until today
        '''
        laufdatum = startdatum
        frequency_function = FrequencsFunctions().get_function_for_name(frequenzfunktion)
        result = []
        while laufdatum < date.today() and laufdatum < endedatum:
            abbuchung = self._berechne_abbuchung(laufdatum, kategorie, name, wert)
            result.append(abbuchung)
            laufdatum = frequency_function(laufdatum)
        return result

    def get_all_einzelbuchungen_until_today(self):
        all_rows = pd.DataFrame()
        for _, row in self.content.iterrows():
            dauerauftrag_buchungen = self.einnahmenausgaben_until_today(row['Startdatum'], row['Endedatum'], row['Rhythmus'], row['Name'], row['Wert'], row['Kategorie'])
            for buchung in dauerauftrag_buchungen:
                all_rows = all_rows.append(buchung, ignore_index=True)
        return all_rows

    def add(self, startdatum, endedatum, kategorie, name, rhythmus, wert):
        neuer_dauerauftrag = pd.DataFrame(
            [[endedatum, kategorie, name, rhythmus, startdatum, wert]],
            columns=['Endedatum', 'Kategorie', 'Name', 'Rhythmus', 'Startdatum', 'Wert']
            )
        self.content = self.content.append(neuer_dauerauftrag, ignore_index=True)
        self.taint()
        print('DATABASE: Dauerauftrag hinzugefügt')

    def aktuelle(self):
        '''
        return aktuelle dauerauftraege
        '''
        dauerauftraege = self.content.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Endedatum > date.today()]
        dauerauftraege = dauerauftraege[dauerauftraege.Startdatum < date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)

    def get(self, db_index):
        db_row = self.content.loc[db_index]
        return self._row_to_dict(self.content.columns, db_index, db_row)

    def past(self):
        '''
        return vergangene dauerauftraege
        '''
        dauerauftraege = self.content.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Endedatum < date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)

    def future(self):
        '''
        return dauerauftraege aus der zukunft
        '''
        dauerauftraege = self.content.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Startdatum > date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)

    def edit(self, index, startdatum, endedatum, kategorie, name, rhythmus, wert):
        '''
        edit dauerauftrag for given index
        '''
        self.content.loc[self.content.index[[index]], 'Startdatum'] = startdatum
        self.content.loc[self.content.index[[index]], 'Endedatum'] = endedatum
        self.content.loc[self.content.index[[index]], 'Wert'] = wert
        self.content.loc[self.content.index[[index]], "Kategorie"] = kategorie
        self.content.loc[self.content.index[[index]], 'Name'] = name
        self.content.loc[self.content.index[[index]], 'Rhythmus'] = rhythmus
        self.taint()

    def delete(self, dauerauftrag_index):
        self.content = self.content.drop(dauerauftrag_index)
        self.taint()

    def _berechne_abbuchung(self, laufdatum, kategorie, name, wert):
        return pd.DataFrame([[laufdatum, kategorie, name, wert, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))

    def frame_to_list_of_dicts(self, dataframe):
        result_list = []
        for index, row_data in dataframe.iterrows():
            row = self._row_to_dict(dataframe.columns, index, row_data)
            result_list.append(row)
        return result_list

    def _row_to_dict(self, columns, index, row_data):
        row = {}
        row['index'] = index
        for key in columns:
            row[key] = row_data[key]
        return row
