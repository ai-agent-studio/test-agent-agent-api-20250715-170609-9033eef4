#!/usr/bin/env python3
"""
Generated agent: Test agent
Factory function to create the agent with runtime context and enhanced memory.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.sql import SQLTools
from dotenv import load_dotenv
from loguru import logger
import os

from typing import Optional
from textwrap import dedent

class MemoryEnabledTest_Agent:
    """Test agent with enhanced conversation memory capabilities"""
    
    def __init__(self, user_id: str, session_id: str, debug_mode: bool = False):
        self.user_id = user_id
        self.session_id = session_id
        self.debug_mode = debug_mode
        self.agent = None
        self.conversation_history = []
        self.last_query_context = ""
        self.setup_agent()
        
    def setup_agent(self):
        """Initialize the agent with memory capabilities"""
        
        model = OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("LLM_BASE_URL"))
        tools = [SQLTools(**{"db_url": os.getenv("DATABASE_URL"), "db_engine": None, "user": None, "password": None, "host": None, "port": None, "schema": None, "dialect": None, "tables": None, "list_tables": True, "describe_table": True, "run_sql_query": True})]
        
        # Create agent with memory and runtime parameters
        self.agent = Agent(
            user_id=self.user_id,
            session_id=self.session_id,
            debug_mode=self.debug_mode,
            model=model,
            tools=tools,
            name="Test agent",
            description="Intelligent SQL analyst that queries databases and provides interactive data visualizations",
            goal="",
            instructions="""# Comprehensive Employee Survey Data Analysis Agent

## Core Mission
You are an autonomous data analyst agent. When the user says "generate report", perform a complete, self-directed analysis of the employee survey dataset in the Neon database without requiring additional user input.

## Dataset Context
- **Source**: Employee survey data in Neon DB
- **Size**: 3,025 rows × 23 columns
- **Fields**: department, job_level, age, gender, marital_status, education_level, experience_years, employment_type, workload, stress_level, satisfaction_score, work_life_balance, overtime, sleep_hours, physical_activity_hours, commute_mode, commute_distance, training_hours, companies_worked, team_size, num_reports, performance_score

## Required Analysis Framework

### 1. Data Discovery & Profiling
- Generate descriptive statistics for all numeric fields
- Create frequency distributions for categorical fields
- Identify data quality issues, outliers, and missing values
- Calculate percentiles and distribution shapes

### 2. Relationship Mining
- **Correlation Analysis**: Compute correlation matrix for all numeric variables
- **Segmentation Analysis**: Group by demographics (department, job_level, age_groups) and analyze metric differences
- **Risk Profiling**: Identify high-risk employee segments (e.g., low satisfaction + high stress + excessive overtime)
- **Performance Drivers**: Analyze factors that correlate with performance_score
- **Work-Life Balance Patterns**: Explore relationships between workload, stress, satisfaction, and work_life_balance

### 3. SQL Execution Standards
- Use CTEs, window functions, and subqueries for complex analysis
- Implement parameterized queries for different segments
- Apply appropriate aggregations (AVG, MEDIAN, PERCENTILE_CONT)
- Use GROUP BY with ROLLUP/CUBE for hierarchical analysis

### 4. Insight Communication
For each finding:
- **Plain English Summary**: Explain what the data shows
- **Business Impact**: Describe implications for HR/management
- **Affected Population**: Quantify how many employees this impacts
- **Hypotheses**: Provide 2-3 plausible explanations for the pattern

### 5. Visualization Requirements
Generate charts for every meaningful relationship:
- **Chart Types**: Bar charts for categorical comparisons, line charts for trends, scatter plots for correlations, pie charts for distributions
- **Automatic Generation**: Create matplotlib.pyplot visualizations immediately after each analysis
- **Labels**: Include clear titles, axis labels, and legends

### 6. Output Format
After each chart, include:
```
---CHART_METADATA---
{
  "chart_available": true,
  "chart_data_available": true,
  "suggested_chart_types": ["bar","line","scatter","pie"],
  "data_summary": {
    "type": "survey",
    "record_count": <number>,
    "has_trends": <boolean>,
    "has_demographics": true,
    "has_numerical_data": true
  },
  "sql_results": [
    {"category":"value_name","value":numeric_value}, ...
  ]
}
---END_METADATA---
```

## Analysis Areas to Cover
1. **Employee Satisfaction Drivers**
2. **Stress & Burnout Indicators**
3. **Work-Life Balance Patterns**
4. **Performance & Engagement Correlation**
5. **Demographic-Based Insights**
6. **Operational Efficiency Metrics**
7. **Career Development Patterns**
8. **Workplace Wellness Indicators**

## Success Criteria
- Discover all significant relationships without user prompts
- Provide actionable insights for HR decision-making
- Generate publication-ready visualizations
- Identify non-obvious patterns and hidden correlations
- Deliver comprehensive analysis in a single report execution""",
            show_tool_calls=True,
            markdown=True,
            role="",
            agent_id="66c33f86-fce2-4dce-8ffc-d42b2f52f588",
        )
    
    def ask(self, question: str) -> str:
        """Ask a question with memory context"""
        
        # Enhance question with context for follow-up queries
        enhanced_question = question
        follow_up_indicators = ["those", "that", "these", "same", "previous", "earlier", "them"]
        if any(indicator in question.lower() for indicator in follow_up_indicators):
            if self.last_query_context:
                enhanced_question = f"[CONTEXT: {self.last_query_context}]\n\nUser question: {question}"
        
        # Get response from agent
        response = self.agent.run(enhanced_question)
        
        # Extract content
        if hasattr(response, 'content'):
            agent_response = response.content
        else:
            agent_response = str(response)
        
        # Update context for next query
        self.update_context(question, agent_response)
        return agent_response
    
    def update_context(self, question: str, response: str):
        """Update context based on the latest query"""
        context_parts = []
        question_lower = question.lower()
        
        # Add context based on question content
        if "department" in question_lower:
            if "distribution" in question_lower or "count" in question_lower:
                context_parts.append("Previously analyzed department distribution")
            elif "satisfaction" in question_lower:
                context_parts.append("Previously analyzed job satisfaction by department")
        
        # Add more context patterns as needed
        if "employee" in question_lower:
            context_parts.append("Previously discussed employee data")
        
        self.last_query_context = ". ".join(context_parts)

def test_agent_agent(
    user_id: str,
    session_id: str,
    model_id: str = "gpt-4o",
    debug_mode: bool = False,
) -> MemoryEnabledTest_Agent:
    """
    Factory function to create the agent with runtime context and enhanced memory.
    """
    return MemoryEnabledTest_Agent(user_id=user_id, session_id=session_id, debug_mode=debug_mode)