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
import hashlib
import hmac
import random
import string

from google.appengine.ext import db

# build path to templates directory
template_dir = os.path.join(os.path.dirname(__file__),"templates")
# initialize jinja environment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# define a secret key
SECRET = 'iamsosecret'


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write( *a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def hash_str(self, cookie_string):
        cookie_string = str(cookie_string)
        # return hashlib.md5(cookie_string).hexdigest()
        return hmac.new(SECRET, cookie_string).hexdigest()

    def make_salt(self):
        emptysting = ''
        return emptysting.join(random.choice(string.letters) for x in xrange(5)) 

    def make_secure_cookie(self, cookie_string):
        return "%s|%s" % (cookie_string, self.hash_str(cookie_string))

    def check_secure_cookie(self, cookie_string):
        cookie_string_val = cookie_string.split("|")[0]
        if cookie_string == self.make_secure_cookie(cookie_string_val):
            return cookie_string_val


class BlogHandler(BaseHandler):

    def blog_key(self, name = 'default'):
        '''
        define a parent (blog name) for all of our blog data
        '''
        return db.Key.from_path('blogs', name)


class MainPage(BlogHandler):
  def get(self):
      self.write('Hello, There is nothing here!')



class Post(db.Model, BlogHandler):
    '''
    define post entity
    '''

    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        '''
        render blog post
        '''

        self._render_text = self.content.replace('\n','<br>')
        return self.render_str("post.html", p = self)



class BlogFront(BlogHandler):
    '''
    blog front page, with recent 10 posts
    '''

    def get(self):
        '''
        get 10 recent posts from Post entity and render them using front.html
        '''

        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        self.render('front.html', posts = posts)

        

class PostPage(BlogHandler):
    '''
    Handle Post Page (permalink)
    '''

    def get(self, post_id):
        '''
        get post from database and render it using template
        '''

        # get the post key
        key = db.Key.from_path('Post', int(post_id), parent = self.blog_key())
        # get the post from db using key
        post = db.get(key)

        # show 404 if post is not available
        if not post:
            self.error(404)
            return

        # render post using permalink template
        # notice that post will have a render method (see definition) which will also be availble in jinja
        self.render("permalink.html", post = post)



class NewPost(BlogHandler):
    '''
    Handle new posts (submission & redirect)
    '''

    def get(self):
        '''
        render new post form
        '''
        self.render("newpost.html")

    def post(self):
        # get request params
        subject = self.request.get('subject')
        content = self.request.get('content')

        # if both subject and contents are proper, redirect
        # else render form with error
        if subject and content:
            p = Post(parent = self.blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)


class CookieTest(BlogHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')
        visit_cookie_str = str(visit_cookie_str)

        if visit_cookie_str:
            cookie_val = self.check_secure_cookie(visit_cookie_str)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1
        visits_cookie = self.make_secure_cookie(visits)

        self.response.headers.add_header('Set-Cookie','visits=%s' % visits_cookie) 
        # we are using add_header sytax as we don't want to override the previosly set 'Content-Type=text/plain' header
        self.write("You have been here %s times!" % visits)
        


# define handlers
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/cookietest', CookieTest),
                               ],
                              debug=True)

