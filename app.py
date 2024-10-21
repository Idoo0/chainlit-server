import chainlit as cl
import pandas as pd
import io
from getResponse import getQueryResponse, getConclusion
from query import getResultFromQuery
from pandasql import PandaSQLException
from pandasql import sqldf

@cl.on_message
async def on_message(message: cl.Message):
    if cl.context.session.client_type == "copilot":
        try:
            # Call the function to get table data as CSV
            fn = cl.CopilotFunction(name="getTableData", args={})
            csv_data = await fn.acall()
            print(f'\nPERTANYAAN: {message.content}\n')
            
            # Convert CSV to DataFrame
            df = pd.read_csv(io.StringIO(csv_data))
            df = change_column_names(df)
            print(f'\Data: {df}\n')

            # Get query for the question
            query = await getQuery(message.content)
            query = query.replace("```sql\n", "").replace("```", "")

            # Run query on database
            result = sqldf(query, env=None)

            # Get coclusion for the result
            response = getConclusion(message.content, query, result)

            await cl.Message(
                content=response
            ).send()

        except PandaSQLException as e:
            # Handle the PandaSQL-specific exception
            print("PandaSQL Exception occurred:", e)
            await cl.Message(content='Analisis sedang tidak bisa dilakukan, coba tanyakan lagi!').send()
        except Exception as e:
            # Handle any other exception that might occur
            print("An unexpected error occurred:", e)
            await cl.Message(content='Analisis sedang tidak bisa dilakukan, coba tanyakan lagi!').send()


@cl.on_chat_start
async def start():
    await cl.Message(content="Halo! Silahkan berikan saya pertanyaan tentang data pada table ini, saya akan membantu anda menganalisa dan menjawab pertanyaan anda.").send()


async def getQuery(input):
    return getQueryResponse(input)


def change_column_names(df):
    new_columns = []
    for column in df.columns:
        new_column = column.replace(' ', '_')
        new_columns.append(new_column)
    df.columns = new_columns
    return df
