# FINAL PROJECT

## INTRODUCTION
The data was accessed from the US Census and CMS (Centre for Medicare and Medicaid Services) marketplace websites.
I chose data related to health insurance and patient demographics, in order to see if socioeconomic determinants of health can impact a patient’s access to and utilization of healthcare.
Based on user input, data for insurance numbers, age, race and population under federal poverty line will be displayed in plots.

# REQUIRED PACKAGES :
•	Pandas (pip install pandas)
•	Requests (pip install requests)
•	Matplotlib (pip install matplotlib)
•	Numpy (pip install numpy)
•	Plotly (pip install plotly)

## ACCESSING DATA USING APIs
The data was accessed using the US Census and CMS HTTP REST API’s.
•	The first dataset was accessed using US Census API with the following URL -
https://api.census.gov/data/timeseries/healthins/sahie?get=NIC_PT,NUI_PT,PCTIC_PT,PCTUI_PT,NAME,AGECAT,IPRCAT,RACECAT&for=state:{us_state_codes[state_code]}&time=2008&key={CENSUS_API_KEY}
Census API key, obtained on requesting from https://api.census.gov/data/key_signup.html was 931f0de4f00a8a5d8b5c4dec03dd1e6513c5e641
•	The second dataset was accessed using CMS Marketplace API with the following URL –
https://marketplace.api.healthcare.gov/api/v1/states/{state_code}/medicaid?apikey={CMS_API_KEY}&year={year}
CMS Marketplace API key, obtained on requesting from https://developer.cms.gov/finder-api/key-request.html was HM9ed6rf6NBIZbXeIQY7Wf3FF3DxjMYz


## DATA STRUCTURE
Description of records - Cache is stored as dict where each key on the root level represents a state.
Each State key is a dict consisting of 2 arrays – Census data as one array and CMS data as the second array.

I am organizing the data into a single level flat tree, which is represented using a pandas dataframe.
Here every single column or node is represented by pandas series , which is essentially a list where each node represents an attribute or a column name.
The same structure is used across both datasets.

## INTERACTION AND PRESENTATION
All files must be downloaded in single folder/working directory.
All user interaction will be under the interaction.py file.
Interaction will be via command line prompt and plotly.

User input will be prompted and they will be asked to give a required input via command line prompt, according to which data from “cache.json” will be used to create plots.
The user will first be asked to select a year from 2016-2020, then will be asked to input the USPS code of a state of their choice , choosing from states of MI, TX, NJ, ND.
Once they select a state, they will shown data of number of uninsured vs insured persons (in that state, in that year).
Next, they will be asked if want to to see a state-wide comparison. If they say yes, they will see a plot for number of insured vs uninsured persons, grouped by different states, for that year.
After this, they will be asked of they wish to see data related to race or age? Depending on their answer, they can see plot of percentage of uninsured persons , grouped by (i) race or (ii) age.
The last plot displayed will be a comparison of percentage of insured persons to the percentage of adults below poverty line (as these are persons who qualify for Medicaid), and it should be interesting to see if both these categories overlap or not. 
In each of these plots, the user will be able to hover the cursor over a point in the plot to look at data (values or counts) corresponding to that point , due to incorporation of Plotly package.