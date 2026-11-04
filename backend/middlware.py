from langchain.agents.middleware import AgentMiddleware


class LoggingMiddleware(AgentMiddleware):

    def before_agent(self, state, runtime):
        states = ""
        print(f"####\nnn before running agent {states}")
        # print(f"runtime: {runtime}\n####")

    def after_agent(self, state, runtime):
        states = ""
        print(f"#####\n after running agent {states}")

    def before_model(self, state, runtime):
        states = ""
        print(f"####\n before running mdoel {states}")

    def after_model(self, state, runtime):
        states = ""
        print(f"####\n after running model {states}")


    













