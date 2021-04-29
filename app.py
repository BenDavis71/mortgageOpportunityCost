import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st




st.title('Mortgage Opportunity Cost Calculator')
#st.markdown("_Let's get educated brother_")
st.markdown("_Historical simulations to optimize investment decisions surrounding housing_")


#cache this function so that streamlit doesn't rerun it everytime a user input is changed
@st.cache(allow_output_mutation=True)
def getData():

    url = 'https://raw.githubusercontent.com/BenDavis71/mortgageOpportunityCost/master/shillerData.csv'
    df = pd.read_csv('url')

    return df 

dfData = getData()


#initialize lists
downPayment = []
mortgageCost = []
mortgageYears = [] 

lumpSum = []
investmentsDuring = []
investmentsAfter = [] 

#user inputs for option 1
st.markdown("__Option 1:__")
col1, col2, col3 = st.beta_columns(3)

#user input for down payment
downPayment.append(col1.number_input("Down Payment", min_value = 0, value = 60000, key = 1))

#user input for cost of mortgage
mortgageCost.append(col2.number_input("Monthly Mortgage Payment", min_value = 0, value = 1034, key = 2))

#user input for length of mortgage
mortgageYears.append(col3.number_input("Years of Mortgage", min_value = 0, value = 30, key = 3))


#user inputs for option 2
st.markdown("__Option 2:__")

col4, col5, col6 = st.beta_columns(3)
#user input for down payment
downPayment.append(col4.number_input("Down Payment", min_value = 0, value = 10500, key = 4))

#user input for cost of mortgage
mortgageCost.append(col5.number_input("Monthly Mortgage Payment", min_value = 0, value = 1496, key = 5))

#user input for length of mortgage
mortgageYears.append(col6.number_input("Years of Mortgage", min_value = 0, value = 30, key = 6))

st.markdown("____")

#calculate opportunity costs
lumpSum = [max(downPayment)-x for x in downPayment]
investmentsDuring = [max(mortgageCost)-x for x in mortgageCost]
investmentsAfter = mortgageCost






#find length of period we're projecting
lengthOfPeriod = max(mortgageYears)

#create a dataframe holding all the start years to iterate through
dfYears = dfData[dfData['date'].astype(str).str[-2:] == '01']
dfYears = dfYears[dfYears['date'] < dfYears['date'].max() + 1 - lengthOfPeriod]



#calculate 
dfProjections = pd.DataFrame()

for startDate in dfYears['date']:
    endDate = startDate + lengthOfPeriod

    df = dfData[dfData['date'].between(startDate,endDate)].reset_index(drop=True)
    df['newInvestments0'] = np.where(df['date'] <= mortgageYears[0] + startDate,investmentsDuring[0],investmentsAfter[0])
    df['newInvestments0'][0] += lumpSum[0]
    df['earnings0'] = df['newInvestments0'] * (df.iloc[-1,1] / df['realReturn'])
    investmentTotal0 = df['earnings0'].sum()

    df['newInvestments1'] = np.where(df['date'] <= mortgageYears[1] + startDate,investmentsDuring[1],investmentsAfter[1])
    df['newInvestments1'][0] += lumpSum[1]
    df['earnings1'] = df['newInvestments1'] * (df.iloc[-1,1] / df['realReturn'])
    investmentTotal1 = df['earnings1'].sum()

    dfProjections = dfProjections.append(pd.DataFrame([[str(startDate)[:4],investmentTotal0,investmentTotal1]],columns=['year','option1','option2']),ignore_index=True)


#present
dfProjections['difference'] = dfProjections['option1'] - dfProjections['option2']

dfProjections['legend'] = np.where(dfProjections['difference'] > 0,'Option 1 wins','Option 2 wins') 


st.write(px.histogram(dfProjections,x='difference',color='legend',template='simple_white', color_discrete_map={'Option 1 wins':'#4056A1', 'Option 2 wins':'#F13C20'}))

dfProjectionsViolin = pd.melt(dfProjections,id_vars = ['year'],value_vars=['option1','option2'])
dfProjectionsViolin.columns = ['Year','legend','value']
dfProjectionsViolin['legend'] = np.where(dfProjectionsViolin['legend'] == 'option1','Option 1','Option 2') 
st.write(px.violin(dfProjectionsViolin, y = 'value',color = 'legend',box=True, points="all",template='simple_white', color_discrete_map={'Option 1':'#4056A1', 'Option 2':'#F13C20'}))

dfProjections.columns = ['Start Year','Option 1 Total','Option 2 Total','Difference','Result']
dfProjections



st.markdown('___')
st.markdown('Created by [Ben Davis](https://github.com/BenDavis71/)')
st.markdown('Data from [Robert Shiller](http://www.econ.yale.edu/~shiller/data.htm)')