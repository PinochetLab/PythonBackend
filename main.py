from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel


class UserForm(BaseModel):
    name: str
    password: str


class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password


class MessageForm(BaseModel):
    receiverName: str
    text: str


class Message:
    def __init__(self, sender: User, receiver: User, text: str):
        self.sender = sender
        self.receiver = receiver
        self.text = text


class MessageInfo:
    def __init__(self, message: Message):
        self.sender = message.sender.name
        self.receiver = message.receiver.name
        self.text = message.text


class Service:
    def __init__(self):
        self.users = []
        self.current_user = None
        self.messages = []
        self.micro_services = [Authorization(self, "/authorization/"), Chat(self, "/chat/")]
        for ms in self.micro_services:
            ms.setup_routes()
        self.routers = [ms.router for ms in self.micro_services]

    def __user_exists(self, user_form: UserForm) -> bool:
        return any(user.name == user_form.name for user in self.users)

    def register(self, user_form: UserForm):
        if self.is_authorized():
            raise HTTPException(401, 'You are authorized!')
        if self.__user_exists(user_form):
            raise HTTPException(401, 'User already exists!')
        self.current_user = User(user_form.name, user_form.password)
        self.users.append(self.current_user)

    def login(self, user_form: UserForm):
        if self.is_authorized():
            raise HTTPException(401, 'You are authorized!')
        if not self.__user_exists(user_form):
            raise HTTPException(401, 'User does not exist!')
        user = list(filter(lambda x: x.name == user_form.name, self.users))[0]
        if user.password != user_form.password:
            raise HTTPException(401, 'Password is not correct!')
        self.current_user = user

    def logout(self):
        if not self.is_authorized():
            raise HTTPException(401, "You are not authorized!")
        self.current_user = None

    def delete_user(self):
        if not self.is_authorized():
            raise HTTPException(401, "You are not authorized!")
        self.users.remove(self.current_user)
        self.current_user = None

    def is_authorized(self) -> bool:
        return self.current_user is not None

    def send_message(self, message_form: MessageForm):
        if not self.is_authorized():
            raise HTTPException(401, "Only authorized users can send messages!")
        if not any(user.name == message_form.receiverName for user in self.users):
            raise HTTPException(401, "Receiver does not exist!")
        receiver = list(filter(lambda x: x.name == message_form.receiverName, self.users))[0]
        if self.current_user == receiver:
            raise HTTPException(401, "You are trying to send message yourself")
        self.messages.append(Message(self.current_user, receiver, message_form.text))

    def sent_messages(self):
        if not self.is_authorized():
            raise HTTPException(401, "Only authorized users can read messages!")
        return list(map(lambda y: MessageInfo(y), filter(lambda x: x.sender == self.current_user, self.messages)))

    def received_messages(self):
        if not self.is_authorized():
            raise HTTPException(401, "Only authorized users can read messages!")
        return list(map(lambda y: MessageInfo(y), filter(lambda x: x.receiver == self.current_user, self.messages)))


class MicroService:
    def __init__(self, service: Service, prefix: str):
        self.service = service
        self.prefix = prefix
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        raise NotImplementedError()


class Authorization(MicroService):
    def setup_routes(self):
        @self.router.get(self.prefix)
        async def root():
            return {"status": "authorized" if self.service.is_authorized() else "not authorized",
                    "name": self.service.current_user.name if self.service.is_authorized() else "not authorized"}

        @self.router.post(self.prefix + "register")
        async def register(user_form: UserForm):
            self.service.register(user_form)

        @self.router.post(self.prefix + "login")
        async def login(user_form: UserForm):
            self.service.login(user_form)

        @self.router.post(self.prefix + "logout")
        async def logout():
            self.service.logout()

        @self.router.post(self.prefix + "delete_account")
        async def evaluate():
            self.service.delete_user()


class Chat(MicroService):
    def setup_routes(self):
        @self.router.get(self.prefix)
        async def root():
            return {"Welcome to", "Chat"}

        @self.router.post(self.prefix + "send")
        async def send(message_form: MessageForm):
            self.service.send_message(message_form)

        @self.router.get(self.prefix + "sent")
        async def sent_messages():
            return self.service.sent_messages()

        @self.router.get(self.prefix + "received")
        async def received_messages():
            return self.service.received_messages()


app = FastAPI()
for router in Service().routers:
    app.include_router(router)
