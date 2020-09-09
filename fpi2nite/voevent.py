import voeventdb.remote as vr
import voeventdb.remote.apiv1 as apiv1
from voeventdb.remote.apiv1 import FilterKeys, OrderValues
from voeventdb.remote.helpers import Synopsis
import datetime
import lxml.etree

import os

def get_swift(ndays=7):
    start_date = datetime.datetime.utcnow() - datetime.timedelta(days=ndays)
    obs_filters = {
        FilterKeys.role: 'observation',
        FilterKeys.authored_since: start_date,
        FilterKeys.stream: 'nasa.gsfc.gcn/SWIFT',
        FilterKeys.ivorn_contains: 'BAT_GRB_Pos',
        }
    swift_ivorns = apiv1.list_ivorn(filters=obs_filters)
    prog = ['A', 'B','C','D','E','F','G','H']
    swift_events = {}
    for ivorn in swift_ivorns:
        raw_xml = apiv1.packet_xml(ivorn)
        root = lxml.etree.fromstring(raw_xml)
        
        name = root.findall('./Why/Inference/Name')[0].text
        name = name.replace(' ', '')
        for key in swift_events.keys():
            if name in key:
                name = name + prog[(prog == key[-1]) + 1]
                break
        if name[-1] not in prog:
            name = name + prog[0]
            
        if 'null' in name:
            continue
        
        isot = root.findall('./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/'
                        'Time/TimeInstant/ISOTime')[0].text
        ra = root.findall('./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/'
                        'Position2D/Value2/C1')[0].text
        dec = root.findall('./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/'
                        'Position2D/Value2/C2')[0].text
                
        swift_events[name] = {'isot': isot,
                              'ra': ra,
                              'dec': dec}

    return swift_events

def get_fermi(ndays=7):
    start_date = datetime.datetime.utcnow() - datetime.timedelta(days=ndays)
    obs_filters = {
        FilterKeys.role: 'observation',
        FilterKeys.authored_since: start_date,
        FilterKeys.stream: 'nasa.gsfc.gcn/Fermi',
        FilterKeys.ivorn_contains: 'GBM_Fin_Pos',
        }
    fermi_ivorns = apiv1.list_ivorn(filters=obs_filters)
    fermi_events = {}
    for ivorn in fermi_ivorns:
        raw_xml = apiv1.packet_xml(ivorn)
        root = lxml.etree.fromstring(raw_xml)
        
        for param in root.findall('./What/Param'):
            if param.attrib['name'] == 'TrigID':
                name = 'FermiGBM-' + param.attrib['value']
                break
        
        isot = root.findall('./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/'
                        'Time/TimeInstant/ISOTime')[0].text
        ra = root.findall('./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/'
                        'Position2D/Value2/C1')[0].text
        dec = root.findall('./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/'
                        'Position2D/Value2/C2')[0].text
                
        fermi_events[name] = {'isot': isot,
                            'ra': ra,
                            'dec': dec}
    return fermi_events

def get_asassn(ndays=7):
    start_date = datetime.datetime.utcnow() - datetime.timedelta(days=ndays)
    obs_filters = {
        FilterKeys.role: 'observation',
        FilterKeys.authored_since: start_date,
        FilterKeys.ivorn_contains: 'ASASSN',
        }
    asassn_ivorns = apiv1.list_ivorn(filters=obs_filters)
    asassn_events  = {}
    for ivorn in asassn_ivorns:
        raw_xml = apiv1.packet_xml(ivorn)
        root = lxml.etree.fromstring(raw_xml)
        
        for param in root.findall('./What/Group/Param'):
            if param.attrib['name'] == 'id_other':
                name = param.attrib['value']
                name = name.replace('= ', '')
                break
            if param.attrib['name'] == 'id_assasn':
                name = param.attrib['value']
                break
        
        isot = root.findall('./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/'
                        'Time/TimeInstant/ISOTime')[0].text
        ra = root.findall('./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/'
                        'Position2D/Value2/C1')[0].text
        dec = root.findall('./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/'
                        'Position2D/Value2/C2')[0].text
                
        asassn_events[name] = {'isot': isot,
                            'ra': ra,
                            'dec': dec}
    return asassn_events

