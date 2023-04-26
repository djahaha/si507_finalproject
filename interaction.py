import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Read the data from the cache file, covert to a dictionary using pandas
df = pd.read_json('cache.json')
all_df = {}
all_cms_df = {}

for state in df.columns:
    columns = []
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    a7 = []
    a8 = []
    a9 = []
    a10 = []

    all_cms_df[state] = pd.DataFrame(df[state]['cms_array'])


    for idx, row in enumerate(df[state]['census_data']):
        if idx==0:
            columns = [item for item in row]
        else:
            for item in row:
                a1.append(item[0])
                a2.append(item[1])
                a3.append(item[2])
                a4.append(item[3])
                a5.append(item[4])
                a6.append(item[5])
                a7.append(item[6])
                a8.append(item[7])
                a9.append(item[8])
                a10.append(item[9])
    temp_df = pd.DataFrame({'a1':a1, 'a2':a2, 'a3':a3, 'a4':a4, 'a5':a5, 'a6':a6, 'a7':a7, 'a8':a8, 'a9':a9, 'a10':a10})
    temp_df.columns = columns
    all_df[state] = temp_df

#converting variables to correct names
for state in df.columns:
    agecat = {"0":"Under 65","1":"18-64","2":"40-64","3":"50-64","4":"Under 19","5":"21-64"}
    all_df[state]['AGECAT'] = all_df[state]['AGECAT'].map(agecat)

    racecat = {"0":"All races","1":"White","2":"Black","3":"Hispanic"}
    all_df[state]['RACECAT'] = all_df[state]['RACECAT'].map(racecat)

    iprcat = {"0":"All income levels","1":"At or below 200 pct of poverty","2":"At or below 250 pct of poverty","3":"At or below 138 pct of poverty", "4":"At or below 400 pct of poverty","5":"Between 138 and 400 pct of poverty"}
    all_df[state]['IPRCAT'] = all_df[state]['IPRCAT'].map(iprcat)


print('Please select one of the following states: MI, TX, NJ, ND')

state_codes = ['MI','TX','NJ','ND']

while True:
    state = input('Please enter a state code: ').upper()
    if state in state_codes:
        print('You have selected the state: ' + state)
        break
    else:
        print('Please enter a valid state code from the states listed below')
        print('Please select one of the following states: MI, TX, NJ, ND')


print('Please select a year in : 2016, 2017, 2018, 2019, 2020 for the state you selected')

years_codes = ['2016','2017','2018','2019','2020']

while True:
    year = input('Please enter a year from 2016-2020: ')
    if year in years_codes:
        print('You have selected the year: ' + year + ' for the state: ' + state + ' , and we will show you comparison between number of uninsured patients and patient age in this year')
        break
    else:
        print('Please enter a valid year from the years listed below')
        print('Please select one of the following years: 2016, 2017, 2018, 2019, 2020')


# for the selected state and year, plot the following:
# 1. Age vs. NUI_PT

temp = all_df[state][all_df[state]['time']==year][['AGECAT','NUI_PT']]
temp['NUI_PT'] = temp['NUI_PT'].astype(float)

fig = px.bar(data_frame=temp.groupby('AGECAT').median().reset_index(),
                x='AGECAT',
                y='NUI_PT',
                color='AGECAT',
                title='Age vs. Number of Uninsured Patients for the state ' + state + ' for the year ' + year)
fig.update_layout(showlegend=False)

fig.update_xaxes(title_text='Age group')
fig.update_yaxes(title_text='Number of Uninsured Patients')

fig.show()

# Also, asking the user if they want to see the comparison of the same plot for the other states
# If yes, then plot the same plot for the other states in the same figure

while True:
    user_input = input('Do you want to see the comparison of the Age vs. Number of Uninsured Patients plot for the other states? (y/n): ').lower()
    if user_input == 'y':
        print('You have selected to see the comparison of the Age vs. Number of Uninsured Patients plot for the other states')
        break
    elif user_input == 'n':
        print('You have selected not to see the comparison of the Age vs. Number of Uninsured Patients plot for the other states')
        break
    else:
        print('Please enter a valid input (y/n)')

# if user_input == 'y':
#     for key in all_df.keys():
#         if key != state:
#             temp = all_df[key][all_df[key]['time']==year][['AGECAT','NUI_PT']]
#             temp['NUI_PT'] = temp['NUI_PT'].astype(float)

#             fig = px.bar(data_frame=temp.groupby('AGECAT').median().reset_index(),
#                             x='AGECAT',
#                             y='NUI_PT',
#                             color='AGECAT',
#                             title='Age vs. NUI_PT for the state: ' + key + ' for the year: ' + year)
#             fig.update_layout(showlegend=False)
#             fig.show()

import plotly.graph_objs as go

if user_input == 'y':
    states = list(all_df.keys())
    states.remove(state)

    # create a list of bar traces for each state
    bar_traces = []
    for st in states:
        temp = all_df[st][all_df[st]['time']==year][['AGECAT','NUI_PT']]
        temp['NUI_PT'] = temp['NUI_PT'].astype(float)
        medians = temp.groupby('AGECAT').median().reset_index()
        bar_trace = go.Bar(x=medians['AGECAT'], y=medians['NUI_PT'], name=st)
        bar_traces.append(bar_trace)

    # add the chosen state's data as a separate bar trace
    chosen_temp = all_df[state][all_df[state]['time']==year][['AGECAT','NUI_PT']]
    chosen_temp['NUI_PT'] = chosen_temp['NUI_PT'].astype(float)
    chosen_medians = chosen_temp.groupby('AGECAT').median().reset_index()
    chosen_bar_trace = go.Bar(x=chosen_medians['AGECAT'], y=chosen_medians['NUI_PT'], name=state)
    bar_traces.append(chosen_bar_trace)

    # create the grouped bar chart
    fig = go.Figure(data=bar_traces)
    fig.update_layout(barmode='group', title='Comparison of Age vs. Number of Uninsured Patients for States in ' + year)
    fig.update_xaxes(title_text="Age Category")
    fig.update_yaxes(title_text="Number of Uninsured Patients")
    fig.show()







# ----------------------------------------------------------------------------------------------------------------------------
# 2.  NIC_PT vs. RACECAT

# Asking the user if they want to see NIC_PT vs. RACECAT for the selected state over the years

while True:
    user_input = input('Do you want to see Number of Insured Patients by Race for the selected state over the years? (y/n): ').lower()
    if user_input == 'y':
        print('You have selected to see Number of Insured Patients by Race for the selected state over the years')
        break
    elif user_input == 'n':
        print('You have selected not to see Number of Insured Patients by Race for the selected state over the years')
        break
    else:
        print('Please enter a valid input (y/n)')

if user_input == 'y':
    temp = all_df[state][['time','RACECAT','NIC_PT']]
    temp['NIC_PT'] = temp['NIC_PT'].astype(float)

    fig = px.line(data_frame=temp.groupby(['time','RACECAT']).median().reset_index(),
                    x='time',
                    y='NIC_PT',
                    color='RACECAT',
                    title='Number of Insured Patients by Race for the state ' + state + ' over the years')
    fig.update_layout(showlegend=True)
    fig.update_xaxes(title_text='Race Category')
    fig.update_yaxes(title_text='Number of Insured Patients')
    fig.show()

# Asking the user if they want to see the comparison of NIC_PT vs. RACECAT for the selected state over the years with the other states

while True:
    user_input = input('Do you want to see the comparison of Number of Insured Patients by Race versus other states over the years ? (y/n): ').lower()
    if user_input == 'y':
        print('You have selected to see the comparison of Number of Insured Patients by Race versus other states over the years')
        break
    elif user_input == 'n':
        print('You have selected not to see the comparison of Number of Insured Patients by Race versus other states over the years')
        break
    else:
        print('Please enter a valid input (y/n)')

if user_input == 'y':
    states = list(all_df.keys())
    states.remove(state)
    for key in states:
        temp = all_df[key][['time','RACECAT','NIC_PT']]
        temp['NIC_PT'] = temp['NIC_PT'].astype(float)

        fig = px.line(data_frame=temp.groupby(['time','RACECAT']).median().reset_index(),
                        x='time',
                        y='NIC_PT',
                        color='RACECAT',
                        title='Number of Insured Patients by Race ' + key + ' over the years')
        fig.update_layout(showlegend=True)
        fig.update_xaxes(title_text='Race Category')
        fig.update_yaxes(title_text='Number of Insured Patients')
        fig.show()

# ----------------------------------------------------------------------------------------------------------------------------

# 4

# from all_cms_df (all_cms_df is a dict with df for each state): ASKING the user if they want to see how pc_fpl values as a pie chart for the selected state for the selected year

while True:
    user_input = input('Do you want to see what the split of population at or below federal poverty line looks like? (y/n): ').lower()
    if user_input == 'y':
        print('You have selected to see what the split of population at or below federal poverty line looks like')
        break
    elif user_input == 'n':
        print('You have selected not to see what the split of population at or below federal poverty line looks like')
        break
    else:
        print('Please enter a valid input (y/n)')

if user_input == 'y':
    temp = all_cms_df[state][['pc_fpl_pregnant','pc_fpl_parent', 'pc_fpl_child_1_5', 'pc_fpl_child_6_18','pc_fpl_adult', 'pc_fpl_child_newborn']]
    temp['pc_fpl_pregnant'] = temp['pc_fpl_pregnant'].astype(float)
    temp['pc_fpl_parent'] = temp['pc_fpl_parent'].astype(float)
    temp['pc_fpl_child_1_5'] = temp['pc_fpl_child_1_5'].astype(float)
    temp['pc_fpl_child_6_18'] = temp['pc_fpl_child_6_18'].astype(float)
    temp['pc_fpl_adult'] = temp['pc_fpl_adult'].astype(float)
    temp['pc_fpl_child_newborn'] = temp['pc_fpl_child_newborn'].astype(float)

     # Aggregate data to get total population at or below FPL for each group
    totals = temp.sum()

    # Create a pie chart
    fig, ax = plt.subplots()
    explode = (0, 0, 0, 0, 0, 0.1) # Explode the "Newborn" slice
    ax.pie(totals, labels=['Pregnant', 'Parent', 'Child 1-5', 'Child 6-18', 'Adult', 'Newborn'], autopct='%1.1f%%', explode=explode)
    ax.set_title('Population at or below federal poverty line by group')

    # Display the pie chart
    plt.show()

#asking user if they want to see comparison of pc_fpl values for states apart from the state they chose
while True:
    user_input = input('Do you want to see what the split of population at or below federal poverty line looks like for states other than your selected state? (y/n): ').lower()
    if user_input == 'y':
        print('You have selected to see what the split of population at or below federal poverty line looks like for states other than your selected state.')
        break
    elif user_input == 'n':
        print('You have selected not to see what the split of population at or below federal poverty line looks like for states other than your selected state.')
        break
    else:
        print('Please enter a valid input (y/n)')

if user_input == 'y':
    selected_state = 'YOUR_STATE'
    other_states = [state for state in all_cms_df.keys() if state != selected_state]

    for state in other_states:
        temp = all_cms_df[state][['pc_fpl_pregnant','pc_fpl_parent', 'pc_fpl_child_1_5', 'pc_fpl_child_6_18','pc_fpl_adult', 'pc_fpl_child_newborn']]
        temp['pc_fpl_pregnant'] = temp['pc_fpl_pregnant'].astype(float)
        temp['pc_fpl_parent'] = temp['pc_fpl_parent'].astype(float)
        temp['pc_fpl_child_1_5'] = temp['pc_fpl_child_1_5'].astype(float)
        temp['pc_fpl_child_6_18'] = temp['pc_fpl_child_6_18'].astype(float)
        temp['pc_fpl_adult'] = temp['pc_fpl_adult'].astype(float)
        temp['pc_fpl_child_newborn'] = temp['pc_fpl_child_newborn'].astype(float)

        # Aggregate data to get total population at or below FPL for each group
        totals = temp.sum()

        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie(totals, labels=['Pregnant', 'Parent', 'Child 1-5', 'Child 6-18', 'Adult', 'Newborn'], autopct='%1.1f%%')
        ax.set_title(f'Population at or below federal poverty line by group in {state}')

        # Display the pie chart
        plt.show()






# ----------------------------------------------------------------------------------------------------------------------------

