from dotenv import load_dotenv

from langchain_community.tools import RequestsPostTool
from langchain_community.utilities.requests import TextRequestsWrapper
import json
load_dotenv()

# headers: tokens -> jwt tokens, api keys
# api input data -> 

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer jkfgakjfgakjsf379tguaksfjasjfbuw9t387tiugakfhakufhawiuf32r8723tgiaukfhaskfuwr378tiugafjgafugaiufwgiuwgqiuguifgwiu",
    "API-Key": "skjfgakfjgkajgfakjggakjfakjGFKAJFGEHFASBGFSAKJ"
}

api_wrapper = TextRequestsWrapper(headers=headers)

api_tool = RequestsPostTool( requests_wrapper = api_wrapper, allow_dangerous_requests = True )


input_data =  {
    "url": "https://dummyjson.com/products/add",
    "data": {
        "title": "BMW m series"
    }
}

input_data = json.dumps(input_data)

api_result = api_tool.run(input_data)


print( api_result )
