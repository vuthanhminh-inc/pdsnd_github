import time
import datetime
import calendar
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter the citie you want to analyze - (1) for Chicago, (2) for New York or (3) for Washington: ")
        try:
            city = int(city)

            if city not in [1, 2, 3]:
                print('Please enter the valid number!.')
                continue

            city = list(CITY_DATA)[city-1]
            break
        except:
            print('Please enter number!.')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter month (from January to June) in number to be analyzed, type (0) to filter all months: ")
        try:
            month = int(month)

            if month == 0:
                month = 'all'
                break

            elif month not in [1, 2, 3, 4, 5, 6]:
                print('Please enter the valid number!.')
                continue

            month = calendar.month_name[month]
            break
        except:
            print('Please enter number!.')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter day (from Monday(2) to Sunday(8)) in number to be analyzed, type (0) to filter all days: ")
        try:
            day = int(day)
        
            if day == 0:
                day = 'all'
                break

            elif day not in list(range(2,9)):
                print('Please enter the valid number!.')
                continue

            day = calendar.day_name[day-2]
            break
        except:
            print('Please enter number!.')
            continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data of choosen city from file
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Filter by month
    if month != 'all':
        df = df[df['Start Time'].dt.month_name() == month]

    # Filter by day of week
    if day != 'all':
        df = df[df['Start Time'].dt.day_name() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Start Time'].dt.month_name().mode()[0]
    print ('The most popular month is: {}'.format(popular_month))

    # display the most common day of week
    popular_day = df['Start Time'].dt.day_name().mode()[0]
    print ('The most popular hour of day is: {}'.format(popular_day))

    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most popular day of week is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print ('The most popular used start station is: {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print ('The most popular used end station is: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_start_and_end_station = df[['Start Station', 'End Station']].value_counts().nlargest().index[0]
    print ('The most frequent trip start from the "{}" station to the "{}" station'.format(popular_start_and_end_station[0], popular_start_and_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print ('The total of travel time: {} minutes'.format(total_trip_duration))

    # display mean travel time
    avg_trip_duration = df['Trip Duration'].mean()
    print ('The average of travel time: {} minutes'.format(int(avg_trip_duration)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    if city == 'washington':
        print("Washington has no data for user's gender and year of birth!")
        return

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    unique_user_types = list(df['User Type'].value_counts(dropna=True))
    number_of_user_type = len(unique_user_types)
    print ('The number of user types: {}'.format(int(number_of_user_type)))

    # Display counts of gender
    unique_genders = list(df['Gender'].value_counts(dropna=True))
    number_of_gender = len(unique_genders)
    print ('The number of user types: {}'.format(int(number_of_gender)))

    # Display earliest, most recent, and most common year of birth
    earliest_year_of_birth = int(df['Birth Year'].min())
    print ('The oldest year of birth: {}'.format(earliest_year_of_birth))
    
    most_recent_year_of_birth = int(df['Birth Year'].max())
    print ('The youngest year of birth: {}'.format(most_recent_year_of_birth))
    
    common_year_of_birth = int(df['Birth Year'].mode()[0])
    print ('The common year of birth: {}'.format(common_year_of_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    # Ask user if they want to see individual trip data.
    start_index, end_index = 0, 5
    data_length = len(df.index)

    user_continue = input("\nWould you like to see the first 5 rows of data?\nEnter 'yes' or 'no': ").lower()
    
    while user_continue == 'yes':
        if end_index > data_length:
            end_index = data_length

        print(df.iloc[start_index:end_index])

        if end_index == data_length:
            print('There are the last data!')
            break

        user_continue = input("\nWould you like to see the next 5 rows of data?\nEnter 'yes' or 'no': ").lower()
        if user_continue != 'yes':
            break
        else:
            start_index += 5
            end_index += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
