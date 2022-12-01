import inspect
import importlib
import datajoint as dj

schema = dj.Schema()


def activate(
    schema_name: str,
    *,
    create_schema: bool = True,
    create_tables: bool = True,
    linking_module: bool = None
):
    """Activate this schema.

    Args:
        schema_name (str): schema name on the database server
        create_schema (bool): when True (default), create schema in the database if it
                            does not yet exist.
        create_tables (bool): when True (default), create schema tables in the database
                             if they do not yet exist.
        linking_module (str): a module (or name) containing the required dependencies.

    Dependencies:
        Upstream tables:
            Device: Referenced by Protocol. Device to perform procedure
            Session: Parent to Session. Typically identifying a recording session
            Trial: Parent to OptoTrial. Optionally from Element-Event
            Event: Parent to OptoTrial. Optionally from Element-Event
            SkullReference: Referenced by Session.SkullReference.
                Specifying the skull reference, such as bregma or lambda
    """

    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(
        linking_module
    ), "The argument 'dependency' must be a module's name or a module"

    global _linking_module
    _linking_module = linking_module

    # activate

    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=_linking_module.__dict__,
    )


@schema
class WaveformType(dj.Lookup):
    """
    Attributes:
        waveform_type ( varchar(32) ): Waveform type (e.g., square, sine)
    """

    definition = """
    waveform_type:    varchar(32)
    """
    contents = zip(["Square", "Ramp", "Sine"])


@schema
class Waveform(dj.Lookup):
    """OptoWaveform defines the shape of one cycle of the optogenetic stimulus

    Attributes:
        waveform_name ( varchar(32) ): Name of waveform
        OptoWaveformType (foreign key): OptoWaveformType primary key
        normalized_waveform (longblob, nullable): For one cycle, normalized to peak
        waveform_description ( varchar(255), nullable ): Description
    """

    definition = """
    # OptoWaveform defines the shape of one cycle of the optogenetic stimulus
    waveform_name            : varchar(32)
    ---
    -> WaveformType
    normalized_waveform=null : longblob      # For one cycle, normalized to peak
    waveform_description=''  : varchar(255)  # description of the waveform
    """

    class Square(dj.Part):
        """Square waveform

        Attributes:
            OptoWaveform (foreign key): OptoWaveform primary key
            on_proportion ( decimal(2, 2) ): Proportion of stim on time within a cycle
            off_proportion ( decimal(2, 2) ): Proportion of stim off time within a cycle
        """

        definition = """
        -> master
        ---
        on_proportion  : decimal(2, 2) # prop of stim on time within a cycle
        off_proportion : decimal(2, 2) # prop of stim off time within a cycle
        """

    class Ramp(dj.Part):
        """Ramp waveform

        Attributes:
            OptoWaveform (foreign key): OptoWaveform primary key
            ramp_up_proportion ( decimal(2, 2) ): Ramp up proportion of the linear waveform
            ramp_down_proportion ( decimal(2, 2) ): Ramp down proportion of the linear waveform
        """

        definition = """
        -> master
        ---
        ramp_up_proportion   : decimal(2, 2) # ramp up prop of the linear waveform
        ramp_down_proportion : decimal(2, 2) # ramp down prop of the linear waveform
        """

    class Sine(dj.Part):
        """Sine Waveform. Starting_phase ranges (0, 2]. 0 for Sine, 0.5 for Cosine

        Attributes:
            OptoWaveform (foreign key): OptoWaveform primary key
            number_of_cycles (smallint): Number of cycles
            starting_phase (decimal(3, 2) ): Phase in pi at the beginning of the cycle.
                Defaults to 0
        """

        definition = """ # Starting_phase ranges (0, 2]. 0 for Sine, 0.5 for Cosine
        -> master
        ---
        number_of_cycles  : smallint
        starting_phase=0  : decimal(3, 2) # (pi) phase at the beginning of the cycle
        """

    class CustomParameter(dj.Part):
        """Custom optogenetic stimulation waveform parameters

        Attributes:
            OptoWaveform (foreign key): OptoWaveform primary key
            waveform_parameter_name ( varchar(32) ): Parameter name
            waveform_parameter_value (float, nullable): Parameter numerical value
            waveform_parameter_value_str ( varchar(32), nullable): Parameter string value
            waveform_parameter_value_blob (blob, nullable): Parameter blob
        """

        definition = """ # Custom optogenetic stimulation waveform parameters
        -> master
        waveform_parameter_name                 : varchar(32)
        ---
        waveform_parameter_value=null           : float
        waveform_parameter_value_str=null       : varchar(32)
        waveform_parameter_value_blob=null      : blob
        """


@schema
class OptoProtocol(dj.Manual):
    """Protocol defines a single opto stimulus that repeats

    Attributes:
        protocol_id (smallint): Protocol ID
        OptoWaveform (foreign key): OptoWaveform primary key
        Device (foreign key): Device primary key
        wavelength (smallint): Wavelength in nm of photo stim. light
        power ( decimal(6, 2) ): Total power in mW from light source
        frequency ( decimal(5, 1) ): Frequency in Hz of the waveform
        duration ( decimal(5, 1) ): Duration in ms of each optostimulus
        protocol_description ( varchar(255) ): Protocol description
    """

    definition = """
    # Protocol defines a single opto stimulus that repeats
    protocol_id     : smallint
    ---
    -> Waveform
    -> Device
    wavelength      : smallint              # (nm) wavelength of photo stim. light
    power           : decimal(6, 2)         # (mW) total power from light source
    frequency       : decimal(5, 1)         # (Hz) frequency of the waveform
    duration        : decimal(5, 1)         # (ms) duration of each optostimulus
    protocol_description='' : varchar(255)  # description of optogenetics protocol
    """


@schema
class SessionProtocol(dj.Manual):
    """Session protocol

    Attributes:
        Session (foreign key): Session primary key
        OptoProtocol (foreign key): OptoProtocol primary key
    """

    definition = """
    -> Session
    -> OptoProtocol
    """


@schema
class SessionBrainLocation(dj.Manual):
    """Session brain location

    WRT: With Respect To

    Attributes:
        Session (foreign key): Session primary key
        location_id (int): ID of of brain location
        ap_location ( decimal(6, 2) ): In um, Anterior/posterior; Anterior Positive
        ml_location ( decimal(6, 2) ): In um, medial axis; Right Positive
        depth ( decimal(6, 2) ): In um, Relative to surface (0); Ventral Negative
        theta ( decimal(5, 2) ): Elevation in degrees. Rotation about
            ml-axis [0, 180] WRT Z
        phi ( decimal(5, 2) ): Azimuth in degrees. Rotations about
            dv-axis [0, 360] WRT X
        SkullReference (foreign key): SkullReference primary key
        light_intensity ( decimal(6, 2) ): (mW/mm2) light intensity at this location
        description ( varchar(255), nullable): brain location description
    """

    definition = """
    -> Session
    location_id : int
    ---
    ap_location : decimal(6, 2) # (um) anterior-posterior; ref 0; Anterior Positive
    ml_location : decimal(6, 2) # (um) medial axis; ref 0; Right Positive
    depth       : decimal(6, 2) # (um) Relative to surface (0); Ventral Negative
    theta       : decimal(5, 2) # (deg) Elevation - rot about ml-axis [0, 180] WRT Z
    phi         : decimal(5, 2) # (deg) Azimuth - rot about dv-axis [0, 360] WRT X
    -> SkullReference
    light_intensity : decimal(6, 2) # (mW/mm2) light intensity at each location
    description=""  : varchar(255) # Brain region description
    """
