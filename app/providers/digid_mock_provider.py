import uuid
from inject import autoparams

from fastapi import Request
from fastapi.responses import RedirectResponse, Response

from max_core.services.template_service import TemplateService
from max_core.models.digid_mock_requests import DigiDMockRequest, DigiDMockCatchRequest
from typing import Dict

class DigidMockProvider:
    @autoparams("template_service")
    def __init__(self, identities: Dict[str, str], template_service: TemplateService):
        self._template_renderer = template_service.templates
        self._identities = identities

    def digid_mock(
        self, request: Request, digid_mock_request: DigiDMockRequest
    ) -> Response:
        state = digid_mock_request.state
        authorize_request = digid_mock_request.authorize_request
        idp_name = digid_mock_request.idp_name
        relay_state = digid_mock_request.RelayState
        artifact = str(uuid.uuid4())

        template_context = {
            "artifact": artifact,
            "relay_state": relay_state,
            "state": state,
            "idp_name": idp_name,
            "authorize_request": authorize_request,
            "identities": self._identities,
            "layout": "layout.html",
            "page_title": "DigiD Mock Login",
        }

        return self._template_renderer.TemplateResponse(
            request=request,
            name="digid_mock.html",
            context=template_context,
        )

    def digid_mock_catch(self, request: DigiDMockCatchRequest) -> RedirectResponse:
        bsn = request.bsn
        relay_state = request.RelayState

        response_uri = "acs" + f"?SAMLart={bsn}&RelayState={relay_state}&mocking=1"
        return RedirectResponse(response_uri, status_code=303)
