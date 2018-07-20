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
from models import Post
from models import Author

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
    def get(self):
        template = jinja_current_directory.get_template(
            'templates/posts.html')
        self.response.write(template.render())

    def post(self):
        title_input = self.request.get('title')
        content_input = self.request.get('content')
        username_input = self.request.get('username')

        blog_post = Post(title=title_input, content=content_input)
        blog_post.put()

        check_authors = Author.query(Author.username == username_input).fetch()
        # check_authors = [Author(username, posts), Author(), Author()]
        if len(check_authors) > 0:
            author = check_authors[0]
            author.posts.append(blog_post.key)
        else:
            author = Author(username=username_input, posts=[blog_post.key])

        author.put()

        blog_posts = []
        for blog_post_key in author.posts:
            blog_posts.append(blog_post_key.get())

        template_vars = {
            'username': username_input,
            'blog_posts': blog_posts
        }
        template = jinja_current_directory.get_template(
            'templates/show_many_posts.html')
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/aboutme', AboutMeHandler),
    ('/posts', PostHandler)
], debug=True)
