from abc import ABC, abstractmethod

class VisionLLM(ABC):
     """
    Every vision model MUST follow this interface.
    """
     @abstractmethod
     def analyze(self, image_path: str)->dict:
         """
        Takes an image path and returns structured intelligence.
        Must follow the canonical schema.
        """
         pass
    
