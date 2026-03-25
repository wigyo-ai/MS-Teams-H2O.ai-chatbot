# H2O Data Utility MCP Tool

This tool provides enterprise data utility functions accessible via the Model Context Protocol (MCP).

## Available Tools

### `generate_uuid`
Generates a new, cryptographically random UUID (version 4) and returns it as a string. Useful for creating unique identifiers for records, sessions, or any entity requiring a globally unique ID.

### `random_choice`
Accepts a list of strings and returns one randomly selected item. Useful for sampling from options, assigning random values, or prototyping randomized logic.

## Usage

This is a stdio-based MCP server intended for use with Enterprise h2oGPTe as a Local MCP Tool. Upload the ZIP bundle via the h2oGPTe interface to make these tools available to your AI agents.
