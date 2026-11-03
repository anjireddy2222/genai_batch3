from langchain.agents.middleware import AgentMiddleware


class LoggingMiddleware(AgentMiddleware):

    def before_agent(self, state, runtime):
        print(f"####\nnn before running agent {state}")
        print(f"runtime: {runtime}\n####")

    def after_agent(self, state, runtime):
        print(f"#####\n after running agent {state}")

    def before_model(self, state, runtime):
        print(f"####\n before running mdoel {state}")

    def after_model(self, state, runtime):
        print(f"####\n after running model {state}")


    













