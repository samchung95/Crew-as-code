import yaml
from jinja2 import Template
from crewai import Agent, Task, Crew
from typing import List, Dict, Optional, Any
from crew_as_code.models import LLM

class CrewAIAgent:
    def __init__(self,
                 name: str,
                 role: str,
                 goal: str,
                 description: str,
                 tasks: List[Dict[str, Any]],
                 tools: Optional[List[Any]] = None,
                 llm: Optional[str] = None,
                 allow_delegation: bool = False,
                 max_iter: int = 25,
                 max_rpm: Optional[int] = None,
                 verbose: bool = False):
        self.name = name
        self.role = role
        self.goal = goal
        self.description = description
        self.tasks = {task['name']: CrewAITask(**task) for task in tasks}
        self.tools = tools if tools is not None else []
        self.llm = llm
        self.allow_delegation = allow_delegation
        self.max_iter = max_iter
        self.max_rpm = max_rpm
        self.verbose = verbose

    def to_crewai_agent(self) -> Agent:
        """Convert CrewAIAgent instance to a CrewAI Agent."""
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.description,
            tools=self.tools,
            llm=self.llm,
            allow_delegation=self.allow_delegation,
            max_iter=self.max_iter,
            max_rpm=self.max_rpm,
            verbose=self.verbose
        )

    def get_task(self, task_name: str) -> Optional['CrewAITask']:
        """Retrieve a specific task by name."""
        return self.tasks.get(task_name)

class CrewAITask:
    def __init__(self, name: str, description: str, expected_output: str, tools: Optional[List[Any]] = None, context: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.expected_output = expected_output
        self.tools = tools if tools is not None else []
        self.context = context if context is not None else []

    def to_crewai_task(self, agent: Agent, context_tasks: Dict[str, Task]) -> Task:
        """Convert CrewAITask instance to a CrewAI Task."""
        return Task(
            description=self.description,
            expected_output=self.expected_output,
            agent=agent,
            tools=self.tools,
            context=[context_tasks[ctx_task] for ctx_task in self.context if ctx_task in context_tasks]
        )

class AgentSettings:
    def __init__(self,
                 llm: Optional[str] = None,
                 memory: bool = False,
                 verbose: bool = False):
        self.llm = llm
        self.memory = memory
        self.verbose = verbose

    def to_dict(self) -> Dict[str, Any]:
        return {
            'llm': self.llm,
            'memory': self.memory,
            'verbose': self.verbose
        }

class TaskAssignment:
    def __init__(self, task_name: str, context: Optional[List[str]] = None):
        self.task_name = task_name
        self.context = context if context is not None else []

class CrewManager:
    def __init__(self, yaml_file_path: str, context: Dict[str, Any]):
        self.yaml_file_path = yaml_file_path
        self.context = context
        self.agents: Dict[str, CrewAIAgent] = {}
        self.load_crew()

    def render_template(self, template_str: str) -> str:
        """Render a Jinja2 template with the current context."""
        template = Template(template_str)
        return template.render(self.context)

    def read_and_render_yaml(self) -> Dict[str, Any]:
        """Read and render the YAML file with the current context."""
        with open(self.yaml_file_path, 'r') as file:
            yaml_content = file.read()
        rendered_yaml = self.render_template(yaml_content)
        return yaml.safe_load(rendered_yaml)

    def load_crew(self) -> None:
        """Load the crew configuration from the YAML file."""
        config = self.read_and_render_yaml()
        self.agents = {
            agent_data['name']: CrewAIAgent(
                name=agent_data['name'],
                role=agent_data['role'],
                goal=agent_data['goal'],
                description=agent_data['description'],
                allow_delegation=agent_data.get('delegation', False),
                tasks=agent_data['tasks'],
                tools=[]  # Add logic to parse tools if defined in the YAML
            ) for agent_data in config.get('agents', [])
        }

    def get_agent(self, agent_name: str) -> Optional[CrewAIAgent]:
        """Retrieve a specific agent by name."""
        return self.agents.get(agent_name)

    def get_task(self, agent_name: str, task_name: str) -> Optional[CrewAITask]:
        """Retrieve a specific task by agent name and task name."""
        agent = self.get_agent(agent_name)
        if agent:
            return agent.get_task(task_name)
        return None

    def reload_crew(self, new_context: Dict[str, Any]) -> None:
        """Reload the crew configuration with a new context."""
        self.context = new_context
        self.load_crew()

    def to_crewai_crew(self, agent_settings: Dict[str,AgentSettings], task_assignments: List[TaskAssignment]) -> Crew:
        """Create a CrewAI Crew from agent and task assignments."""
        crew_agents = []
        crew_tasks = []
        context_tasks = {}

        # Create agents
        for agent_name in agent_settings.keys():
            agent = self.get_agent(agent_name)
            if agent:
                for task_name in agent.tasks.keys():
                    context_tasks[task_name] = None
        
        # Create tasks and assign contexts
        agents = [agent for agent in self.agents.values() if agent.name in [agent_name for agent_name in agent_settings]]
        for agent in agents:
            agent_settings_full = {
                    'role': agent.role,
                    'goal': agent.goal,
                    'backstory': agent.description,
                    'tools': agent.tools,
                    'allow_delegation': agent.allow_delegation,
                    'max_iter': agent.max_iter,
                    'max_rpm': agent.max_rpm,
                    **agent_settings[agent.name].to_dict()
                }
            # print(agent_settings[agent.name].to_dict())
            agent_instance = Agent(
                **agent_settings_full
            )
            crew_agents.append(agent_instance)
            # print(crew_agents)
            agent_name = agent.name
            # Loop through task assignments to find matching tasks for the agent
            for assignment in task_assignments:
                task = self.get_task(agent_name, assignment.task_name)
                if task:
                    task_instance = {
                        'description': task.description,
                        'expected_output': task.expected_output,
                        'tools': task.tools,
                        'context': [context_tasks[ctx_task] for ctx_task in assignment.context if ctx_task in context_tasks],
                        'agent': agent_instance
                    }

                    task_instance = Task(
                        **task_instance
                    )
                    crew_tasks.append(task_instance)
                    context_tasks[assignment.task_name] = task_instance

        return Crew(
            agents=crew_agents,
            tasks=crew_tasks,
            verbose=2  # Set to desired verbosity level
        )

if __name__ == '__main__':

    LLMS = LLM("GROQ_API_KEYS")
    # Example usage:
    context = {
        'text': 'Sample text for metadata extraction',
        'segmented_text': 'Sample segmented text for question extraction',
    }
    yaml_file_path = 'agents.yaml'
    manager = CrewManager(yaml_file_path, context)
    # To reload the crew with new context data:
    new_context = {
        'text': 'Updated text for metadata extraction',
        'segmented_text': 'Updated segmented text for question extraction',
    }
    manager.reload_crew(new_context)
    # Hand-pick specific agents and tasks with additional parameters
    agent_assignments = {
        'metadata_extraction_agent': AgentSettings(llm=LLMS.groq_8b(), memory=False, verbose=True),
        'question_extraction_agent': AgentSettings(llm=LLMS.groq_8b(), memory=False, verbose=True)
    }
    task_assignments = [
        TaskAssignment(task_name='metadata_task'),
        TaskAssignment(task_name='question_extraction_task', context=['metadata_task'])
    ]
    crew = manager.to_crewai_crew(agent_assignments, task_assignments)
    # results = crew.kickoff()
    print(crew)
