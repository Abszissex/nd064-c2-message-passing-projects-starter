
from app.udaconnect.services import PersonService
import grpc
import person_pb2_grpc as person_pb2_grpc
import person_pb2 as person_pb2
import time
from concurrent import futures

class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def GetByIds(self, request, context):
        persons = PersonService.retrieveMultiple(request.ids)

        result = person_pb2.PersonList()
        result.persons.extend(persons)
        return result

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


    print("Server starting on port 5005...")
    server.add_insecure_port("[::]:5005")
    server.start()
    # Keep thread alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)