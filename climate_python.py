
#import matplotlib
#style.use('fivethirtyeight')
#import matplotlib.pyplot as plt
#from dateutil.relativedelta import *
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, redirect, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)


measurement.__dict__

# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 




# Calculate the date one year from the last date in data set.
#twelvemonthsago = dt.datetime(2017, 8, 23) - relativedelta(months=+12)
#print(twelvemonthsago)

# Perform a query to retrieve the data and precipitation scores

annual_prcp = session.query(measurement.date, measurement.prcp).\
                  filter(measurement.date >= dt.datetime(2016, 8, 23, 0)).all()
dates = []
prcp = []
for row in annual_prcp:
    dates.append(row[0])
    prcp.append(row[1])



prcp_dic = {'Date' : dates, 'Percipitation' : prcp}
# Save the query results as a Pandas DataFrame and set the index to the date column
prcp_df = pd.DataFrame(prcp_dic)

prcp_df.head()



# Sort the dataframe by date

sorted_prcp_df = prcp_df.sort_values(by='Date')
#sorted_prcp_df.plot(kind='line', x='Date', y='Percipitation', grid = True, ylabel = "Inches", rot = 90, title = "Last Twelve Months: Percipitation in Hawaii")


# Use Pandas Plotting with Matplotlib to plot the data

#plt.plot(sorted_prcp_df.iloc[:,0], sorted_prcp_df.iloc[:,1], label = "Percipitation")
#plt.legend(loc='best')

#plt.title('Percipitation in Hawaii for Last Twelve Months')
#plt.xlabel('Inches')
#plt.xticks(np.arange())
#plt.ylabel('Date')

#plt.show()



total_stations = session.query(measurement, station).\
    filter(measurement.station == station.station).\
    group_by(station.id).count()
#print(total_stations)

station_names = session.query(station.name).\
    filter(measurement.station == station.station).\
    group_by(station.id).all()


test = session.query(station.name, func.count(measurement.station)).\
    filter(measurement.station == station.station).\
    group_by(station.name).\
    order_by(func.count(station.id).desc()).all()
# List the stations and the counts in descending order.
#for row in test:
 #   print(row)



highest_temp = session.query(func.max(measurement.tobs)).\
    filter(measurement.station == station.station).\
    filter(station.name == 'WAIHEE 837.5, HI US').all()
##print(highest_temp)

average_temp = session.query(func.avg(measurement.tobs)).\
    filter(measurement.station == station.station).\
    filter(station.name == 'WAIHEE 837.5, HI US').all()
#print(average_temp)


temp_twelve_month = session.query(measurement.tobs).\
    filter(measurement.station == station.station).\
    filter(measurement.date >= dt.datetime(2016, 8, 23, 0)).\
    filter(station.name == 'WAIHEE 837.5, HI US').all()

#temp_twelve_month

#temp_df = pd.DataFrame(temp_twelve_month)
#temp_df = temp_df.rename(columns={0:'Temperature'})
#temp_df.head()

#temp_df['Frequency'] = temp_df.groupby(['Temperature'])['Temperature'].transform('count')
#temp_df.head()
#index = pd.Index(range(0, 25))

#hist_data = temp_df.value_counts()
#hist_data


#def column(matrix, i):
    #return [row[i] for row in matrix]

#frequencies = column(hist_data, 1)

sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

def start_tobs_measures(startdate):
    data = session.query(*sel).\
    filter(measurement.date >= str(startdate)).all()
    return data
    

def end_tobs_measures(start, end):
    start=dt.datetime.strptime(start, '%Y-%m-%d')
    end=dt.datetime.strptime(end, '%Y-%m-%d')
    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    return results

print(start_tobs_measures('2016-8-3'))

print(end_tobs_measures('2016-8-3', '2017-9-3'))

#len(temp_df.value_counts())


#hist_temp_df = pd.DataFrame(hist_data)

#hist_temp_df.head()



bins = 12
#plt.hist(temp_df['Temperature'], bins, density= 1)
#plt.xlabel('Temperature')
#plt.ylabel('Frequency')
session.close()