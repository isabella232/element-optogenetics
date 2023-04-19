# Tutorials

+ DataJoint Elements are modular pipelines that can be connected into a complete workflow.  [Workflow Optogenetics](https://github.com/datajoint/workflow-optogenetics)) is an example that combines four DataJoint Elements - Lab, Animal, Session, and Optogenetics.

+ Workflow Optogenetics includes an [interactive tutorial on GitHub Codespaces](https://github.com/datajoint/workflow-optogenetics#interactive-tutorial), which is configured for users to run the pipeline.

+ In the interactive tutorial, the [example notebook](https://github.com/datajoint/workflow-optogenetics/tree/main/notebooks.tutorial.ipynb) describes the pipeline and provides instructions for adding data to the pipeline.

## Installation

Installation of the Element requires an integrated development environment and database.
Instructions to setup each of the components can be found on the 
[User Instructions](https://datajoint.com/docs/elements/user-guide/) page. These 
instructions use the example workflows
(e.g., [workflow-optogenetics](https://github.com/datajoint/workflow-optogenetics)), 
which can be modified for a user's specific experimental requirements.  This example
workflow uses four Elements (Lab, Animal, Session, and Optogenetics) to construct a
complete pipeline, and is able to ingest experimental metadata.

### Notebooks

Each of the 
[notebooks](https://github.com/datajoint/workflow-optogenetics/tree/main/notebooks) in 
the workflow steps through ways to interact with the Element itself. 

- [Configure](./01-configure.ipynb)
   helps configure your local DataJoint installation to point to the correct database.
- [Workflow Structure](./02-workflow-structure-optional.ipynb) demonstrates the table
   architecture of the Element and key DataJoint basics for interacting with these
   tables.
- [Process](./03-process.ipynb) steps through adding data to these tables.
