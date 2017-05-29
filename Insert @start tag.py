# Insert @start tag
# A workflow for the iOS text editor Editorial
# Copyright (c) 2017 Duncan MacIntyre
# Licensed under the MIT License, see LICENSE.txt

# This workflow, when run, prompts the user to select a date. @start(YYYY-MM-DD) is then inserted
# at the cursor, where YYYY-MM-DD is the selected date.

import datetime
import dialogs
import workflow
import editor

# generate a list of DateObjects for the next seven days after today
dates = [datetime.date.today() + datetime.timedelta(days=(i + 1)) for i in range(7)]

# generate a list of readable dates in the form '   Weekday, Month Day', each corresponding to
# one date in dates
readable_dates = [i.strftime('   %A, %B %d') for i in dates]

# prompt the user to choose one of readable_dates or '   Other', store choice in chosen
chosen = dialogs.list_dialog(title = 'Choose a start date:', items = readable_dates + ['   Other'])

# if one of readable_dates was chosen...
if chosen in readable_dates:
	# change chosen to the DateObject in dates at the same index as chosen is in readable_dates
	chosen = dates[readable_dates.index(chosen)]
# otherwise, if '   Other' was chosen...
elif chosen == '   Other':
	# prompt the user to choose a date, store their choice as a DateObject in chosen
	chosen = dialogs.date_dialog()

# if chosen is not None...
# (this would happen if the user closed one of the above dialogs without choosing anything)
if chosen is not None:
	# insert @start(YYYY-MM-DD) at the cursor, where YYYY-MM-DD is the chosen date in this format
	editor.insert_text('@start(' + chosen.isoformat() + ')')
