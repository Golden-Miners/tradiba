from typing import Dict, List

class MultimodalSkillSDK:
    """
    Multimodal Skill SDK letting Skill Packs declare supported modalities and access APIs.
    """
    def __init__(self):
        self.supported_inputs: List[str] = []
        self.supported_outputs: List[str] = []

    def declare_modalities(self, inputs: List[str], outputs: List[str]) -> None:
        self.supported_inputs = inputs
        self.supported_outputs = outputs

    def get_capabilities(self) -> Dict[str, List[str]]:
        return {
            "inputs": self.supported_inputs,
            "outputs": self.supported_outputs
        }
