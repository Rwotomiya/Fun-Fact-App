import requests
from pywebio.output import put_text, put_button, clear, put_loading, put_markdown, put_scrollable
from pywebio import start_server

# Global variables to keep track of facts history and current index
facts_history = []
current_index = -1

def get_random_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        response.raise_for_status()
        data = response.json()
        return data['text']
    except requests.RequestException as e:
        return f"Failed to retrieve a fact: {e}"

def main():
    put_markdown("# 🎉 Fun Fact Generator 🎉")
    put_markdown("## 🌟 Welcome to Fun Facts! 🌟")
    put_button("🔍 Get a Fun Fact", onclick=lambda: display_fact())
    put_button("📜 View All Facts", onclick=lambda: view_all_facts())

def display_fact():
    global facts_history, current_index
    with put_loading():
        fact = get_random_fact()

    # Add the new fact to the history and update the current index
    if current_index < len(facts_history) - 1:
        facts_history = facts_history[:current_index + 1]
    facts_history.append(fact)
    current_index = len(facts_history) - 1

    clear()
    put_markdown("# 🎉 Fun Fact Generator 🎉")
    put_markdown("## 🌟 Welcome to Fun Facts! 🌟")
    put_markdown(f"### 💡 {fact}")
    put_button("🔍 Get Another Fact", onclick=lambda: display_fact())
    if current_index > 0:
        put_button("⏪ Previous Fact", onclick=lambda: show_previous_fact())
    put_button("📜 View All Facts", onclick=lambda: view_all_facts())

def show_previous_fact():
    global current_index
    if current_index > 0:
        current_index -= 1
        clear()
        put_markdown("# 🎉 Fun Fact Generator 🎉")
        put_markdown("## 🌟 Welcome to Fun Facts! 🌟")
        put_markdown(f"### 💡 {facts_history[current_index]}")
        put_button("🔍 Get Another Fact", onclick=lambda: display_fact())
        if current_index > 0:
            put_button("⏪ Previous Fact", onclick=lambda: show_previous_fact())
        put_button("📜 View All Facts", onclick=lambda: view_all_facts())

def view_all_facts():
    clear()
    put_markdown("# 🎉 Fun Fact Generator 🎉")
    put_markdown("## 🌟 Welcome to Fun Facts! 🌟")
    put_markdown("### 📜 All Viewed Facts")
    if facts_history:
        for i, fact in enumerate(facts_history, start=1):
            put_markdown(f"- {fact}")
    else:
        put_markdown("No facts viewed yet.")
    put_button("🔙 Back to Facts", onclick=lambda: main())

if __name__ == "__main__":
    start_server(main, port=8080, debug=True)
