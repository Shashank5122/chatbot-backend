
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_llm_chain(llm):
    prompt_template = """
    <|system|>
    Answer the question based on your knowledge. Use the following context to help:

    {context}

    </s>
    <|user|>
    {question}
    </s>
    <|assistant|>
    """

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    return prompt | llm | StrOutputParser()
