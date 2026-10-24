from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, Optional, Literal


# TypeDict is only for representating it does not perform runtime validation and can give wrong format output
# We are creating a review analyzer which analyze areview and generate its summary and sentiment
model=ChatOllama(
    model="qwen2.5:3b",
    base_url="http://127.0.0.1:11434"
)

#schema
json_schema={
  "title": "Review",
  "type": "object",
  "properties": {
    "key_themes": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Write down all the key themes discussed in the review in a list"
    },
    "summary": {
      "type": "string",
      "description": "A brief summary of the review"
    },
    "sentiment": {
      "type": "string",
      "enum": ["pos", "neg"],
      "description": "Return a sentiment of the review either negative, positive or neutral"
    },
    "pros": {
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the pros inside a list"
    },
    "cons": {
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the pros inside a list"
    },
    "name":{
        "type": ["array", "null"],
        "description":"Write the name of the reviewer"
    }
  },
"required": ["key_themes","summary","sentiment"]
}

#with_structured_output actually generates a system prompt telling how to return an output based on class attached, annotationn can be provided to give the definition of elemnts
structured_model= model.with_structured_output(json_schema)

result= structured_model.invoke("""I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it is an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I am gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful

Cons:
Bulky and heavy—not great for one-handed use
Bloatware still exists in One UI
Expensive compared to competitors""")

#it is a python dict
print(type(result))
print(result)