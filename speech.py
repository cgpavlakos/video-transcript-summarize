import oci
import json

compartment_id = "ocid1.compartment.oc1..aaaaaaaao6gsecwqnnmwttt3fbuba2tmuunsliyidbnwmytarhbbwez6mlpq"
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

with open("input.txt", "r") as file:
    input_text = file.read()

with open("instruction.txt", "r") as file2:
    instruction_text = file2.read()

#instruction_text = "Summarize this transcript with both an overview and detailed bullet points. Start with an overview in a couple of sentences. After that use bullet points to provide plenty of detail. Your response should be 1-2 pages long."
# Service endpoint
endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"

generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
chat_detail = oci.generative_ai_inference.models.ChatDetails()

chat_request = oci.generative_ai_inference.models.CohereChatRequest()
chat_request.preambleOverride = "You are an Oracle employee tasked with putting together an executive summary of an hour-long conversation. You have been given the transcript."
chat_request.message = instruction_text + input_text
chat_request.temperature = 0
chat_request.frequency_penalty = 0
chat_request.top_p = 0.75
chat_request.top_k = 0
chat_request.max_tokens = 3000



chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceya7ozidbukxwtun4ocm4ngco2jukoaht5mygpgr6gq2lgq") #command-r-plus
chat_detail.chat_request = chat_request
chat_detail.compartment_id = compartment_id
chat_response = generative_ai_inference_client.chat(chat_detail)
# Print result
print("**************************Summarization Result**************************")
print("")
#print(vars(chat_response)) ##put this back for debug
try:
    # Get the 'chat_response' attribute, then access the 'text' within it
    text_result = chat_response.data.chat_response.text  
    print(text_result)

except (AttributeError, KeyError) as e:
    print(f"Error processing response: {e}")

with open("output.txt", "w") as outfile:
    try:
        # Get the 'chat_response' attribute, then access the 'text' within it
        text_result = chat_response.data.chat_response.text
        outfile.write(text_result)
        print("Result written to output.txt")

    except (AttributeError, KeyError) as e:
        outfile.write(f"Error processing response: {e}")
        print(f"Error written to output.txt: {e}")
