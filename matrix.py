from matrix_client.client import MatrixClient

class Matrix:
    def __init__(self, username, password, homeserver):
        self.username = username
        self.password = password
        self.homeserver = homeserver

    def send_notification(self, roomid, text):
        client = MatrixClient(self.homeserver)
        token = client.login(username=self.username, password=self.password)
        room = client.join_room(roomid)
        room.send_text(text)
