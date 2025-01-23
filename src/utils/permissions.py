class Permissions:
    @staticmethod
    def verify(action, request_user=None, target_user=None):
        actions = ["view_data", "update_password"]
        type_user = request_user["type_user"]
        if type_user == "admin":
            return True
        elif type_user == "broker" and action in actions:
            return request_user["type_broker"] == target_user["type_client"] or request_user["type_broker"] == target_user["type_broker"]
        elif type_user == "client" and action in actions:
            return request_user["account"] == target_user["account"]
        return False
