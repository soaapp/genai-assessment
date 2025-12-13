"""
Agent tools for handling different types of user queries

Current tools:
- CalculatorTool
- WeatherTool
- WordProcessorTool
"""

import re, random
from ast import literal_eval

def tool_calc(q, trace):
    """Detect and evaluate mathematical expressions"""
    trace.append("CalculatorTool: Checking if query contains math expression")
    if match := re.search(r'\d[\d\s\+\-\*\/]*', q):
        expression = match.group(0).strip()
        trace.append(f"CalculatorTool: Found potential expression '{expression}'")
        # Verify prompt has at least one operator
        if len(expression) > 1 and any(op in expression for op in "+-*/"):
            trace.append(f"CalculatorTool: Validated expression contains operators")
            try:
                trace.append(f"CalculatorTool: Evaluating '{expression}'")
                # Using this eval to avoid "code injection" on the site. Ensures its safer if this was PROD level.
                result = str(eval(expression, {"__builtins__": {}}, {}))
                trace.append(f"CalculatorTool: Successfully calculated result = {result}")
                return "CalculatorTool", result
            except Exception as e:
                trace.append(f"CalculatorTool: Evaluation failed - {str(e)}")
                pass
        else:
            trace.append(f"CalculatorTool: Expression '{expression}' lacks valid operators, skipping")
    else:
        trace.append("CalculatorTool: No math expression found in query")
    return None

def tool_weather(q, trace):
    """Provide mock weather data for location-based queries"""
    trace.append("WeatherTool: Checking if query is weather-related")
    if "weather" in q.lower():
        trace.append("WeatherTool: Confirmed - keyword 'weather' found")
        trace.append("WeatherTool: Attempting to extract location from query")

        # Extract city from query
        city = "Unknown"
        for p in ["in ", "at ", "for "]:
            if p in q:
                city = q.split(p)[1].strip()
                trace.append(f"WeatherTool: Successfully extracted location '{city}'")
                break

        if city == "Unknown":
            trace.append("WeatherTool: No location found, using default 'Unknown'")

        # Generate random weather data
        trace.append("WeatherTool: Generating random weather data")
        conditions = ["Sunny", "Cloudy", "Rainy", "Snowing", "Partly Cloudy"]
        temp = random.randint(-10, 25)
        condition = random.choice(conditions)

        result = f"{temp}°C, {condition} in {city.title()}"
        trace.append(f"WeatherTool: Weather data ready -> {result}")
        return "WeatherTool", result
    else:
        trace.append("WeatherTool: No 'weather' keyword found, skipping")
    return None

def tool_text(q, trace):
    """Process text transformations or calculate query length as fallback."""
    trace.append("TextProcessorTool: Analyzing query for text processing keywords")

    if "upper" in q.lower():
        trace.append("TextProcessorTool: Found 'upper' keyword")
        trace.append("TextProcessorTool: Applying UPPERCASE transformation")
        result = q.upper()
        trace.append(f"TextProcessorTool: Transformation complete -> {result}")
        return "TextProcessorTool", result
    elif "lower" in q.lower():
        trace.append("TextProcessorTool: Found 'lower' keyword")
        trace.append("TextProcessorTool: Applying lowercase transformation")
        result = q.lower()
        trace.append(f"TextProcessorTool: Transformation complete -> {result}")
        return "TextProcessorTool", result
    else:
        trace.append("TextProcessorTool: No specific keyword found")
        trace.append("TextProcessorTool: Defaulting to length calculation (Fallback tool)")
        result = str(len(q))
        trace.append(f"TextProcessorTool: Query length = {result} characters")
        return "TextProcessorTool", result


# Tool registry for agent execution
AGENT_TOOLS = [tool_calc, tool_weather, tool_text]