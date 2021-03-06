# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import handyfunctions

form = """
<form action="/" method="post">
	What is your birth date?
	<br>
	<label>Day
		<input type="text" name="day" value="%(day)s">
	</label>
	<label>Month
		<input type="text" name="month" value="%(month)s">
	</label>
	<label>Year
		<input type="text" name="year" value="%(year)s">
	</label>
	<div style="color: red">%(error)s</div>
	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):

	def write_form(self, error="", day="", month="", year=""):
		return self.response.out.write(form % {"error": error, "day": day, "month": month, "year": year})

	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.write_form()

	def post(self):
		user_day = self.request.get('day')
		user_month = self.request.get('month')
		user_year = self.request.get('year')

		user_day = handyfunctions.escape_html(user_day)
		user_month = handyfunctions.escape_html(user_month)
		user_year = handyfunctions.escape_html(user_year)

		day = handyfunctions.valid_day(user_day)
		month = handyfunctions.valid_month_short(user_month)
		year = handyfunctions.valid_year(user_year)

		if not (day and month and year):
			self.write_form("that's not a valid day is it???", user_day, user_month, user_year)
		else:
			self.redirect("/thanks")


class ThanksHandler(webapp2.RequestHandler):

	def get(self):
		return self.response.out.write("Perfect day to be born")



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)
], debug=True)

