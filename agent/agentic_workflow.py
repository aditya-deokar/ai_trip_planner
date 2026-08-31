
from typing import Optional
from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

class GraphBuilder():
    def __init__(self, model_provider: str = "groq", model_name: Optional[str] = None, checkpointer: Optional[MemorySaver] = None):
        self.model_loader = ModelLoader(model_provider=model_provider, model_name=model_name)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([* self.weather_tools.weather_tool_list, 
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list])
        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None
        self.checkpointer = checkpointer if checkpointer is not None else MemorySaver()
        self.system_prompt = SYSTEM_PROMPT
    
    
    def agent_function(self, state: MessagesState):
        """Main agent function with idempotent system prompt injection"""
        messages = state["messages"]
        # Only prepend system prompt if not already present at start of conversation
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [self.system_prompt] + list(messages)
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        self.graph = graph_builder.compile(checkpointer=self.checkpointer)
        return self.graph
        
    def __call__(self):
        return self.build_graph()