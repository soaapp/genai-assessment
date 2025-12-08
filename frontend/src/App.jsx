import React from 'react';
import { useState, useEffect, useRef } from 'react';
import { Container, Title, TextInput, Button, Paper, Group, Stack, Text, Code, ScrollArea } from '@mantine/core';
import { IconRobot, IconHistory } from '@tabler/icons-react';
import { useDisclosure } from '@mantine/hooks';


function App() {
  // States for main UI components
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);

  // States for history
  const [opened, {open, close}] = useDisclosure(false);
  const [historyItems, setHistoryItems] = useState([]);

  const viewport = useRef(null);

  // Auto-scroll to bottom whenever logs update
  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'smooth' });
    }
  }, [logs]);

  // Function to handle history
  const fetchHistory = async () => {
    try {
      const res = await fetch('http://localhost:3001/history');
      const data = await res.json();
      setHistoryItems(data);
      open();
    } catch (e) {
      console.error("Failed to fetch history from SQLite", e);
    }
  }

  const handleProcess = async () => {
    if (!query) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://localhost:3001/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task: query }),
      });

      if (!response.ok) {
        throw new Error("Unsuccessful network call");
      }

      const data = await response.json();

      setResult(data.output);
      const timestamp = new Date(data.ts).toLocaleTimeString('en-US', {
        hour12: false,
        hour: "numeric", 
        minute: "numeric", 
        second: "numeric"
      });

      const timedLogs = data.steps.map(step => `[${timestamp}] ${step}`);

      setLogs(prev => [
        ...prev, 
        ...timedLogs,
        ""
      ]);

    } catch (error) {
      console.error("Error:", error);
      setResult("Error connecting to backend");
    } finally {
      setLoading(false)
    }
  };

  return (
    <Container size="md" py="xl">
      <Stack gap="lg">
        <Group>
          <IconRobot size={32} color="#228be6" />
          <Title order={2}>Agent</Title>
        </Group>

        <Paper withBorder p="md" shadow="sm" radius="md">
          <Group align="flex-end">
            <TextInput 
              label="Enter a task"
              placeholder="e.g., 'What is 5 + 10' or 'What is the weather in Toronto' or 'hello there'"
              style={{ flex: 1 }}
              value={query}
              onChange={(event) => setQuery(event.currentTarget.value)}
              onKeyDown={(e) => { if (e.key === "Enter") handleProcess() }}
            />
            <Button
              onClick={handleProcess}
              loading={loading}
            >
              Process
            </Button>
          </Group>
        </Paper>

        {result && (
          <Paper withBorder p="md" radius="md" bg="blue.0" style={{ borderColor: '#228be6' }}>
            <Title order={5} c="blue.9" mb="xs">Result</Title>
            <Code block color="blue" fz="lg">{result}</Code>
          </Paper>
        )}

        
        <Paper withBorder p="md" radius="md" bg="gray.0">
          <Group mb="sm">
            <IconHistory size={20} opacity={0.5} />
            <Title order={5}>System Logs</Title>
          </Group>
          
          <ScrollArea h={300} viewportRef={viewport} type="always" offsetScrollbars>
            <Stack gap={4}>
              {logs.length === 0 && <Text c="dimmed" size="sm">Waiting for input...</Text>}
              
              {logs.map((step, index) => (
                <Text key={index} size="xs" style={{ fontFamily: 'monospace' }} c="dimmed">
                  {step}
                </Text>
              ))}
            </Stack>
          </ScrollArea>
        </Paper>
        
      </Stack>
    </Container>
  );
}

export default App;