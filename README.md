# Phone_pulse_data_visualization_and_exploration

# Hi everyone!

# Introduction:
  The Indian digital payments story has truly captured the world’s imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-art payments infrastructure built as Public Goods championed by the central bank and the government. PhonePe started in 2016 and has been a strong beneficiary of the API driven digitisation of payments in India. When we started , we were constantly looking for definitive data sources on digital payments in India without much success. As a way of giving back to the data and developer community, we decided to open the anonymised aggregate data sets that demystify the what, why and how of digital payments in India. Licensed under the CDLA-Permissive-2.0 open data license, the PhonePe Pulse Dataset API is a first of its kind open data initiative in the payments space.
  
# Project approach:
1. Data extraction: 
  Clone the Github using scripting to fetch the data from the
Phonepe pulse Github repository and store it in a suitable format such as CSV
or JSON.
2. Data transformation: 
  Use a scripting language such as Python, along with
libraries such as Pandas, to manipulate and pre-process the data. This may
include cleaning the data, handling missing values, and transforming the data
into a format suitable for analysis and visualization.
3. Database insertion: 
  Use the "mysql-connector-python" library in Python to
connect to a MySQL database and insert the transformed data using SQL
commands.
4. Dashboard creation: 
  Use the Streamlit and Plotly libraries in Python to create
an interactive and visually appealing dashboard. Plotly's built-in geo map
functions can be used to display the data on a map and Streamlit can be used
to create a user-friendly interface with multiple dropdown options for users to
select different facts and figures to display.
5. Data retrieval: 
  Use the "mysql-connector-python" library to connect to the
MySQL database and fetch the data into a Pandas dataframe. Use the data in
the dataframe to update the dashboard dynamically.
6. Deployment: 
  Ensure the solution is secure, efficient, and user-friendly. Test
the solution thoroughly and deploy the dashboard publicly, making it
accessible to users

Link for the dataset:
  https://github.com/PhonePe/pulse#readme

# How to install:

Step 1(Getting the Repo): 
  Clone this git repository to your PC.
 
Step 2(Preparing the program to load data):
  Use requirements.txt to install all the modules needed for the program.
  
Step 3(Building the Database with sql):
  Run pulse_sql.ipynb on your pc with jupyter notebook.
  
  Note!:
    The Database should be created before running pulse_sql.ipynb on your PC 
 and were only going to create tables and insert values to it.
  
Step4 (Final touch):
    Run Main.py on your streamlit environment by the below command.
  # streamlit run main.py 
  
  Note!:
    You should switch to the file directory having main.py
    eg:
      cd path/
      goto step4
      
 # Thank you have a nice day!
   
  
