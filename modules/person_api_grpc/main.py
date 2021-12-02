
from __future__ import annotations
from typing import List
import grpc
import person_pb2_grpc as person_pb2_grpc
import person_pb2 as person_pb2
from concurrent import futures
from sqlalchemy import Column, Integer, String
from marshmallow import Schema, fields
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import os
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

PORT = os.environ.get("CONNECTION_PORT", "5000")

engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session.configure(bind=engine)  

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)


class PersonSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    company_name = fields.String()

    class Meta:
        model = Person

class PersonService:
    @staticmethod
    def retrieveMultiple(person_ids: List[int]) -> List[Person]:
        session = Session()
        person = session.query(Person).filter(
            Person.id.in_(person_ids)
        ).all()
        return person

    @staticmethod
    def getAll() -> List[Person]:
        session = Session()
        person = session.query(Person).all()
        return person


def convertPersonToProtoPerson(p):
    return person_pb2.Person(
        id = p.id,
        first_name = p.first_name,
        last_name = p.last_name,
        company_name = p.company_name
    )


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def GetByIds(self, request, context):

        print(f"GET BY IDS: {request.ids}")
        persons = PersonService.retrieveMultiple(request.ids)
        try:
            result = person_pb2.PersonList(
                persons = [convertPersonToProtoPerson(p) for p in persons]
            )
            return result
        except Exception as e:
            print(e)
            raise e

    def GetAll(self, request, context):
        print(f"GET ALL")
        persons = PersonService.getAll()
        try:
            result = person_pb2.PersonList(
                persons = [convertPersonToProtoPerson(p) for p in persons]
            )
            return result
        except Exception as e:
            print(e)
            raise e


    def Create(self, request, context):
        person_dict = {
            "id": request.id,
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name
        }

        person = PersonService.create(person_dict)
        return person_pb2.Person(**person)



def start_grpc_server():
    # Initialize gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)


    print(f"Server starting on port {PORT}...")
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    server.wait_for_termination()


start_grpc_server()