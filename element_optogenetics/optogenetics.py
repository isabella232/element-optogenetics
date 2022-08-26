import datajoint as dj

schema = dj.Schema()


def activate(schema_name, create_schema=True, create_tables=True):
    """
    activate(schema_name, create_schema=True, create_tables=True)
        :param schema_name: schema name on the database server to use on activation
        :param create_schema: when True (default), create schema if nonexistent
        :param create_tables: when True (default), create tables if nonexistent
        :param linking_module: a module name or module containing required dependencies

    Upstream tables:
        + Device: Referenced by OptoProtocol. Device to perform procedure
        + Session: Parent to OptoSession. Typically identifying a recording session
        + Trial: Parent to OptoTrial. Optionally from Element-Event
        + Event: Parent to OptoTrial. Optionally from Element-Event
        + BrainRegion: Referenced by OptoSession.BrainRegion.
                       Specifying the skull reference, such as bregma or lambda
        + SkullReference: Referenced by OptoSession.BrainLocation.
                          Specifying brain region
    """

    schema.activate(
        schema_name, create_schema=create_schema, create_tables=create_tables
    )


@schema
class OptoWaveformType(dj.Lookup):
    definition = """
    opto_waveform_type:    varchar(32)
    """
    contents = zip(["Square", "Ramp", "Sine"])


@schema
class OptoWaveform(dj.Lookup):
    definition = """
    # OptoWaveform defines the shape of one cycle of the optogenetic stimulus
    opto_waveform_name            : varchar(32)
    ---
    -> OptoWaveformType
    opto_normalized_waveform=null : longblob      # For one cycle, normalized to peak
    opto_waveform_description=''  : varchar(255)  # description of the waveform
    """

    class Square(dj.Part):
        definition = """
        -> master
        ---
        opto_on_proportion  : decimal(2, 2) # prop of stim on time within a cycle
        opto_off_proportion : decimal(2, 2) # prop of stim off time within a cycle
        """

    class Ramp(dj.Part):
        definition = """
        -> master
        ---
        ramp_up_proportion   : decimal(2, 2) # ramp up prop of the linear waveform
        ramp_down_proportion : decimal(2, 2) # ramp down prop of the linear waveform
        """

    class Sine(dj.Part):
        deinition = """ # Starting_phase ranges (0, 2]. 0 for Sine, 0.5 for Cosine
        -> master
        ---
        number_of_cycles  : smallint
        starting_phase=0  : decimal(3, 2) # (pi) phase at the beginning of the cycle
        """

    class CustomParameter(dj.Part):
        definition = """ # Custom optogenetic stimulation waveform parameters
        -> master
        opto_waveform_parameter_name                 : varchar(32)
        ---
        opto_waveform_parameter_value=null           : float
        opto_waveform_parameter_value_str=null       : vachar(32)
        opto_waveform_parameter_value_blob=null      : blob
        """


@schema
class OptoProtocol(dj.Manual):  # TODO: Add hash?
    definition = """
    # OptoProtocol defines a single opto stimulus that repeats
    opto_protocol_id     : smallint
    ---
    -> OptoWaveform
    -> Device
    opto_wavelength      : smallint              # (nm) wavelength of photo stim. light
    opto_power           : decimal(6, 2)         # (mW) total power from light source
    opto_frequency       : decimal(5, 1)         # (Hz) frequency of the waveform
    opto_duration        : decimal(5, 1)         # (ms) duration of each optostimulus
    opto_protocol_description='' : varchar(255)  # description of optogenetics protocol
    """


@schema
class OptoSession(dj.Manual):
    definition = """
    -> Session
    """

    class Protocol(dj.Part):
        definition = """
        -> master
        -> OptoProtocol
        """

    class BrainRegion(dj.Part):  # TODO: split coordinate_framework.py to own Element?
        definition = """
        -> master
        -> BrainRegion
        ---
        light_intensity   : decimal(6, 2)  # (mW/mm2) light intensity for brain region
        """

    class BrainLocation(dj.Part):
        definition = """
        -> master
        location_id : int
        ---
        ap_location : decimal(6, 2) # (um) anterior-posterior; ref 0; Anterior Positive
        ml_location : decimal(6, 2) # (um) medial axis; ref 0; Right Positive
        depth       : decimal(6, 2) # (um) Relative to surface (0); Ventral Negative
        theta       : decimal(5, 2) # (deg) Elevation - rot about ml-axis [0, 180] WRT Z
        phi         : decimal(5, 2) # (deg) Azimuth - rot about dv-axis [0, 360] WRT X
        -> BrainRegion
        light_intensity : decimal(6, 2) # (mW/mm2) light intensity at each location
        """


@schema
class OptoTrial(dj.Imported):
    definition = """
    -> Trial
    -> OptoSession
    """

    class OptoEvent(dj.Part):  # TODO: Pull from element-event?
        definition = """
        -> master
        -> Event
        ---
        -> OptoSession.Protocol
        """

    class BrainRegion(dj.Part):
        definition = """
        -> master
        -> OptoSession.BrainRegion
        """

    class BrainLocation(dj.Part):
        definition = """
        -> master
        -> OptoSession.BrainLocation
        """
