import datajoint as dj

schema = dj.Schema()


def activate(schema_name, create_schema=True, create_tables=True, linking_module=None):
    """
    activate(schema_name, create_schema=True, create_tables=True)
        :param schema_name: schema name on the database server to activate the `optogenetics` element
        :param create_schema: when True (default), create schema in the database if it does not yet exist.
        :param create_tables: when True (default), create tables in the database if they do not yet exist.
        :param linking_module: a module name or a module containing the
         required dependencies to activate the `subject` element:
             Upstream tables:
                + Device: Reference table for OptoProtocol, device to perform optogenetics experiments
                + Session: Parent table to OptoSession, typically identifying a recording session
                + SessionTrial: Parent table to OptoTrial, passive trial or behavioral trial
                + BrainRegion: Reference table for OptoSession.BrainRegion, specifying the skull reference, such as bregma or lambda
                + SkullReference: Reference table for OptoSession.BrainLocation, specifying the brain region


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
    opto_waveform_name              : varchar(32)
    ---
    -> OptoWaveformType
    opto_normalized_waveform=null   : longblob    # Waveform for one cycle of the optogenetics stimulation, normalized to peak
    opto_waveform_description=''    : varchar(255)  # description of the waveform
    """

    class Square(dj.Part):
        definition = """
        -> master
        ---
        opto_on_proportion      : decimal(2, 2) # proportion of stim on time within a cycle
        opto_off_proportion     : decimal(2, 2) # proportion of stim off time within a cycle
        """

    class Ramp(dj.Part):
        definition = """
        -> master
        ---
        ramp_up_proportion    : decimal(2, 2)  # ramp up proportion of the linear waveform
        ramp_down_proportion  : decimal(2, 2)  # ramp down proportion of the linear waveform
        """

    class Sine(dj.Part):
        deinition = """
        -> master
        ---
        number_of_cycles  : smallint
        starting_phase=0  : decimal(3, 2) # (pi) phase of sine wave at the beginning of the cycle, ranging (0, 2], 0 for a Sine wave, 0.5 for a Cosine wave.
        """

    class CustomParameter(dj.Part):
        # Parameters
        definition = """
        -> master
        opto_waveform_parameter_name                 : varchar(32)
        ---
        opto_waveform_parameter_value=null           : float
        opto_waveform_parameter_value_str=null       : vachar(32)
        opto_waveform_parameter_value_blob=null      : blob
        """


@schema
class OptoProtocol(dj.Manual):
    definition = """
    # OptoProtocol defines a single opto stimulus repeat
    opto_protocol_id     : smallint
    ---
    -> OptoWaveform
    -> Device
    opto_wavelength      : smallint         # (nm) wavelength of the photo stimulation light
    opto_power           : decimal(6, 2)    # (mW) total power coming out of the light source
    opto_frequency       : decimal(5, 1)    # (Hz) frequency of waveform
    opto_duration        : decimal(5, 1)    # (ms) duration of each optostimulus
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

    class BrainRegion(dj.Part):
        definition = """
        -> master
        -> BrainRegion
        ---
        light_intensity   : decimal(6, 2)  # (mW/mm2) light intensity at each brain region
        """

    class BrainLocation(dj.Part):
        definition = """
        -> master
        location_id : int
        ---
        ap_location : decimal(6, 2) # (um) anterior-posterior; ref is 0; more anterior is more positive
        ml_location : decimal(6, 2) # (um) medial axis; ref is 0 ; more right is more positive
        depth       : decimal(6, 2) # (um) manipulator depth relative to surface of the brain (0); more ventral is more negative
        theta       : decimal(5, 2) # (deg) - elevation - rotation about the ml-axis [0, 180] - w.r.t the z+ axis
        phi         : decimal(5, 2) # (deg) - azimuth - rotation about the dv-axis [0, 360] - w.r.t the x+ axis
        -> BrainRegion
        light_intensity : decimal(6, 2) # (mW/mm2) light intensity at each brain location
        """


@schema
class OptoTrial(dj.Imported):
    definition = """
    -> SessionTrial
    -> OptoSession
    """

    class Event(dj.Part):
        definition = """
        -> master
        opto_event_id         :
        ---
        opto_stim_start_time  : float  # (ms) opto stimulus start time relative to the trial start
        opto_stim_end_time    : float  # (ms) opto stimulus end time relative to the trial start
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
