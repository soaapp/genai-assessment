from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_calc_tool():
    """Test CalculatorTool"""
    response = client.post("/process", json={"task": "5 + 10"})
    assert response.status_code == 200
    data = response.json()
    assert data["tool"] == "CalculatorTool"
    assert data["output"] == "15"

def test_weather_tool():
    """Test WeatherTool"""
    response = client.post("/process", json={"task": "Weather in Toronto"})
    assert response.status_code == 200
    data = response.json()
    assert data["tool"] == "WeatherTool"
    assert "Toronto" in data["output"]

def test_text_processor_tool_uppercase():
    """Test TextProcessorTool"""
    response = client.post("/process", json={"task": "uppercase hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["tool"] == "TextProcessorTool"
    assert "HELLO" in data["output"]

def test_text_processor_tool_lowercase():
    """Test TextProcessorTool"""
    response = client.post("/process", json={"task": "lowercase WORLD"})
    assert response.status_code == 200
    data = response.json()
    assert data["tool"] == "TextProcessorTool"
    assert "world" in data["output"]

def test_text_processor_tool_total_count():
    """Test TextProcessorTool"""
    response = client.post("/process", json={"task": "Total count of this string"})
    assert response.status_code == 200
    data = response.json()
    assert data["tool"] == "TextProcessorTool"
    assert "26" in data["output"]

def test_history_endpoint():
    """Test that the history is returned as a list"""
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)