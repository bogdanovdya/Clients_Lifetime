from app import db


class PortalAuth(db.Model):
    portal = db.Column(db.CHAR(255), primary_key=True)
    access_token = db.Column(db.CHAR(255))
    refresh_token = db.Column(db.CHAR(255))
    event_counter = db.Column(db.INTEGER, default=0)

    def __init__(self, *args, **kwargs):
        super(PortalAuth, self).__init__(*args, **kwargs)
