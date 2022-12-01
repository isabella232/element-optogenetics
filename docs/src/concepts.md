# Concepts

## Optogenetic Research

The seminal 2005 paper[^1] by Karl Deisseroth and colleagues established a strategy for
using light (*opto-*) to directly regulate the activation of genetically modified
(*-genetics*) neurons. By incorporating genes from photosensitive algae, neurons become
sensitive to different wavelengths for either excitation or inhibition.

In other areas of reseach, researchs can look at the correlation between neuronal
firings and animal behavior. By being able to look for the presence or absence of
behavior with or without optogenetic stimulation, researchers can draw more direct
causal links between neuronal populations and corresponding behavior.

[^1]: Boyden, E. S., Zhang, F., Bamberg, E., Nagel, G., & Deisseroth, K. (2005).
    [Millisecond-timescale, genetically targeted optical control of neural activity](https://www.nature.com/articles/nn1525).
    Nature neuroscience, 8(9), 1263-1268.

## Key Partnerships

Key members of the [U19 BrainCOGS project](https://www.braincogs.org/) at Princeton
University were consulted during development. The
[MATLAB U19 pipeline](https://github.com/BrainCOGS/U19-pipeline-matlab/tree/master/schemas/%2Boptogenetics)
serves as an important precursor project to this Element.

## Element Features

This Element stores key information about optogenetic stimulus protocols and their
implementation in a given recording session.

## Element Architecture

Each node in the following diagram represents the analysis code in the workflow and the
corresponding tables in the database.  Within the workflow, Element Optogenetics connects
to upstream Elements including Lab, Animal, Session, and Event.  For more detailed
documentation on each table, see the API docs for the respective schemas.

![element-optogenetics diagram](https://raw.githubusercontent.com/datajoint/element-optogenetics/main/images/diagram_opto.svg)

### `lab` schema ([API docs](../api/workflow_Optogenetics/pipeline/#workflow_Optogenetics.pipeline.Device))

| Table | Description |
| --- | --- |
| Device | Pulse sequence device |

### `subject` schema ([API docs](https://datajoint.com/docs/elements/element-animal/api/element_animal/subject))

- Although not required, most choose to connect the `Session` table to a `Subject` table.

| Table | Description |
| --- | --- |
| Subject | Basic information of the research subject |

### `session` schema ([API docs](https://datajoint.com/docs/elements/element-session/api/element_session/session_with_datetime))

| Table | Description |
| --- | --- |
| Session | Unique experimental session identifier |

### `opto` schema ([API docs](../api/element_optogenetics/optogenetics))

| Table | Description |
| --- | --- |
| WaveformType | Basic Waveform types (e.g., Square, Ramp, Sine) |
| Waveform | Waveform full characteristics, including type-specific part tables |
| Protocol | Stimulation protocol |
| SessionProtocol | Pairing of session and protocol |
| SessionBrainLocation | Pairing of session and brain surgery location information |

## Roadmap

Further development of this Element is community driven.  Upon user requests and based on guidance from the Scientific Steering Group we will add further features to this Element.
