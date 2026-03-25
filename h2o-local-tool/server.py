import asyncio
import random
import uuid
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

server = Server("h2o-data-utility")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="generate_uuid",
            description="Generate a new random UUID (version 4) and return it as a string.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="random_choice",
            description="Return one randomly selected string from a provided list of options.",
            inputSchema={
                "type": "object",
                "properties": {
                    "options": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "A non-empty list of strings to choose from.",
                        "minItems": 1,
                    }
                },
                "required": ["options"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    if name == "generate_uuid":
        result = str(uuid.uuid4())
        return [types.TextContent(type="text", text=result)]

    if name == "random_choice":
        options: list[str] = arguments.get("options", [])
        if not options:
            raise ValueError("The 'options' list must contain at least one item.")
        result = random.choice(options)
        return [types.TextContent(type="text", text=result)]

    raise ValueError(f"Unknown tool: '{name}'")


async def main() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
