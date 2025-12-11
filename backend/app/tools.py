import re, random

def log(trace, msg):
    trace.append(f"Step {len(trace)+1}: {msg}")

def tool_calc(q, trace):
    log(trace, "CalculatorTool: Checking if query contains math expression")
    if match := re.search(r'\d[\d\s\+\-\*\/]*', q):
        expression = match.group(0).strip()
        log(trace, f"CalculatorTool: Found potential expression '{expression}'")
        # Verify prompt has at least one operator
        if len(expression) > 1 and any(op in expression for op in "+-*/"):
            log(trace, f"CalculatorTool: Validated expression contains operators")
            try:
                log(trace, f"CalculatorTool: Evaluating '{expression}'")
                result = str(eval(expression))
                log(trace, f"CalculatorTool: Successfully calculated result = {result}")
                return "CalculatorTool", result
            except Exception as e:
                log(trace, f"CalculatorTool: Evaluation failed - {str(e)}")
                pass
        else:
            log(trace, f"CalculatorTool: Expression '{expression}' lacks valid operators, skipping")
    else:
        log(trace, "CalculatorTool: No math expression found in query")
    return None

def tool_weather(q, trace):
    log(trace, "WeatherTool: Checking if query is weather-related")
    if "weather" in q.lower():
        log(trace, "WeatherTool: Confirmed - keyword 'weather' found")
        log(trace, "WeatherTool: Attempting to extract location from query")

        # TODO: If the city is still Unknown maybe we can fallback on saying "Unable to get weather"
        city = "Unknown"
        for p in ["in ", "at ", "for "]:
            if p in q:
                city = q.split(p)[1].strip()
                log(trace, f"WeatherTool: Successfully extracted location '{city}'")
                break

        if city == "Unknown":
            log(trace, "WeatherTool: No location found, using default 'Unknown'")

        # Randomize weather for fun
        log(trace, "WeatherTool: Generating random weather data")
        conditions = ["Sunny", "Cloudy", "Rainy", "Snowing", "Partly Cloudy"]
        temp = random.randint(-10, 25)
        condition = random.choice(conditions)

        result = f"{temp}°C, {condition} in {city.title()}"
        log(trace, f"WeatherTool: Weather data ready -> {result}")
        return "WeatherTool", result
    else:
        log(trace, "WeatherTool: No 'weather' keyword found, skipping")
    return None

def tool_text(q, trace):
    log(trace, "TextProcessorTool: Fallback tool activated (no other tools matched)")
    log(trace, "TextProcessorTool: Analyzing query for text processing keywords")

    if "upper" in q.lower():
        log(trace, "TextProcessorTool: Found 'upper' keyword")
        log(trace, "TextProcessorTool: Applying UPPERCASE transformation")
        result = q.upper()
        log(trace, f"TextProcessorTool: Transformation complete -> {result}")
        return "TextProcessorTool", result
    elif "lower" in q.lower():
        log(trace, "TextProcessorTool: Found 'lower' keyword")
        log(trace, "TextProcessorTool: Applying lowercase transformation")
        result = q.lower()
        log(trace, f"TextProcessorTool: Transformation complete -> {result}")
        return "TextProcessorTool", result
    else:
        log(trace, "TextProcessorTool: No specific keyword found")
        log(trace, "TextProcessorTool: Defaulting to length calculation")
        result = str(len(q))
        log(trace, f"TextProcessorTool: Query length = {result} characters")
        return "TextProcessorTool", result
    

AGENT_TOOLS = [tool_calc, tool_weather, tool_text]