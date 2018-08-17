#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:zpp

from django.forms import Form,widgets,fields

class RegisterForm(Form):
	user = fields.CharField()
	name = fields.CharField()
	sex = fields.CharField()
	birthday = fields.CharField()
	email = fields.CharField()
	password = fields.CharField()
	job_number = fields.CharField()
	position = fields.CharField()
	department = fields.CharField()
	phone_number = fields.CharField()