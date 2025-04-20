# From the course: "Master Agentic Apps development from Scratch - Hands on!"  by Alex Souza

* Working exercises from the Udemy course: https://www.udemy.com/course/building-autonomous-apps-with-ai-agents-from-scratch/learn/lecture/47982817#reviews

# How to use:

* Look in src. You're a smart guy, figure it out.

# Agentic AI Application Development Tutorial

This repository serves as a practical guide for learning how to develop Agentic AI applications. It provides a progressive learning path through two implementations, demonstrating the evolution from basic concepts to production-ready patterns.

## Repository Overview

The codebase is organized into two main versions, showing the progression of development practices and concepts:
- `srcv1/`: Foundation implementation
- `srcv2/`: Advanced implementation with improvements

### Learning Objectives

1. **Understanding AI Agents**
   - Tool-using AI implementation
   - Conversation management
   - State handling
   - Agent-to-agent communication

2. **Software Engineering Best Practices**
   - Type safety
   - Error handling
   - Testing
   - Code organization
   - Documentation

3. **Practical Application**
   - Real-world use cases
   - Integration patterns
   - Production considerations

## Codebase Structure

### Version 1 (srcv1) - Foundation

Basic implementation focusing on core concepts:

```
srcv1/
├── brain.py         # Core thinking and memory management
├── common.py        # Basic types and shared utilities
├── tools.py         # Tool definitions and implementations
├── reactexecutor.py # Main execution logic
└── main.py         # Application entry point
```

#### Key Learning Points
1. ReAct (Reasoning and Acting) pattern implementation
2. Basic tool execution flow
3. Simple conversation management
4. Memory handling through the Brain class

### Version 2 (srcv2) - Advanced Implementation

Enhanced implementation with production-ready features:

```
srcv2/
├── runner.py       # Improved execution engine
├── custom_types.py # Enhanced type definitions
├── airline-app.py  # Practical application example
├── utils.py        # Shared utilities
├── tests/         # Testing infrastructure
└── common.py      # Shared components
```

#### Key Improvements
1. Robust error handling
2. Enhanced type safety
3. Improved conversation flow
4. Real-world application example
5. Better code organization

## Key Features and Concepts

### 1. Tool Management

Tools are defined as functions with metadata for AI use:

```python
lost_baggage_tool = AgentFunction(
    name="transfer_to_lost_baggage",
    description="Transfer the customer to the lost baggage department",
    function=transfer_to_lost_baggage,
)
```

**Learning Points:**
- Function wrapping for AI use
- Proper documentation
- Type safety in tool definitions

### 2. Conversation Management

The system manages AI conversations through a structured flow:

```python
def run(self, agent: Agent, messages: list, variables: dict, max_interactions=10):
    """Execute the conversation loop with improved flow control"""
```

**Key Concepts:**
- Message history management
- Context preservation
- Safety limits
- State management

### 3. Type Safety and Structure

Strong typing ensures reliable operation:

```python
class TaskResponse(BaseModel):
    """Encapsulates the possible responses from a task."""
    messages: List = []
    agent: Optional[Agent] = None
    context_variables: Dict = {}
```

**Features:**
- Pydantic model usage
- Type validation
- Clear interface definitions

### 4. Error Handling and Debugging

Robust error management ensures reliability:

```python
try:
    result = tool.function()
except Exception as e:
    debug_print(True, f"Error executing {tool_name}: {str(e)}")
```

**Implementation Aspects:**
- Comprehensive error catching
- Debugging utilities
- Error recovery patterns

## Educational Progression

### 1. Basic Concepts (srcv1)
- Understanding AI agents
- Basic tool usage
- Simple conversation flows
- Memory management

### 2. Advanced Concepts (srcv2)
- Complex conversation management
- Tool orchestration
- Type safety
- Error resilience
- Real-world applications

### 3. Best Practices
- Code organization
- Documentation
- Type safety
- Error handling
- Testing structure

## Practical Applications

### Airline Customer Service Bot

A real-world example implementing:
- Lost baggage handling
- Flight cancellation processing
- Multi-tool integration
- Error handling
- User interaction flows

### Tool Integration Examples

1. **Customer Service Tools**
   - Lost baggage handling
   - Flight cancellation processing

2. **Utility Tools**
   - Wikipedia searches
   - Calculator functions
   - Date handling

## Development Guidelines

### 1. Code Organization
- Clear module separation
- Logical file structure
- Consistent naming conventions

### 2. Type Safety
- Use of Pydantic models
- Clear interface definitions
- Proper type hints

### 3. Error Handling
- Comprehensive error catching
- Proper error reporting
- Recovery mechanisms

### 4. Testing
- Unit test structure
- Integration testing
- Error case coverage

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start with srcv1 for basic concepts
4. Progress to srcv2 for advanced implementation

## Learning Path

1. **Foundation (srcv1)**
   - Study basic agent implementation
   - Understand tool integration
   - Learn conversation management

2. **Advanced Concepts (srcv2)**
   - Explore improved architecture
   - Study error handling
   - Understand type safety

3. **Practical Application**
   - Implement airline bot features
   - Add custom tools
   - Handle real-world scenarios

## Conclusion

This codebase demonstrates the progression from basic AI agent concepts to production-ready implementations. Through practical examples and clear structure, it provides a comprehensive learning path for developers interested in building Agentic AI applications.

The evolution from srcv1 to srcv2 shows how to improve:
- Code organization
- Error handling
- Type safety
- Testing
- Real-world application

By following this guide and studying the code progression, developers can learn how to build robust, maintainable AI agent applications.
