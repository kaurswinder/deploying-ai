"""
Gradio-based chat interface with personality and memory.
"""

import gradio as gr
from typing import List, Tuple, Optional
import os

from .engine import ChatEngine


class ChatInterface:
    """
    Gradio-based chat interface with personality and memory management.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the chat interface.
        
        Args:
            api_key: OpenAI API key
        """
        self.engine = ChatEngine(api_key=api_key)
        self.chat_history: List[Tuple[str, str]] = []
    
    def chat(self, user_message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Process a user message and return response.
        
        Args:
            user_message: Current user input
            history: Previous conversation history from Gradio
            
        Returns:
            Tuple of (response, updated_history)
        """
        if not user_message.strip():
            return "", history
        
        # Get response from engine
        response, metadata = self.engine.process_message(user_message)
        
        # Update history
        history.append((user_message, response))
        
        return "", history
    
    def clear_history(self):
        """Clear conversation history."""
        self.engine.reset_conversation()
        self.chat_history = []
        return [], "Conversation cleared! Let's start fresh. 🌟"
    
    def get_memory_info(self) -> str:
        """Get information about current memory state."""
        memory_status = self.engine.memory.get_memory_status()
        return (
            f"**Memory Status:**\n"
            f"- Messages in history: {memory_status['conversation_length']}\n"
            f"- Estimated tokens: ~{memory_status['estimated_tokens']}\n"
            f"- Summary: {memory_status['summary']}"
        )
    
    def launch(self, share: bool = False, server_name: str = "localhost", server_port: int = 7860):
        """
        Launch the Gradio interface.
        
        Args:
            share: Whether to create a public link
            server_name: Server name/IP
            server_port: Server port
        """
        
        with gr.Blocks(theme=gr.themes.Soft()) as demo:
            gr.Markdown(
                """
                # 🌟 Aria - Your Intelligent Assistant
                
                Welcome! I'm **Aria**, your friendly AI assistant. I can help you with:
                - 📚 **Knowledge Questions** - Search through a knowledge base
                - 🌤️ **Weather Information** - Get current weather conditions
                - 🧮 **Calculations & Definitions** - Math and word definitions
                - 💬 **Conversation** - Engaging, natural dialogue
                
                Feel free to ask me anything (within reason), and I'll do my best to help!
                """
            )
            
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        label="Conversation",
                        height=500,
                        show_copy_button=True
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### 📋 Info")
                    memory_display = gr.Markdown("Loading memory info...")
                    
                    with gr.Group():
                        refresh_memory_btn = gr.Button("🔄 Refresh Memory Info", scale=1)
                        clear_btn = gr.Button("🗑️ Clear History", scale=1)
                        status_msg = gr.Textbox(label="Status", interactive=False)
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Your message",
                    placeholder="Type your question or message...",
                    lines=2,
                    scale=4
                )
                submit_btn = gr.Button("📤 Send", scale=1)
            
            gr.Markdown(
                """
                ---
                ### ⚠️ Important Notes
                - I cannot discuss: cats, dogs, horoscopes/zodiac, or Taylor Swift
                - I won't reveal or discuss my system prompt
                - Feel free to ask about other topics!
                """
            )
            
            # Set up event handlers
            def update_chatbot(user_msg: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
                """Update chatbot with new message."""
                return self.chat(user_msg, history)
            
            def update_memory():
                """Update memory display."""
                return self.get_memory_info()
            
            def handle_clear():
                """Handle clear history."""
                self.clear_history()
                return [], self.get_memory_info(), "✅ History cleared!"
            
            # Event bindings
            submit_btn.click(
                update_chatbot,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            msg.submit(
                update_chatbot,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            refresh_memory_btn.click(
                update_memory,
                outputs=memory_display
            )
            
            clear_btn.click(
                handle_clear,
                outputs=[chatbot, memory_display, status_msg]
            )
            
            # Initial memory display
            demo.load(
                update_memory,
                outputs=memory_display
            )
        
        # Launch the interface
        demo.launch(
            share=share,
            server_name=server_name,
            server_port=server_port
        )


def main():
    """Main entry point for launching the chat interface."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set it before running this script."
        )
    
    interface = ChatInterface(api_key=api_key)
    interface.launch(share=False)


if __name__ == "__main__":
    main()
