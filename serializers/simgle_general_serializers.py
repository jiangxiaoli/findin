__author__ = 'FindIn'

def error_serializers(msg, code):

  return {"error":
            {"message":msg,
              "code": code}
          }