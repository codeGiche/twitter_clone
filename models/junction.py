# followers function
from main import db

followers = db.Table("follower_followee_jk", 
                    db.Column("me_user_id_follower",db.Integer,db.ForeignKey("users_twitter.id")),
                    db.Column("followee_id_followee", db.Integer, db.ForeignKey("users_twitter.id")))