"""Web application entry point."""

import gradio as gr
from fastapi import FastAPI

import demo

app = FastAPI()


@app.get("/api")
async def api():
    """Public API"""
    return {"message": "Hello World"}


# Mount gradio demo app.
app = gr.mount_gradio_app(app, demo.app, path="/")
