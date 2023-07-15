import csv
import sys
import json

file = sys.argv[1]

cancellation_cols = {
    'First name': None,
    'Last name': None,
    'E-Mail Address': None,
    'Phone Number': None,
    'Group name': None,
    'Membership level name': None,
    'Membership status': None,
    'Created date': None,
    'Cancelled at': None,
    'Cancellation Request format & date': None,
    'Length of membership': None,
    'Cancellation reason': None,
    'Shipping State/Province': None,
}

on_hold_cols = {
    'First name': None,
    'Last name': None,
    'E-Mail Address': None,
    'Phone Number': None,
    'Group name': None,
    'Membership level name': None,
    'Membership status': None,
    'Created date': None,
    'On hold format & date': None,
    'On Hold Reason': None,
    'Status Changed At Date': None,
    'Hold ends at': None,
    'Shipping State/Province': None,
}

with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    cols = next(reader)
    for i, item in enumerate(cols):
        if (item in cancellation_cols):
            cancellation_cols[item] = i
        if (item in on_hold_cols):
            on_hold_cols[item] = i
    for row in reader:
        if (row[on_hold_cols['Membership status']] == 'On Hold'):
            hold_time = str(on_hold_cols["Hold ends at"])
            print(type(hold_time))
            print(f'on hold until {row[on_hold_cols["Hold ends at"]]}')
        if (row[cancellation_cols['Membership status']] == 'Cancelled'):
            cancelled_date = cancellation_cols["Cancelled at"]
            print(f'cancelled on {row[cancellation_cols["Cancelled at"]]}')
        else:
            pass
