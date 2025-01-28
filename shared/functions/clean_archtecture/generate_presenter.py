from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

groq_client = ChatGroq(model="llama-3.3-70b-specdec",
                       api_key=os.getenv("GROQ_API_KEY"))


def generate_presenter(inputs: dict):
    prompt = f"""
Create a presenter class with Python
Instantiate the repository
Instantiate the usecase
Instantiate the controller
Use the HttpResponse class to return the response

The context of the presenter structure is:
{inputs}

This is a example of a presenter class:
```python
from src.modules.get_all_alerts.app.get_all_alerts_controller import GetAllAlertsController
from src.modules.get_all_alerts.app.get_all_alerts_usecase import GetAllAlertsUsecase
from src.shared.environments import Environments
from src.shared.infra.repositories.alerts_repository_mock import AlertsRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest, HttpResponse

repo = Environments.get_alerts_repo()()
usecase = GetAllAlertsUsecase(repo=repo)
controller = GetAllAlertsController(usecase=usecase)


def get_all_alerts_presenter(request):
    request = HttpRequest(body=request)

    response = controller(request=request)

    return HttpResponse(body=response.body, status_code=response.status_code)```
    """

    client = groq_client
    response = client.invoke(prompt).content
    return response
