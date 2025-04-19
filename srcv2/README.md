# Autonomous Helper Agent v2

* ReAct version 2
* A real, useful application: The good old flight bookings app!

# Expected output

* Should look something like this:

```
Starting the application...

User query: I lost my baggage, what should I do?
Sending request to assistant...
[2025-04-20 02:35:53 AppRunner: Starting execution...
[2025-04-20 02:35:53 Interaction 1/10
[2025-04-20 02:35:53 Creating inference request with messages: [{'role': 'system', 'content': "\n    You are a helpful airline assistant that helps customers with their problems.\n    \n    Available tools:\n    1. transfer_to_lost_baggage: Use this tool when customers report lost baggage\n    2. transfer_to_cancelled_flights: Use this tool when customers have issues with cancelled flights\n    \n    Analyze the customer's query carefully and use the appropriate tool to help them.\n    If they mention lost baggage, use the transfer_to_lost_baggage tool.\n    If they mention cancelled flights, use the transfer_to_cancelled_flights tool.\n    "}, {'role': 'user', 'content': 'I lost my baggage, what should I do?'}]
[2025-04-20 02:35:53 Tools available: [{'type': 'function', 'function': {'name': 'transfer_to_lost_baggage', 'description': 'Transfer the customer to the lost baggage department when they report lost baggage', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'transfer_to_cancelled_flights', 'description': 'Transfer the customer to the cancelled flights department when they have issues with cancelled flights', 'parameters': {'type': 'object', 'properties': {}}}}]
[2025-04-20 02:35:53 Sending request to OpenAI...
[2025-04-20 02:35:55 Received response from OpenAI: {"content":null,"refusal":null,"role":"assistant","annotations":[],"audio":null,"function_call":null,"tool_calls":[{"id":"call_Qy0m0XpuxC9Q7FZRTfjkdPKz","function":{"arguments":"{}","name":"transfer_to_lost_baggage"},"type":"function"}]}
[2025-04-20 02:35:55 Processing tool call: transfer_to_lost_baggage
[2025-04-20 02:35:55 Executing tool: transfer_to_lost_baggage
Executing lost baggage transfer...
[2025-04-20 02:35:55 Tool execution successful: {'role': 'tool', 'name': 'transfer_to_lost_baggage', 'tool_call_id': 'call_Qy0m0XpuxC9Q7FZRTfjkdPKz', 'content': 'I will transfer you to the lost baggage department.'}
[2025-04-20 02:35:55 Interaction 2/10
[2025-04-20 02:35:55 Creating inference request with messages: [{'role': 'system', 'content': "\n    You are a helpful airline assistant that helps customers with their problems.\n    \n    Available tools:\n    1. transfer_to_lost_baggage: Use this tool when customers report lost baggage\n    2. transfer_to_cancelled_flights: Use this tool when customers have issues with cancelled flights\n    \n    Analyze the customer's query carefully and use the appropriate tool to help them.\n    If they mention lost baggage, use the transfer_to_lost_baggage tool.\n    If they mention cancelled flights, use the transfer_to_cancelled_flights tool.\n    "}, {'role': 'user', 'content': 'I lost my baggage, what should I do?'}, {'content': None, 'refusal': None, 'role': 'assistant', 'annotations': [], 'audio': None, 'function_call': None, 'tool_calls': [{'id': 'call_Qy0m0XpuxC9Q7FZRTfjkdPKz', 'function': {'arguments': '{}', 'name': 'transfer_to_lost_baggage'}, 'type': 'function'}]}, {'role': 'tool', 'name': 'transfer_to_lost_baggage', 'tool_call_id': 'call_Qy0m0XpuxC9Q7FZRTfjkdPKz', 'content': 'I will transfer you to the lost baggage department.'}]
[2025-04-20 02:35:55 Tools available: [{'type': 'function', 'function': {'name': 'transfer_to_lost_baggage', 'description': 'Transfer the customer to the lost baggage department when they report lost baggage', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'transfer_to_cancelled_flights', 'description': 'Transfer the customer to the cancelled flights department when they have issues with cancelled flights', 'parameters': {'type': 'object', 'properties': {}}}}]
[2025-04-20 02:35:55 Sending request to OpenAI...
[2025-04-20 02:35:56 Received response from OpenAI: {"content":"I have transferred you to the lost baggage department who will assist you further with your lost baggage issue.","refusal":null,"role":"assistant","annotations":[],"audio":null,"function_call":null,"tool_calls":null}
[2025-04-20 02:35:56 Conversation complete, breaking...
[2025-04-20 02:35:56 AppRunner: Execution completed

Assistant response:
user: I lost my baggage, what should I do?
assistant: None
Function called: None
tool: I will transfer you to the lost baggage department.
assistant: I have transferred you to the lost baggage department who will assist you further with your lost baggage issue.
Function called: None

Application finished.
```
