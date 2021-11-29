
from flask_restplus import fields
from app.udaconnect.schemas import (
    LocationSchema,
)
from app.udaconnect.services import LocationService
from flask import request, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

locationModel = api.model('Location', {
    'person_id': fields.Integer(required=True),
    'longitude': fields.String(required=True),
    'latitude': fields.String(required=True),
})


@api.route("/locations")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(status_code=202)
    @api.doc(responses={202: 'Accepted'})
    @api.doc(responses={400: 'Invalid Payload'})
    @api.doc(body=locationModel)
    def post(self):
        try:
            LocationService.create(request.get_json())
        except Exception as e:
            print(e)
            return Response(str(e), status=400)

        return Response(status=202)

    