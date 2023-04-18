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

## Element Roadmap

This Element stores key information about optogenetic stimulus protocols used during 
experimental sessions.  Further development of this Element is community driven.  Upon 
user requests and based on guidance from the Scientific Steering Group we will add 
further features to this Element. 

- [x] Stimulus parameters (waveform properties, wavelength, power, duration, etc.)
- [x] Implant location of the optical fiber
- [x] Stimulus pulse generator
- [x] Stimulus start and end times during an experimental session
