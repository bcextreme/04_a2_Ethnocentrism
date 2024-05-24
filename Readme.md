# Liu Qi Wang code
- Group 40
- Student Name: Xiaolin Liu, Student Id: 1486485
- Student Name: Yuning Qi, Student Id: 1420589
- Student Name: Ziqi Wang, Student Id: 1446535 

## Model File Structure
- `visual.py` - Is the entry to the model, contains functions to visualize the data generated from the simulation.
- `agent.py` - Contains the definition for the EthnocentrismAgent class, which defines agent behavior.
- `model.py` - Contains the EthnocentrismModel class that manages the simulation environment.
- `param.py` - Contains configuration parameters used by agents and the model.


## Running the Model
To run the model, you need to execute visual.py
This script will generate `agent_stats.csv` containing the relationship between the number of dissidents and step changes and `model_output.csv` containing information of all agents in each step:
- `python visual.py`

The above is the model implemented according to the assignment requirements, and the following is the file we used when doing experiments and writing reports, drawing the data in `agent_stats.csv` as a plot, for which we introduced external libraries pandas and matplotlib.

Note: This data plotng file is independent of the model, and it's just for converting the CSV file into images. After adding this file, the model can still run independently without relying on any external libraries.

## Generating Plots
First, make sure that the external libraries pandas and matplotlib for drawing lines are imported and that `agent_stats.csv` is also located in the current directory.
To generate plot, execute `plot_data.py`
- `python plot_data.py`

The generated `agent_cooperation.png` is a plot of population changes with the number of runs.

Again, this file is only for generating images that are used in the report. You will only need to use this when you want to replicate and test the experiments described in the report.



