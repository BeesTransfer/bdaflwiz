"""
Provides remote instance models.
"""

class ShipmentTrack(dict):
    """
    Provides a shipment track resource class.
    """

    def __init__(self,
                 SEARCHON=None,
                 AWB=None,
                 CONSIGNEENAME=None,
                 CONSIGNORNAME=None,
                 CURRENTSTATUS=None,
                 DESTINATION=None,
                 ORIGIN=None,
                 PICKUPDATE=None,
                 SHIPMENTREFERENCENUMBER=None,
                 TOTALWEIGHT=None):
        """
        Constructs a :class:`ShipmentTrack` class instance.
        """
        self["SEARCHON"] = SEARCHON
        self["AWB"] = AWB
        self["CONSIGNEENAME"] = CONSIGNEENAME
        self["CONSIGNORNAME"] = CONSIGNORNAME
        self["CURRENTSTATUS"] = CURRENTSTATUS
        self["DESTINATION"] = DESTINATION
        self["ORIGIN"] = ORIGIN
        self["PICKUPDATE"] = PICKUPDATE
        self["SHIPMENTREFERENCENUMBER"] = SHIPMENTREFERENCENUMBER
        self["TOTALWEIGHT"] = TOTALWEIGHT
        self["CHECKPOINTS"] = list()
        self["CURRENTSTATUSDATETIME"] = None

    def add_cp(self, CP):
        self["CHECKPOINTS"].append(CP)
        self["CURRENTSTATUSDATETIME"] = CP["CHECKDATETIME"]


class ShipmentTrackCP(dict):
    """
    Provides a checkpoint resource representation.
    """

    def __init__(self,
                 CHECKDATE=None,
                 CHECKPOINT=None,
                 CHECKPOINTDESCRIPTION=None,
                 CHECKTIME=None,
                 LOCATIONNAME=None,
                 CHECKDATETIME=None):
        """
        Constructs a :class:`ShipmentTrackCP` class instance.
        """
        self["CHECKDATE"] = CHECKDATE
        self["CHECKPOINT"] = CHECKPOINT
        self["CHECKPOINTDESCRIPTION"] = CHECKPOINTDESCRIPTION
        self["CHECKTIME"] = CHECKTIME
        self["LOCATIONNAME"] = LOCATIONNAME
        self["CHECKDATETIME"] = CHECKDATETIME
