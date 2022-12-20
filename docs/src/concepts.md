# Concepts

## Optogenetic Research

The seminal 2005 paper[^1] by Karl Deisseroth and colleagues established a strategy for
using light (*opto-*) to directly regulate the activation of genetically modified
(*-genetics*) neurons. By incorporating genes from photosensitive algae, neurons become
sensitive to different wavelengths for either excitation or inhibition.
Scientists now use this technology to draw more direct
causal links between the activity of neuronal populations and corresponding animal behavior.

[^1]: Boyden, E. S., Zhang, F., Bamberg, E., Nagel, G., & Deisseroth, K. (2005).
    [Millisecond-timescale, genetically targeted optical control of neural activity](https://www.nature.com/articles/nn1525).
    Nature neuroscience, 8(9), 1263-1268.

## Key Partnerships

Key members of the [U19 BrainCoGS project](https://www.braincogs.org/) at Princeton
University were consulted during development. The
[U19 BrainCoGS MATLAB pipeline](https://github.com/BrainCOGS/U19-pipeline-matlab/tree/master/schemas/%2Boptogenetics)
serves as an important precursor project to this Element.

## Element Features

This Element stores key information about optogenetic stimulus protocols used during experimental sessions:
- Stimulus parameters (waveform properties, wavelength, power, duration, etc.)
- Implant location of the optical fiber.
- Stimulus pulse generator.
- Stimulus start and end times during an experimental session.

## Element Architecture

Each node in the following diagram represents the analysis code in the workflow and the
corresponding tables in the database.  Within the workflow, Element Optogenetics connects
to upstream Elements including Lab, Animal, and Session.  For more detailed
documentation on each table, see the API docs for the respective schemas.

![element-optogenetics diagram](https://raw.githubusercontent.com/datajoint/element-optogenetics/main/images/diagram_opto.svg)

### `reference` schema ([API docs](../api/workflow_Optogenetics/pipeline/#workflow_Optogenetics.reference.Device))

| Table | Description |
| --- | --- |
| Device | Pulse generator device |

### `subject` schema ([API docs](https://datajoint.com/docs/elements/element-animal/latest/api/element_animal/subject/#element_animal.subject.Subject))

- Although not required, most choose to connect the `Session` table to a `Subject` table.

| Table | Description |
| --- | --- |
| Subject | Basic information of the research subject |

### `surgery` schema ([API docs](https://datajoint.com/docs/elements/element-animal/latest/api/element_animal/surgery/#element_animal.surgery.Implantation))

- The `Implantation` table can be user-defined , or one can choose to use the `surgery.Implantation` table from `element-animal`.

| Table | Description |
| --- | --- |
| Implantation | Location of an implanted device |

### `session` schema ([API docs](https://datajoint.com/docs/elements/element-session/latest/api/element_session/session_with_id))

| Table | Description |
| --- | --- |
| Session | Unique experimental session identifier |

### `optogenetics` schema ([API docs](../api/element_optogenetics/optogenetics))

| Table               | Description |
| ---                 |   ---       |
| OptoWaveformType | Stimulus waveform type (e.g., square, ramp, sine) |
| OptoWaveform | Shape of one cycle of the stimulus waveform |
| OptoWaveform.Square | Square waveform properties |
| OptoWaveform.Ramp | Ramp waveform properties |
| OptoWaveform.Sine | Sine waveform properties |
| OptoStimParams | Stimulus parameters |
| OptoProtocol | Protocol for a given session |
| OptoEvent | Start and end time of the stimulus within a session |

## Roadmap

Further development of this Element is community driven.  Upon user requests and based
on guidance from the Scientific Steering Group we will add further features to this
Element.
