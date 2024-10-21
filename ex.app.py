import chainlit as cl
from getResponse import getQueryResponse, getConclusion;
from query import getResultFromQuery;

@cl.on_message
async def main(message: cl.Message):
    content = message.content   
    print(message.content)
    # Extract CSV data and question if available
    if 'context' in content and 'question' in content:
        context = content['context']
        question = content['question']
        
        # Process the CSV data and question
        print("Received context (CSV):", context)
        print("Received question:", question)

        # You can now use context and question in your LLM
        response = await getQuery(question)
        formated = response.replace("```sql\n", "").replace("```", "")
        print(formated)

        # Run query on database
        responseQ = getResultFromQuery(formated)
        print(responseQ)

        # Get final conclusion
        responseFinal = getConclusion(question, formated, responseQ)

        # Send the response back
        await cl.Message(
            content=responseFinal,
        ).send()
    else:
        print('no context!')
        # Handle case where only a question is sent
        response = await getQuery(content)
        formated = response.replace("```sql\n", "").replace("```", "")
        print(formated)
        responseQ = getResultFromQuery(formated)
        print(responseQ)
        responseFinal = getConclusion(content, formated, responseQ)

        await cl.Message(
            content=responseFinal,
        ).send()

async def getQuery(input):
    return getQueryResponse(input)