from flask import session, abort
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint, google
import requests
import os

bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
    hosted_domain="email.wm.edu"
)

def loggedin():
    return google.authorized

def userinfo():
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return resp.json()

@oauth_authorized.connect_via(bp)
def check_hosted_domain(blueprint, token):
    resp_json = userinfo()
    if resp_json["hd"] != blueprint.authorization_url_params["hd"]:
        print("HOSTED DOMAIN ERROR: "+resp_json["hd"])
        requests.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token["access_token"]}
        )
        session.clear()
        abort(403)
