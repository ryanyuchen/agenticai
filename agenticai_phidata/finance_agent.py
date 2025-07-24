from phi.agent import Agent
from phi.mode.groa import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

# web search agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id="chatgpt-4o"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True
    markdown=True
)

# finanical agent
finanical_agent = Agent(
    name="Finanical AI Agent",
    role="",
    model=Groq(id="chatgpt-4o"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentials=True, company_news=True)
    ],
    instructions=["Use tables to display the data"],
    show_tool_calls=True
    markdown=True
)

multi_ai_agent = Agent(
    team=[web_search_agent, finanical_agent],
    instructions=["Always include sources", "Use table to display the data"]
    show_tool_calls=True,
    markdown=True
)

mutlti_ai_agent.print_response("Summarize analyst recomendation and share the latest news for NVDIA", stream=True)
