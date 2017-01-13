import cgi

def valid_day(day):
  if day and day.isdigit():
    day = int(day)
    if day > 0 and day <= 31:
      return day

# months list
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

def valid_year(year):
  if year and year.isdigit():
    year = int(year)
    if year > 1900 and year < 2017:
      return year

def escape_html(s):
  return cgi.escape(s, quote=True)