# -----------
# User Instructions
# 
# Modify the valid_month() function to verify 
# whether the data a user enters is a valid 
# month. If the passed in parameter 'month' 
# is not a valid month, return None. 
# If 'month' is a valid month, then return 
# the name of the month with the first letter 
# capitalized.
#

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

# build dictionary 
month_abbrs = dict((m[:3].lower(), m) for m in months)
          
def valid_month(month):
  if month:
    cap_month = month.capitalize();

    if cap_month in months:
        return cap_month

def valid_month_short(month):
  if month:
    short_month = month[:3].lower() # get first 3 letters of input
    return month_abbrs.get(short_month) # check if short_month exists in the dictionary
        
        
print valid_month("january") 
print valid_month("jan") 
print valid_month_short("january") 
print valid_month_short("jan") 
print valid_month_short("janasfasfaf") 
print valid_month_short("jjjj") 
