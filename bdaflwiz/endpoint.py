"""
Provides the endpoint access for :mod:`bdaflwiz` module.
"""

from bdaflwiz import xml2json
from bdaflwiz.config import Configuration
from bdaflwiz.resources import ShipmentTrack
from bdaflwiz.resources import ShipmentTrackCP
from dateutil.parser import parse as parse_datetime
from decimal import Decimal
import json
import urllib

class NoMatchFound(Exception):
    """
    Indicates that there is no match found for the search.
    """
    pass

class Endpoint(object):
    """
    Provides an endpoint access class.
    """

    def __init__(self, config=Configuration()):
        """
        Constructs a :class:`Endpoint` class instance.
        """
        self.config = config

    def search(self, search_value, search_key=None):
        """
        Searches and returns a ShipmentTrack instance for the given
        keyword. If nothing found, raises :class:`NoMatchFound`
        exception.
        """
        url = self.config.get_url(search_value, search_key)
        resource_as_xml = urllib.urlopen(url).read()
        resource_as_json = xml2json.xml2json(resource_as_xml)
        resource_as_dict = json.loads(resource_as_json)

        if not isinstance(resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"], dict):
            raise NoMatchFound("No match found for %s" % (search_value))

        st = ShipmentTrack(
            SEARCHON=parse_datetime(resource_as_dict["SHIPMENTTRACK"]["SEARCHON"]),
            AWB=resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["AWB"],
            CONSIGNEENAME=resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["CONSIGNEENAME"],
            CONSIGNORNAME=resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["CONSIGNORNAME"],
            CURRENTSTATUS=resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["CURRENTSTATUS"],
            DESTINATION=resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["DESTINATION"],
            ORIGIN=resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["ORIGIN"],
            PICKUPDATE=parse_datetime(resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["PICKUPDATE"]),
            SHIPMENTREFERENCENUMBER=resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["SHIPMENTREFERENCENUMBER"],
            TOTALWEIGHT=Decimal(resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["TOTALWEIGHT"]))

        cps_raw = resource_as_dict["SHIPMENTTRACK"]["SHIPMENTREPORT"]["CHECKPOINTDETAILS"]["CHECKPOINTS"]
        cps_tba = []
        if isinstance(cps_raw, list):
            for cp in cps_raw:
                cps_tba.append(ShipmentTrackCP(
                    CHECKDATE=cp["CHECKDATE"],
                    CHECKPOINT=cp["CHECKPOINT"],
                    CHECKPOINTDESCRIPTION=cp["CHECKPOINTDESCRIPTION"],
                    CHECKTIME=cp["CHECKTIME"],
                    LOCATIONNAME=cp["LOCATIONNAME"],
                    CHECKDATETIME=parse_datetime("%s %s" % (cp["CHECKDATE"], cp["CHECKTIME"]))))
        else:
            cp = cps_raw
            cps_tba.append(ShipmentTrackCP(
                CHECKDATE=cp["CHECKDATE"],
                CHECKPOINT=cp["CHECKPOINT"],
                CHECKPOINTDESCRIPTION=cp["CHECKPOINTDESCRIPTION"],
                CHECKTIME=cp["CHECKTIME"],
                LOCATIONNAME=cp["LOCATIONNAME"],
                CHECKDATETIME=parse_datetime("%s %s" % (cp["CHECKDATE"], cp["CHECKTIME"]))))
        cps_tba = sorted(cps_tba, key=lambda x: x["CHECKDATETIME"])
        for cp in cps_tba:
            st.add_cp(cp)
        return st
