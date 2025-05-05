# Startup Pitcher Bot

Startup Pitcher Bot is a smart Streamlit application that helps founders craft compelling pitch decks by learning from top real-world examples. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot searches the web for pitch strategies based on your startup profile and generates a tailored, slide-by-slide presentation aligned to your goals.

## Folder Structure

```
Startup-Pitcher-Bot/
├── startup-pitcher-bot.py
├── README.md
└── requirements.txt
```

* **startup-pitcher-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

### 🚀 Startup Preferences Input

Define your startup's name, stage, one-liner, problem, solution, business model, pitch purpose, and desired deck length (1 to 20 slides).

### 🔍 AI-Powered Pitch Research

The `Startup Researcher` agent creates a focused search query using your inputs, runs a live SerpAPI search, and retrieves top pitch examples, market signals, and investor-facing strategies.

### ✨ Tailored Pitch Generation

The `Startup Pitcher` agent transforms the startup summary and web research into a professionally structured pitch deck — in Markdown format — with slides mapped to the length and style you choose.

### 🧾 Slide-by-Slide Output

Your pitch is presented in structured slides with section headings, bullets, and embedded trends from real-world references.

### 💾 Download Option

Easily download your full pitch deck as a `.txt` file for later editing, review, or sharing with your team or investors.

### 🖥️ Clean Streamlit UI

The app uses a responsive, wide-layout interface optimized for clarity, with API key management, form inputs, pitch generation, and preview/download built into a seamless workflow.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Startup-Pitcher-Bot.git
   cd Startup-Pitcher-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run startup-pitcher-bot.py
   ```

2. **In your browser**:

   * Add your OpenAI and SerpAPI keys in the sidebar
   * Fill in your startup details and pitch preferences
   * Click **🎯 Generate Startup Pitch**
   * View your AI-generated deck in a 2-column slide layout
   * Click **📥 Download Pitch Deck** to save it as `.txt`

## Code Overview

* **`render_startup_pitch_requirements()`**
  Captures user-defined startup inputs: problem, solution, business model, market, and pitch goals.

* **`generate_startup_pitch()`**

  * Uses the `Startup Researcher` agent to conduct web searches via SerpAPI
  * Sends findings and preferences to the `Startup Pitcher` agent to generate the pitch

* **`render_pitch_columns()`**
  Neatly arranges pitch slides in two side-by-side columns using Streamlit layout utilities.

* **`main()`**
  Manages the page layout, input flow, API keys, and presentation rendering pipeline.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Make sure your additions are clean, aligned with the app’s purpose, and tested for a smooth user experience.
