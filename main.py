#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import os
import jinja2

#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template('my_blog.html')
        self.response.write(template.render())

class AboutMeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template('about_me.html')
        self.response.write(template.render())

class PostHandler(webapp2.RequestHandler):
    # GET Request Handler
    def get(self):
        # Store 'new_post.html' template in variable.
        template = jinja_current_dir.get_template('new_post.html')
        # Render template and write it to GET response.
        self.response.write(template.render())

    # POST Request Handler
    def post(self):
        # Save data from form.
        tweet = self.request.get('tweet')

        # Put data into dictionary for Jinja.
        template_vars = { "tweet" : tweet }

        # Store template in variable.
        template = jinja_current_dir.get_template('view_post.html')

        # Render template with dictionary data, write to POST response.
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/aboutme', AboutMeHandler),
    ('/posts', PostHandler)
], debug=True)
