import React from 'react';
import { useState, useEffect } from 'react';
import { Container, Title, TextInput, Button, Paper, Group, Stack, Text, Code } from '@mantine/core';
import { IconRobot } from '@tabler/icons-react';


function App() {

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
              placeholder="e.g., 'calc 5 + 10' or 'weather Toronto' or 'upper hello'"
              style={{ flex: 1 }}
            />
            <Button>
              Process
            </Button>
          </Group>
        </Paper>

        
        <Paper withBorder p="md" radius="md" bg="gray.0">
          <Title order={4} mb="md">Logs</Title>
          <Group mt="lg">
            <Text fw={700}>Final Output:</Text>
            <Code color="blue" fz="lg"></Code>
          </Group>
        </Paper>
        
      </Stack>
    </Container>
  );
}

export default App;