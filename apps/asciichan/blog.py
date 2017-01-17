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

import os
import jinja2
import webapp2

# build path to templates directory
template_dir = os.path.join(os.path.dirname(__file__),"templates")
# initialize jinja environment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write( *a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

class MainPage(BaseHandler):
    def render_front(self, title="", art="", error=""):
        self.render("front.html", title=title, art=art, error=error)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            self.write('thanks!')
        else:
            error = "We need both title and art"
            self.render_front(title, art, error) # we don't have to do title=title etc everytime
		

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

