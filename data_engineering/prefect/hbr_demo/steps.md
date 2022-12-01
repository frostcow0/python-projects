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

Once you apply the deployment yaml file, the console will tell you to run `prefect agent start -q 'default'`. It's important that you ACTUALLY run `prefect agent start -q default`, without the single quotes around default, or your flow won't make it into the queue you've made.
