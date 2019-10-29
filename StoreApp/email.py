from flask_mail import Message
from StoreApp import mail
from flask import render_template

def send_receipt(email, product):
  msg = Message(subject='Coffee Shop Purchase' , sender=("Coffee Shop", mail.MAIL_USERNAME), recipients=[email])
  msg.body = render_template('email_receipt.html', product=product)
  msg.html = render_template('email_receipt.html', product=product)
  mail.send(msg)

def send_sale_notification():
  msg = Message(subject=email , sender=("Coffee Shop", mail.MAIL_USERNAME), recipients=["ty.timms16@gmail.com"])
  msg.body = name + ": " + text_body
  mail.send(msg)