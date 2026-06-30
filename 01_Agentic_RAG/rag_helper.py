
INSTRUCTIONS = """ 
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."

"""


USER_PROMPT_TEMPLATE = """

Question:
{question}


Context:
{context}

"""



class RAGBase:

    def __init__(
        self, 
        index, 
        llm_client,
        course='llm-zoomcamp',
        instructions=INSTRUCTIONS,
        user_prompt_template=USER_PROMPT_TEMPLATE,
        model='gpt-5.4-mini'
    ):
        self.index = index
        self.llm_client = llm_client
        self.course = course
        self.instructions = instructions
        self.user_prompt_template = user_prompt_template
        self.model = model
    

    # Search the query
    def search(self, question):
        boost_dict = {'question': 2.0, 'section': 0.5}
        filter_dict = {'course' : self.course}

        return self.index.search(question,
                            boost_dict=boost_dict,
                            filter_dict=filter_dict,
                            num_results=5)




    # Build the prompt

    def build_context(self, search_results):
        lines = []
        
        for doc in search_results:
            lines.append(doc['section'])
            lines.append("Q: " + doc['question'])
            lines.append("Ans: " + doc['answer'])
            lines.append("")

        return "\n".join(lines).strip()

    def build_prompt(self, question, search_results):
        context = self.build_context(search_results=search_results)
        prompt = USER_PROMPT_TEMPLATE.format(
            question = question,
            context = context
        )

        return prompt.strip()


    # Send the prompt to LLM for answer
    def llm_response(self, prompt):
        llm_response = self.llm_client.chat.completions.create(
            messages = [
            { 'role': 'system',
                'content': self.instructions},
            {'role': 'user',
            'content': prompt}
            ],
            model=self.model
    )

        return llm_response.choices[0].message.content
        
    

    # Build the RAG pipeline

    def rag(self, query):
        search_results =  self.search(query)
        prompt = self.build_prompt(query, search_results)
        answer = self.llm_response(prompt)

        return answer


