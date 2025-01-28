from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

groq_client = ChatGroq(model="llama-3.3-70b-specdec",
                       api_key=os.getenv("GROQ_API_KEY"))


def generate_controller(inputs: dict):
    prompt = f"""
Create a controller class with Python
Use the injectable usecase
Use the viewmodel to return the response
Use the exception handler to return the errors

The context of the controller structure is:
{inputs}

This is a example of a controller class:
```python
from src.modules.get_all_alerts.app.get_all_alerts_usecase import GetAllAlertsUsecase
from src.modules.get_all_alerts.app.get_all_alerts_viewmodel import GetAllAlertsViewmodel
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetAllAlertsController:
    def __init__(self, usecase: GetAllAlertsUsecase):
        self.GetAllAlertsUsecase = usecase
    def __call__(self, request: IRequest) -> IResponse:
        try:
            alerts = self.GetAllAlertsUsecase()
            viewmodel = GetAllAlertsViewmodel(alerts)
            return OK(viewmodel.to_dict())
        except NoItemsFound as err:
            return NotFound(body=err.message)
        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=err.args[0])```
    """

    client = groq_client
    response = client.invoke(prompt).content
    return response
