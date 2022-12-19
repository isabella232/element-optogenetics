# Tutorials

## Installation

Installation of the Element requires an integrated development environment and database.
Instructions to setup each of the components can be found on the 
[User Instructions](https://datajoint.com/docs/elements/user-guide/) page. These 
instructions use the example workflows
(e.g., [workflow-optogenetics](https://github.com/datajoint/workflow-optogenetics)), 
which can be modified for a user's specific experimental requirements.  This example
workflow uses four Elements (Lab, Animal, Session, and Optogenetics) to construct a
complete pipeline, and is able to ingest experimental metadata.

<!-- ### Videos

The [Element Optogenetics tutorial](https://www.youtube.com/watch?v=8FDjTuQ52gQ) gives an 
overview of the workflow files and notebooks as well as core concepts related to 
optogenetics research.

[![YouTube tutorial](https://img.youtube.com/vi/8FDjTuQ52gQ/0.jpg)](https://www.youtube.com/watch?v=8FDjTuQ52gQ) -->

### Notebooks

Each of the 
[notebooks](https://github.com/datajoint/workflow-optogenetics/tree/main/notebooks) in 
the workflow steps through ways to interact with the Element itself. 

- [Configure](./01-Configure.ipynb)
   helps configure your local DataJoint installation to point to the correct database.
- [Workflow Structure](./02-WorkflowStructure_Optional.ipynb) demonstrates the table
   architecture of the Element and key DataJoint basics for interacting with these
   tables.
- [Process](./03-Process.ipynb) steps through adding data to these tables.
