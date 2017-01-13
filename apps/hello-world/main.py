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
		<input type="text" name="day">
	</label>
	<label>Month
		<input type="text" name="month">
	</label>
	<label>Year
		<input type="text" name="year">
	</label>
	<div style="color: red">%(error)s</div>
	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):

	def write_form(self, error=""):
		return self.response.out.write(form % {"error": error})

	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.write_form()

	def post(self):
		user_day = handyfunctions.valid_day(self.request.get('day'))
		user_month = handyfunctions.valid_month_short(self.request.get('month'))
		user_year = handyfunctions.valid_year(self.request.get('year'))

		if not (user_day and user_month and user_year):
			self.write_form("that's not a valid day is it???")
		else:
			return self.response.out.write("Perfect day to be born")


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

