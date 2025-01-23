class Permissions:
    @staticmethod
    def password(request_user=None, target_user=None):
        type_user = request_user["type_user"]
        if type_user == "admin":
            return True
        elif type_user == "broker":
            return request_user["type_broker"] == target_user["type_client"] or request_user["type_broker"] == target_user["type_broker"]
        elif type_user == "client":
            return request_user["account"] == target_user["account"]
        return False

    @staticmethod
    def view_data(request_user):
        return request_user["type_user"] == "admin"