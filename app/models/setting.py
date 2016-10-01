from . import db


class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    # S3
    aws_key = db.Column(db.String)
    aws_secret = db.Column(db.String)
    aws_bucket_name = db.Column(db.String)
    # Google Auth
    google_client_id = db.Column(db.String)
    google_client_secret = db.Column(db.String)
    # Stripe Keys
    stripe_client_id = db.Column(db.String)
    stripe_secret_key = db.Column(db.String)
    stripe_publishable_key = db.Column(db.String)
    # PayPal Credentials
    paypal_mode = db.Column(db.String)
    paypal_sandbox_username = db.Column(db.String)
    paypal_sandbox_password = db.Column(db.String)
    paypal_sandbox_signature = db.Column(db.String)
    paypal_live_username = db.Column(db.String)
    paypal_live_password = db.Column(db.String)
    paypal_live_signature = db.Column(db.String)
    # FB
    fb_client_id = db.Column(db.String)
    fb_client_secret = db.Column(db.String)
    # Twitter
    tw_consumer_key = db.Column(db.String)
    tw_consumer_secret = db.Column(db.String)
    # Instagram
    in_client_id = db.Column(db.String)
    in_client_secret = db.Column(db.String)
    # Sendgrid
    sendgrid_key = db.Column(db.String)
    # Google Analytics
    analytics_key = db.Column(db.String)
    # App secret
    secret = db.Column(db.String)
    # storage place, local, s3, .. can be more in future
    storage_place = db.Column(db.String)
    # Social links
    google_url = db.Column(db.String)
    github_url = db.Column(db.String)
    twitter_url = db.Column(db.String)
    support_url = db.Column(db.String)
    facebook_url = db.Column(db.String)
    youtube_url = db.Column(db.String)
    android_app_url = db.Column(db.String)
    web_app_url = db.Column(db.String)

    def __init__(self, aws_key=None, aws_secret=None, aws_bucket_name=None,
                 google_client_id=None, google_client_secret=None,
                 fb_client_id=None, fb_client_secret=None, tw_consumer_key=None,
                 stripe_client_id=None,
                 stripe_secret_key=None, stripe_publishable_key=None,
                 in_client_id=None, in_client_secret=None,
                 tw_consumer_secret=None, sendgrid_key=None,
                 secret=None, storage_place=None,
                 google_url=None, github_url=None,
                 twitter_url=None, support_url=None,
                 analytics_key=None,
                 paypal_mode=None,
                 paypal_sandbox_username=None,
                 paypal_sandbox_password=None,
                 paypal_sandbox_signature=None,
                 paypal_live_username=None,
                 paypal_live_password=None,
                 paypal_live_signature=None,
                 facebook_url=None, youtube_url=None, android_app_url=None, web_app_url=None):
        self.aws_key = aws_key
        self.aws_secret = aws_secret
        self.aws_bucket_name = aws_bucket_name
        self.google_client_id = google_client_id
        self.google_client_secret = google_client_secret
        self.fb_client_id = fb_client_id
        self.fb_client_secret = fb_client_secret
        self.tw_consumer_key = tw_consumer_key
        self.tw_consumer_secret = tw_consumer_secret
        self.in_client_id = in_client_id
        self.in_client_secret = in_client_secret
        self.sendgrid_key = sendgrid_key
        self.analytics_key = analytics_key
        self.secret = secret
        self.storage_place = storage_place
        self.google_url = google_url
        self.github_url = github_url
        self.twitter_url = twitter_url
        self.support_url = support_url
        self.facebook_url = facebook_url
        self.youtube_url = youtube_url
        self.stripe_client_id = stripe_client_id
        self.stripe_publishable_key = stripe_publishable_key
        self.stripe_secret_key = stripe_secret_key
        self.web_app_url = web_app_url
        self.android_app_url = android_app_url
        self.paypal_mode = paypal_mode
        self.paypal_sandbox_username = paypal_sandbox_username
        self.paypal_sandbox_password = paypal_sandbox_password
        self.paypal_sandbox_signature = paypal_sandbox_signature
        self.paypal_live_username = paypal_live_username
        self.paypal_live_password = paypal_live_password
        self.paypal_live_signature = paypal_live_signature

    def __repr__(self):
        return 'Settings'

    def __str__(self):
        return str(self).encode('utf-8')

    def __unicode__(self):
        return 'Settings'
