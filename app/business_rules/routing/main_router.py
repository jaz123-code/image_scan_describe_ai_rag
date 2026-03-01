from app.services.model_engines.openai_vision import OpenAIVision
from app.services.model_engines.local_vision import LocalVision

def get_vision_engine(provider: str):
    provider = provider.lower()
    match provider:
        case "openai":
            return OpenAIVision()
        case "local":
            return LocalVision()
        case _:
            raise ValueError(f"Unsupported provider: {provider}")