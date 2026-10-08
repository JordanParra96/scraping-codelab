import asyncio
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from playwright.async_api import async_playwright
from langchain_community.agent_toolkits.playwright.toolkit import (
    PlayWrightBrowserToolkit,
)


async def main():
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)

    playwright = await async_playwright().start()
    async_browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    tools = toolkit.get_tools()
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=(
            "You can use a web browser, you can click on buttons, search on inputs, and look up any information on any website."
        ),
    )

    out = await agent.ainvoke({
        "messages": [
            SystemMessage(content="You are a helpful assistant"),
            HumanMessage(content="""
                Go to https://quotes.toscrape.com/
                Look at the first quote and translate it to three languages:
                spanish, japanese and swahili
                """)
        ]
    })

    response = out["messages"][-1].text
    print(response)

    await async_browser.close()
    await playwright.stop()


if __name__ == "__main__":
    asyncio.run(main())
