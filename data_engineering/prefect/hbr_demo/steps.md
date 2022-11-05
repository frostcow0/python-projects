## Sequential conda commands (in terminal):
- `conda create -n prefect2 python=3.9`

- `conda activate prefect2`

- `conda install prefect -y`

- `conda install pandas -y`

## Setting up Prefect Orion Server (in same terminal):
- `prefect orion start`

## Build & apply deployment for the example flow (new terminal):
- `conda activate prefect2`

- `prefect deployment build prefect_flow_example.py:covid_data -n covid_data-deployment -t dev`

- `prefect deployment apply covid_data-deployment.yaml`

