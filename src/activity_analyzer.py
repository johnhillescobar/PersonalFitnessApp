import pandas as pd
import numpy as np
import psycopg2
import myfitnesspal
from myfitnesspal.client import Client

"""
Author: John Hill Escobar

In case a suggestion please, contact me through:

    1. JohnDataAnalytics@gmail.com
    2. Via LinkedIn: https://www.linkedin.com/in/johnhillescobar/

"""

class ActivityTracker:
    """
    

    The functions you will find there are these:

        1. get_total_nutrition_per_date() -> Provides a dataframe with total nutrition values and goals on the 
           dates specified by end user
        2. get_total_nutrition_per_meal() -> Provides a dataframe with total nutrition values per daily meals based 
           on the date range provided by end user. No goals per meal are defined here.
        3. get_total_nutrition_per_entry() -> Provides a dataframe with total nutrition values per daily entry meal 
           based on the date range provided by end user. No goals per entry meal are defined here.
    
    """

    def __init__(self) -> None:

        self.client = Client()

    def get_total_nutrition_per_date(self, initial_date, end_date = None):
        """
        This function provides a dataframe with total nutrition values and goals on the dates specified by end user.

        Inputs:

            initial_date: string argument 'YYYY-MM-DD'.  Corresponds to the first day of your data pull.
            end_date: string argument 'YYYY-MM-DD' [Optional].  Corresponds to the last day of your data pull.

            Caveat: end_date will be matched with initial_date when NO end_date is provided.
        
        Outputs:

            A dataframe with both actual and goal macros will be generated.  A NoneType object is generated when 
            no data is available in MyFitnessPal
        """

        self.initial_date = initial_date
        self.end_date = end_date

        if self.end_date is None:
            self.end_date = self.initial_date

        self.total_days_data = pd.DataFrame()
        self.total_goals_data = pd.DataFrame()

        self.range_days = pd.date_range(start=self.initial_date, end= self.end_date)

        for day_ in self.range_days:
    
            print('generating nutrition data for {}'.format(day_))
            nutrition_activity = self.client.get_date(day_.year, day_.month, day_.day)
            
            if len(nutrition_activity.totals) > 0:
                
                self.total_days_data = pd.concat([self.total_days_data, pd.DataFrame.from_dict([{** {"date": day_}, **nutrition_activity.totals}], orient = 'columns')])
                self.total_goals_data = pd.concat([self.total_goals_data, pd.DataFrame.from_dict([{** {"date": day_}, **nutrition_activity.goals}], orient = 'columns')])

            else:

                print('No record found on day {}'.format(day_))
     
            print('\nnutrition load successful')


        self.total_days_data = pd.merge(self.total_days_data, self.total_goals_data, how = 'inner', on = 'date', suffixes = ('', '_goal'))

        return self.total_days_data
    
    def get_total_nutrition_per_meal(self, initial_date, end_date = None):
        """
        This function provides a dataframe with total nutrition values per daily meal based on the date range provided by
        end user. No goals per meal are defined here.

        Inputs:

            initial_date: string argument 'YYYY-MM-DD'.  Corresponds to the first day of your data pull.
            end_date: string argument 'YYYY-MM-DD' [Optional].  Corresponds to the last day of your data pull.

            Caveat: end_date will be matched with initial_date when NO end_date is provided.
        
        Outputs:

            A dataframe with both actual macros PER MEAL will be generated.  A NoneType object is generated when 
            no data is available in MyFitnessPal
        """

        self.initial_date = initial_date
        self.end_date = end_date

        if self.end_date is None:
            self.end_date = self.initial_date

        self.total_meal_data = pd.DataFrame()

        self.range_days = pd.date_range(start=self.initial_date, end= self.end_date)

        for day_ in self.range_days:
    
            print('generating nutrition data for {}'.format(day_))
            nutrition_activity = self.client.get_date(day_.year, day_.month, day_.day)
            
            if len(nutrition_activity.totals) > 0:
                
                for meal in range(len(nutrition_activity.meals)):
                    
                    print('generating nutrition data for {}'.format(meal))
        
                    self.total_meal_data  = pd.concat([self.total_meal_data ,pd.DataFrame.from_dict([{** {"date": day_}, ** {"meal": nutrition_activity.meals[meal].name}, **nutrition_activity.meals[meal].totals}], orient = 'columns')])
       
            else:

                print('No record found on day {}'.format(day_))
     
            print('\nnutrition load successful')

        self.total_meal_data.fillna(0, inplace= True)

        return self.total_meal_data



    def get_total_nutrition_per_entry(self, initial_date, end_date = None):
        """
        This function provides a dataframe with total nutrition values per daily entry meal based on the date range provided by
        end user. No goals per entry meal are defined here.

        Inputs:

            initial_date: string argument 'YYYY-MM-DD'.  Corresponds to the first day of your data pull.
            end_date: string argument 'YYYY-MM-DD' [Optional].  Corresponds to the last day of your data pull.

            Caveat: end_date will be matched with initial_date when NO end_date is provided.
        
        Outputs:

            A dataframe with both actual macros PER MEAL will be generated.  A NoneType object is generated when 
            no data is available in MyFitnessPal
        """

        self.initial_date = initial_date
        self.end_date = end_date

        if self.end_date is None:
            self.end_date = self.initial_date

        self.total_entry_data = pd.DataFrame()

        self.range_days = pd.date_range(start=self.initial_date, end= self.end_date)

        for day_ in self.range_days:
    
            print('generating nutrition data for {}'.format(day_))
            nutrition_activity = self.client.get_date(day_.year, day_.month, day_.day)
            
            if len(nutrition_activity.totals) > 0:
                
               for meal in range(len(nutrition_activity.meals)):
                   
                   print('generating nutrition data for {}'.format(meal))
                   
                   for entry in range(len(nutrition_activity.meals[meal])):
                       
                       self.total_entry_data  = pd.concat([self.total_entry_data,pd.DataFrame.from_dict([{** {"date": day_}, ** {"meal": nutrition_activity.meals[meal].name}, ** {"entry": nutrition_activity.meals[meal].entries[entry].name}, **nutrition_activity.meals[meal].entries[entry].totals}], orient = 'columns')])
       
            else:

                print('No record found on day {}'.format(day_))
     
            print('\nnutrition load successful')

        self.total_entry_data.fillna(0, inplace= True)

        return self.total_entry_data


    def get_water_per_date(self, initial_date, end_date = None):
        """
        This function provides a dataframe with total nutrition values and goals on the dates specified by end user.

        Inputs:

            initial_date: string argument 'YYYY-MM-DD'.  Corresponds to the first day of your data pull.
            end_date: string argument 'YYYY-MM-DD' [Optional].  Corresponds to the last day of your data pull.

            Caveat: end_date will be matched with initial_date when NO end_date is provided.
        
        Outputs:

            A dataframe with both actual and goal macros will be generated.  A NoneType object is generated when 
            no data is available in MyFitnessPal
        """

        
        self.initial_date = initial_date
        self.end_date = end_date

        if self.end_date is None:
            self.end_date = self.initial_date

        self.total_water_data = pd.DataFrame()
      
        self.range_days = pd.date_range(start=self.initial_date, end= self.end_date)

        for day_ in self.range_days:
    
            print('generating nutrition data for {}'.format(day_))
            nutrition_activity = self.client.get_date(day_.year, day_.month, day_.day)
            
            if len(nutrition_activity.totals) > 0:
                
                self.total_water_data = pd.concat([self.total_water_data, pd.DataFrame.from_dict([{"date": day_, 'water_consumption': nutrition_activity.water}], orient = 'columns')])

            else:

                print('No record found on day {}'.format(day_))
     
            print('\nnutrition load successful')

        self.total_water_data.fillna(0, inplace= True)

        return self.total_water_data
        







