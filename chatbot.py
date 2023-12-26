from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class Chatbot:
    history = {}

    context = """
    You are automated Recruitment Assistant for VXI Philippines

    Below are the following comma separated job vacancies in different sites:

    Site, Job Vacancy
    Makati, Sales Associate
    Makati, Project Manager
    Makati, Instructional Designer
    Makati, Reporting and Compliance Associate
    Makati, Financial Revenue Analyst
    Makati, Business Intelligence Supervisor
    Makati, Sr. Business Intelligence Analyst
    Makati, Peza Associate (Active Pooling)
    Makati, Business Intelligence Analyst
    QC North EDSA, Customer Service Associate
    QC North EDSA, Sales Associate
    QC North EDSA, Techinical Support Associate
    QC North EDSA, Realtime Analyst
    QC North EDSA, Project Manager
    QC North EDSA, Instructional Designer
    QC North EDSA, Workforce Scheduler
    QC North EDSA, Multimedia Creator
    QC North EDSA, Jr. Multimedia Creator
    Pasay, Customer Service Associate
    Bridgetowne, Customer Service Associate
    Bridgetowne, Sales Associate

    Ask the user in which site they are interested to apply
    Tell them all available sites that have vacancy
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.llm = ChatOpenAI()

    def getHistory(self):
        if self.user_id in self.history:
            return self.history[self.user_id]
        self.history[self.user_id] = list()
        return self.history[self.user_id]

    def saveMessage(self, message):
        chat_history = self.getHistory()
        chat_history.append(message)
        self.history[self.user_id] = chat_history
        
    def chatAi(self, message):
        chat = HumanMessage(content = message)
        messages = [
            SystemMessage(content = self.context),
            *self.getHistory(),
            chat
        ]
        response = self.llm.invoke(messages)
        self.saveMessage(chat)
        self.saveMessage(response)
        return response