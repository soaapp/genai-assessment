import re, random

def tool_calc(q, trace):
    if match := re.search(r'\d[\d\s\+\-\*\/]*', q):
        expression = match.group(0).strip()
        # Verify prompt has at least one operator
        if len(expression) > 1 and any(op in expression for op in "+-*/"):
            trace.append(f"CalculatorTool: Detected math expression '{expression}'")
            try:
                result = str(eval(expression))
                trace.append(f"CalculatorTool: Successfully evaluated '{expression}' = {result}")
                return "CalculatorTool", result
            except:
                trace.append(f"CalculatorTool: Failed to eval '{expression}'")
                pass
    return None

def tool_weather(q, trace):
    if "weather" in q.lower():
        trace.append("WeatherTool: Detected keyword 'weather'")
        
        # TODO: If the city is still Unknown maybe we can fallback on saying "Unable to get weather"
        city = "Unknown"
        for p in ["in ", "at ", "for "]:
            if p in q:
                city = q.split(p)[1].strip()
                trace.append(f"WeatherTool: Extracted location '{city}'")
                break
        
        # Randomize weather for fun
        conditions = ["Sunny", "Cloudy", "Rainy", "Snowing", "Partly Cloudy"]
        temp = random.randint(-10, 25)
        condition = random.choice(conditions)
        
        result = f"{temp}°C, {condition} in {city.title()}"
        trace.append(f"WeatherTool: Fetched data -> {result}")
        return "WeatherTool", result
    return None

def tool_text(q, trace):
    trace.append("TextProcessorTool: Fallback tool activated")
    
    if "upper" in q.lower():
        trace.append("TextProcessorTool: Logic 'UPPERCASE' selected based on keyword")
        return "TextProcessorTool", q.upper()
    elif "lower" in q.lower():
        trace.append("TextProcessorTool: Logic 'LOWERCASE' selected based on keyword")
        return "TextProcessorTool", q.lower()
    else:
        trace.append("TextProcessorTool: Logic 'Total Length of Prompt' selected")
        return "TextProcessorTool", str(len(q))
    

TOOLS = [tool_calc, tool_weather, tool_text]