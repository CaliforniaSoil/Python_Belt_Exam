from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import md5
import os, binascii
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile('^[A-z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        # Check whether email exists in db
        if User.objects.filter(email=postData['email']):
            errors.append('Email is already registered')
        # Validate first name
        if len(postData['name']) < 2:
            errors.append('Name must be at least 2 characters')
        elif not NAME_REGEX.match(postData['name']):
            errors.append('Name must only contain alphabet')
        # Validate last name
        if len(postData['alias']) < 2:
            errors.append('Alias must be at least 2 characters')
        elif not NAME_REGEX.match(postData['alias']):
            errors.append('Alias must only contain alphabet')
        # Validate email
        if len(postData['email']) < 1:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append('Invalid email format')
        # Validate password
        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters')
        # Validate confirm password
        elif postData['password'] != postData['confirm']:
            errors.append('Passwords do not match')

        # if no errors
        if len(errors) == 0:
            hashed_pw = md5.new(postData['password']).hexdigest()
            # add to database
            User.objects.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=hashed_pw)

        return errors

    def login(self, postData):
        errors = []
        # if email is found in db
        if User.objects.filter(email=postData['email']):
            hashed_pw = md5.new(postData['password']).hexdigest()
            # compare hashed passwords
            if User.objects.get(email=postData['email']).password != hashed_pw:
                errors.append('Incorrect password')
        # else if email is not found in db
        else:
            errors.append('Email has not been registered')
        return errors


class User(models.Model):
	name = models.CharField(max_length = 45)
	alias = models.CharField(max_length = 45)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	favorites = models.ManyToManyField("Quote", related_name="favorites", default=None)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

	def __str__(self):
		return "name:{}, alias:{}, email:{}, password:{}, created_at:{}, updated_at:{}".format(self.name, self.alias, self.email, self.password, self.created_at, self.updated_at)

class QuoteManager(models.Manager):
	def validateQuote(self, post_data):

		is_valid = True
		errors = []

		if len(post_data.get('content')) < 12:
			is_valid = False
			errors.append('Message must be more than 10 characters')
		return (is_valid, errors)

class Quote(models.Model):
	content = models.CharField(max_length = 255)
	author = models.CharField(max_length = 255)
	poster = models.ForeignKey(User, related_name = 'authored_quotes')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = QuoteManager()

	def __str__(self):
		return 'content:{}, author:{}'.format(self.content, self.user)
