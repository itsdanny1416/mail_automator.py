from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas as pd

env = Environment(
    loader=FileSystemLoader("app/email_templates"),
    autoescape=select_autoescape(["html"])
)

def render_email(title: str, df: pd.DataFrame) -> str:
    """Render an email template with a title and a DataFrame as an HTML table."""
    template = env.get_template("email_template.html")
    html_table = df.to_html(index=False, classes="dataframe", border=0)
    return template.render(title=title, table=html_table)