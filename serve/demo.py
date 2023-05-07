"""Gradio demo frontend application."""

import gradio as gr

TITLE = """
# Sign language and emotions translation
"""

DESCRIPTION = """
"""

ARTICLE = """
A technology that will give the opportunity for people to communicate easily in their own language between one and other with more privacy and easier access.

Translate not only to understand what someone is saying but to understand what they are expressing thanks to the emotion recognition.
"""


def image_process(image):
    """Process image here."""
    # TODO
    return f"image outputs {id(image)}"


def webcam_process(video):
    """Process video here."""
    # TODO
    return f"video outputs {id(video)}"


image_page = gr.Interface(
    fn=image_process,
    inputs=[
        gr.Image(info="Image"),
    ],
    outputs="text",
    allow_flagging="never",
)

webcam_page = gr.Interface(
    fn=webcam_process,
    inputs=[
        gr.Image(source="webcam", streaming=True),
    ],
    outputs="text",
    allow_flagging="never",
    live=True,
    # batch=True,
    # max_batch_size=4,
)


app = gr.Blocks()
with app:
    with gr.Row():
        gr.Markdown(TITLE)
    with gr.Row():
        gr.Markdown(DESCRIPTION)

    gr.TabbedInterface(
        [image_page, webcam_page],
        ["Process image", "Process webcam"],
    )

    with gr.Row():
        with gr.Accordion("More ..."):
            gr.Markdown(ARTICLE)


if __name__ == "__main__":
    app.launch(
        debug=True,
        share=True,
        show_api=False,
        show_error=True,
        # favicon_path=r"demo.png",
    )
