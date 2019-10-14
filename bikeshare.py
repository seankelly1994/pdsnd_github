import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': './data/chicago.csv',
              'new york': './data/new_york_city.csv',
              'washington': './data/washington.csv' }

city_list = ['washington', 'new york', 'chicago']
month_list = ['january', 'february', 'march', 'april', 'may', 'june']
day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    #Change number 2 for section 3
    print('Hello! Let\'s explore some US bikeshare data!')
    print("Your choices are Washington, New York or Chicago")

    city = input("Enter the name of the city you would like to explore: ")
    city = city.lower()
    
    print("Great your chosen city is: " + city)

    while (city not in city_list or city == ''):
        city = input("Incorrect entry, please enter the name of one of the three selected cities: ")


    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Enter the month you would like to investigate: ")
    month = month.lower()

    while(month not in month_list or month == ''):
        month = input("Incorrect Entry, please enter the correct month with capital letters: ")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter the day would like to investigate: ")
    day = day.lower()
    while(day not in day_list or day == ''):
        day = input("Incorrect Entry, please enter correct day with capital letters: ")
        

    #Convert inputs to lower case for the dictionary
    city = city.lower()
    month = month.lower()
    day = day.lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = month_list
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print("The Most popular month is " + str(month_list[popular_month - 1]))


    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day of the week is " + str(popular_day))


    # Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The Most popular hour is " + str(popular_hour) + ":00 h")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_station_start = df['Start Station'].mode()[0]
    print("The most popular start station is " + str(popular_station_start))

    # Display most commonly used end station
    popular_station_end = df['End Station'].mode()[0]
    print("The most popular end station is " + str(popular_station_end))

    # Display most frequent combination of start station and end station trip
    overall_station = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    print("The most popular combination is " + str(overall_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_days = total_travel_time//86400
    total_travel_time_hours = (total_travel_time % 86400) //3600
    total_travel_time_minutes = ((total_travel_time % 86400) % 3600) //60
    total_travel_time_seconds = (((total_travel_time % 86400) % 3600) % 60)//60

    print("Total travel time is " + str(total_travel_time_days) + " days " + str(total_travel_time_hours) + " hours " + str(total_travel_time_minutes) + " minutes and " + str(total_travel_time_seconds) + " seconds")


    # Display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types distribution below")
    print(str(user_types))

    # Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts()
        print("Gender distribution below")
        print(str(gender_distribution))
    except:
        print("No gender data availble for Washington")

    # Display earliest, most recent, and most common year of 
    try:
        earlist_birth = str(df['Birth Year'].min())
        earlist_birth = earlist_birth.split('.')
        recent_birth = str(df['Birth Year'].max())
        recent_birth = recent_birth.split('.')
        common_year_birth = str(df['Birth Year'].mode()[0])
        common_year_birth = common_year_birth.split('.')

        print("Earlist birth Year is " + earlist_birth[0] + " the most recent birth year is " + recent_birth[0] + " and the most common birth year is " + common_year_birth[0])

    except:
        print("No availible birth data for this data set")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def sample_date(df):
    count = int(input("How many rows would you like to see? "))
    for d in range(count):
        print(df.iloc[d])
    
    return 'Done'


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Ask the user if they would like to see some sample data
        answer = input("Would you like to see some sample data? ")
        answer = answer.lower()

        if(answer == 'yes'):
            sample_date(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
