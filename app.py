import streamlit as st
from graph import run_pipeline

# Streamlit page setup
st.set_page_config(page_title="LinkedIn Post Generator", layout="wide")

st.title(" AI LinkedIn Post Generator")
st.markdown("""
This tool uses **Gemini + LangGraph agents** to research, summarize, and craft a high-quality LinkedIn post from a topic you provide.
""")

# --- Inputs ---
topic = st.text_input("Enter a topic", placeholder="e.g. AI in Healthcare, Cybersecurity trends, Climate Tech innovations")
tone = st.selectbox(" Select Tone", ["professional", "friendly", "inspirational"])
length = st.selectbox(" Select Length", ["short", "medium", "long"])

# --- Run pipeline ---
if st.button(" Generate LinkedIn Post"):
    if not topic:
        st.error(" Please enter a topic before generating the post.")
    else:
        with st.spinner("🧩 Agents collaborating... please wait."):
            try:
                result, mermaid_graph = run_pipeline(topic, tone, length)

                # --- Display results ---
                st.success("✅ Agents have finished their collaboration!")


                with st.expander(" Key Insights (Agent 2: Summarizer)", expanded=True):
                    st.markdown(result.get("summary", "_No summary available._"))

                st.subheader("✍️ Final LinkedIn Post (Agent 3: Writer)")
                st.text_area(
                    "Generated Post:",
                    result.get("post", "_No post generated._"),
                    height=250
                )

               

            except Exception as e:
                st.error(f"❌ An error occurred while generating the post:\n\n{str(e)}")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using LangGraph, Gemini, and Streamlit.")
