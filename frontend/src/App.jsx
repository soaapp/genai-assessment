import React from 'react';
import { useState, useEffect } from 'react';
import { Container, Title, TextInput, Button, Paper, Group, Stack, Text, Code } from '@mantine/core';
import { IconRobot } from '@tabler/icons-react';


function App() {

  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false)

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

        
        <Paper withBorder p="md" radius="md" bg="gray.0">
          <Title order={4} mb="md">Logs</Title>
          <Group mt="lg">
            <Text fw={700}>Final Output:</Text>
            <Code color="blue" fz="lg">
              {result || "Waiting for prompt"}
            </Code>
          </Group>
        </Paper>
        
      </Stack>
    </Container>
  );
}

export default App;