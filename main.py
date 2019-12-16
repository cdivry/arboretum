#!/usr/bin/env python3

import json

def get_keywords(el):
    keyw = el['properties']['nomfrancais']
    if el['properties']['nomlatin']:
        keyw += " " + el['properties']['nomlatin']
    if keyw == None:
        keyw = "element"
    else:
        keyw.replace('.', ' ').replace('\'', ' ').replace('"', ' ')
        keyw = "element " + ' '.join(keyw.lower().split())
    return (keyw)


def update_html_tri(elements):

    # tri
    elements = sorted(elements, key=lambda e: e['nom'])
    print("Elements: " + str(len(elements)))

    # reorganisation par espece
    _tmp = {}
    for e in elements:
        if e['nom'] not in _tmp or not _tmp[e['nom']]:
            _tmp[e['nom']] = {
                'keywords': e['keywords'],
                'list': [],
            }
        _tmp[e['nom']]['list'] += [e]

    content = ""
    for espece in _tmp:
        content += """
        <div class="%(class)s">
        <h3 onclick="el_display(this.parentElement)">%(nom)s (%(pop)s)</h3>
        """ % {
            'class': _tmp[espece]['keywords'],
            'nom': espece,
            'pop': str(len(_tmp[espece]['list'])),
        }
        for el in _tmp[espece]['list']:
            content += """
            <div class="subelement">
            <a target="_blank" href="%(gmap)s" title="Google Maps">(gmap)</a> - 
            <a target="_blank" href="%(qmap)s" title="Qwant Maps">(qmap)</a> - 
            <i>%(endroit)s</i>
            </div>
            """ % el
        content += "</div>"

    with open('files/style.css', 'r') as fd:
        css = fd.read()
    with open('files/template.html', 'r') as fd:
        page = fd.read()
        html = page % {
            'LISTING': content,
            'CSS': css,
        }
    with open('www/index.html', 'w') as fd:
        fd.write(html)

def check_element(el):
    # nom
    if not el['properties']['nomfrancais']:
        return (False)
    if el['properties']['nomfrancais'] == "RAS":
        return (False)
    # GPS
    if not el['geometry']:
        return (False)
    if not el['geometry']['coordinates']:
        return (False)
    return (True)

def get_params(el):
    _tmp = {
        'latitude': el['geometry']['coordinates'][1],
        'longitude': el['geometry']['coordinates'][0],
        'nom': el['properties']['nomfrancais'],
        'endroit': el['properties']['clc_secteur'],
        'keywords': get_keywords(el),
    }
    _tmp['gmap'] = "https://www.google.com/maps/@%(latitude)s,%(longitude)s,10m/data=!3m1!1e3" % _tmp
    _tmp['qmap'] = "https://www.qwant.com/maps/#map=77/%(latitude)s/%(longitude)s" % _tmp
    return (_tmp)

def update_binary():
    with open('input.json', 'r') as fd:
        res = json.load(fd)
        elements = []
        for el in res['features']:
            #print(json.dumps(el, indent=4, sort_keys=True))
            if not check_element(el):
                continue
            elements.append(get_params(el))
        update_html_tri(elements)

if __name__ == '__main__':
    update_binary()
