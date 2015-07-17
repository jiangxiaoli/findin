__author__ = 'FindIn'

def user_wish_serializers(id, wish):

    return {"user":
                {"id":id,
                 "wish": wish}
    }