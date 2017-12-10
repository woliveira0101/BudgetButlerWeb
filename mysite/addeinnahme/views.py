
from viewcore import viewcore
from viewcore import request_handler
from viewcore.converter import datum, dezimal_float, from_double_to_german


def handle_request(request):
    context = viewcore.generate_base_context('addeinnahme')
    context['element_titel'] = 'Neue Einnahme'
    context['page_subtitle'] = 'Daten der Einnahme:'
    context['approve_title'] = 'Einnahme hinzufügen'
    einzelbuchungen = viewcore.database_instance().einzelbuchungen

    if request.method == 'POST' and request.POST['action'] == 'add':
        print(request.POST)
        if 'edit_index' in request.POST:
            einzelbuchungen.edit(
                int(request.POST['edit_index']),
                datum(request.POST['date']),
                request.POST['kategorie'],
                request.POST['name'],
                dezimal_float(request.POST['wert']))
            viewcore.add_changed_einzelbuchungen(
                {
                    'fa':'pencil',
                    'datum':str(datum(request.POST['date'])),
                    'kategorie':request.POST['kategorie'],
                    'name':request.POST['name'],
                    'wert':from_double_to_german(dezimal_float(request.POST['wert']))
                    })

        else:
            einzelbuchungen.add(
                datum(request.POST['date']),
                request.POST['kategorie'],
                request.POST['name'],
                dezimal_float(request.POST['wert']))
            viewcore.add_changed_einzelbuchungen(
                {
                    'fa':'plus',
                    'datum':str(datum(request.POST['date'])),
                    'kategorie':request.POST['kategorie'],
                    'name':request.POST['name'],
                    'wert':from_double_to_german(dezimal_float(request.POST['wert']))
                    })
        viewcore.save_database()

    if request.method == 'POST' and request.POST['action'] == 'edit':
        print('Please edit:', request.POST['edit_index'])
        db_index = int(request.POST['edit_index'])
        selected_item = einzelbuchungen.get(db_index)
        selected_item['Datum'] = str(selected_item['Datum'].day) + '/' + str(selected_item['Datum'].month) + '/' + str(selected_item['Datum'].year)
        selected_item['Wert'] = from_double_to_german(selected_item['Wert'])
        context['default_item'] = selected_item
        context['bearbeitungsmodus'] = True
        context['edit_index'] = db_index
        context['set_kategorie'] = True
        context['element_titel'] = 'Einnahme Nr.' + str(db_index) + ' bearbeiten'
        context['page_subtitle'] = 'Daten bearbeiten:'
        context['approve_title'] = 'Einnahme aktualisieren'

    context['kategorien'] = sorted(einzelbuchungen.get_kategorien_einnahmen())
    context['letzte_erfassung'] = reversed(viewcore.get_changed_einzelbuchungen())
    context['transaction_key'] = 'requested'
    return context

def index(request):
    return request_handler.handle_request(request, handle_request, 'theme/addeinnahme.html')
