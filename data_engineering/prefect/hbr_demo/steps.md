## Sequential conda commands (in terminal):
- `conda create -n prefect2 python=3.9 pandas`

- `conda activate prefect2`

- `conda install -c conda-forge prefect -y`

## Setting up Prefect Orion Server (in same terminal):
- `prefect orion start`

## Build & apply deployment for the example flow (new terminal):
- `conda activate prefect2`

- `prefect deployment build SCRIPT_NAME.py:FLOW_NAME -t dev`

- `prefect deployment apply FLOW_NAME-deployment.yaml`

