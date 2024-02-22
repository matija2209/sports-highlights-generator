# import os

# import vertexai
# from google.cloud import aiplatform
# from vertexai.generative_models import GenerativeModel, Part
# from google.api_core.client_options import ClientOptions
# from google.cloud.speech_v2 import SpeechClient
# from google.cloud.speech_v2.types import cloud_speech
# import requests
# import io,os
# from google.cloud.speech_v2.types import ExplicitDecodingConfig

# GCP_PROJECT_ID=os.environ.get("GCP_PROJECT_ID")
# GCP_LOCATION=os.environ.get("GCP_LOCATION")

# # https://cloud.google.com/vertex-ai/docs/generative-ai/start/quickstarts/quickstart-multimodal
# # https://gemini.google.com/app/91688c92f95b27d5
# def generate_with_bard(prompt:str, text=None,tokens=256)->str:
#     try:
#         vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
#            # Load the model
#         multimodal_model = GenerativeModel("gemini-1.0-pro")
#         # Query the model
#         response = multimodal_model.generate_content(
#             stream=False,
#             generation_config={
#                  "temperature": 0.0,
#             },
#             contents=f"{prompt} {text}" if text else prompt,
#         )
#         return response.text
#     except Exception as e:
#         raise Exception("Gemini has failed to generate text",e) from e

