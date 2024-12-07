import os
import requests
import pandas as pd
import plotly.graph_objects as go
from pandas import DataFrame
from urllib.parse import urlparse


def ensure_env_file():
    """
    Function to ensure the DOTENV file exists. If not, it creates the file and exits the program.
    """
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, "w") as f:
            f.write("# Github API data for requests\n")
            f.write("REPO_OWNER=\n")
            f.write("REPO_NAME=\n")
            f.write("TOKEN=\n")
            f.write("URL=\n")
        print("DOTENV file was created. Please, fill in the necessary details and rerun the program.")
        exit()


def load_env_variables():
    """
    Function to manually load environment variables from the `.env` file.
    :return: Tuple of repository owner, repository name, and API token.
    """
    env_vars = {}
    with open(".env", "r") as env_file:
        for line in env_file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                env_vars[key.strip()] = value.strip()

    _token = env_vars.get("TOKEN")
    owner, name = None, None

    if env_vars.get("URL"):
        try:
            # Extract owner and repo from URL
            parsed_url = urlparse(env_vars["URL"])
            _, owner, name = parsed_url.path.strip("/").split("/")
        except ValueError:
            print("Invalid URL format. Falling back to REPO_OWNER and REPO_NAME.")

    if not owner or not name:
        owner = env_vars.get("REPO_OWNER")
        name = env_vars.get("REPO_NAME")

    if not _token or not owner or not name:
        print("Please ensure 'TOKEN', and either 'URL' or 'REPO_OWNER' and 'REPO_NAME' are filled in the '.env' file.")
        exit()

    return owner, name, _token


def fetch_code_frequency(_owner, _name, _token):
    """
    Fetches code frequency data (additions and deletions) from the GitHub API.
    :param _owner: Owner of the GitHub repository.
    :param _name: Name of the GitHub repository.
    :param _token: GitHub API token.
    :return: JSON response with code frequency data.
    """
    url = f"https://api.github.com/repos/{_owner}/{_name}/stats/code_frequency"
    headers = {"Authorization": f"token {_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_commit_activity(_owner, _name, _token):
    """
    Fetches commit activity data for each contributor from the GitHub API.
    :param _owner: Owner of the GitHub repository.
    :param _name: Name of the GitHub repository.
    :param _token: GitHub API token.
    :return: JSON response with commit activity data.
    """
    url = f"https://api.github.com/repos/{_owner}/{_name}/stats/contributors"
    headers = {"Authorization": f"token {_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def process_data(code_freq, activity):
    """
    Processes the raw data into structured pandas DataFrames for plotting.
    :param code_freq: Raw code frequency data.
    :param activity: Raw commit activity data.
    :return: Tuple of DataFrames for code frequency and commit activity.
    """
    # Process code frequency
    code_dataframe: DataFrame = pd.DataFrame(code_freq, columns=["timestamp", "additions", "deletions"])
    code_dataframe["timestamp"] = pd.to_datetime(code_dataframe["timestamp"], unit="s")
    code_dataframe["deletions"] = -code_dataframe["deletions"].abs()  # Deletions are shown as negative

    # Process commit activity
    contributors_data = []
    for contributor in activity:
        name = contributor["author"]["login"]
        weeks = contributor["weeks"]
        weekly_data = pd.DataFrame(weeks)
        weekly_data["author"] = name
        weekly_data["timestamp"] = pd.to_datetime(weekly_data["w"], unit="s")
        contributors_data.append(weekly_data[["timestamp", "c", "author"]])

    commit_dataframe: DataFrame = pd.concat(contributors_data, ignore_index=True)

    return code_dataframe, commit_dataframe


def plot_data(code_dataframe, commit_dataframe):
    """
    Visualizes code frequency and contributor activity using Plotly.
    :param code_dataframe: DataFrame containing code frequency data.
    :param commit_dataframe: DataFrame containing commit activity data.
    """
    fig = go.Figure()

    # Scale code frequency data for better visualization
    max_commits = commit_dataframe["c"].max() or 1
    scaling_factor = max_commits / max(code_dataframe["additions"].max(), abs(code_dataframe["deletions"].min()))

    # Add code frequency data with filled areas
    fig.add_trace(
        go.Scatter(
            x=code_dataframe["timestamp"],
            y=code_dataframe["additions"] * scaling_factor,
            mode="lines",
            fill="tozeroy",
            line=dict(color="green", width=2),
            name="Additions (scaled)",
            opacity=0.6
        )
    )
    fig.add_trace(
        go.Scatter(
            x=code_dataframe["timestamp"],
            y=code_dataframe["deletions"] * scaling_factor,
            mode="lines",
            fill="tozeroy",
            line=dict(color="red", dash="dot", width=2),
            name="Deletions (scaled)",
            opacity=0.6
        )
    )

    # Add commit activity data for each contributor
    contributors = commit_dataframe["author"].unique()
    for contributor in contributors:
        contributor_data = commit_dataframe[commit_dataframe["author"] == contributor]
        fig.add_trace(
            go.Scatter(
                x=contributor_data["timestamp"],
                y=contributor_data["c"],
                mode="lines+markers",
                line=dict(width=1.5),
                name=f"Commits by: {contributor}"
            )
        )

    # Set layout for dark theme
    fig.update_layout(
        title="Code frequency withing contributor activity",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Changes (additions/deletions scaled)"),
        template="plotly_dark",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=40, b=40),
    )

    fig.show()

    # Raw code frequency graph
    fig_code_freq = go.Figure()
    fig_code_freq.add_trace(
        go.Scatter(
            x=code_dataframe["timestamp"],
            y=code_dataframe["additions"],
            mode="lines",
            line=dict(color="green"),
            name="Additions",
        )
    )
    fig_code_freq.add_trace(
        go.Scatter(
            x=code_dataframe["timestamp"],
            y=code_dataframe["additions"],
            mode="lines",
            fill="tozeroy",
            line=dict(color="green", width=2),
            name="Additions (scaled)",
            opacity=0.6
        )
    )
    fig_code_freq.add_trace(
        go.Scatter(
            x=code_dataframe["timestamp"],
            y=code_dataframe["deletions"] * scaling_factor,
            mode="lines",
            fill="tozeroy",
            line=dict(color="red", dash="dot", width=2),
            name="Deletions (scaled)",
            opacity=0.6
        )
    )
    fig_code_freq.update_layout(
        title="Raw code frequency",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Additions/Deletions"),
        template="plotly_dark",
    )
    fig_code_freq.show()

    # Raw commit activity graph
    fig_commit_activity = go.Figure()
    for contributor in contributors:
        contributor_data = commit_dataframe[commit_dataframe["author"] == contributor]
        fig_commit_activity.add_trace(
            go.Scatter(
                x=contributor_data["timestamp"],
                y=contributor_data["c"],
                mode="lines+markers",
                line=dict(width=1.5),
                name=f"Commits by {contributor}",
            )
        )
    fig_commit_activity.update_layout(
        title="Raw commit activity",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Commits"),
        template="plotly_dark",
    )
    fig_commit_activity.show()


if __name__ == "__main__":
    ensure_env_file()

    repo_owner, repo_name, token = load_env_variables()

    try:
        code_frequency = fetch_code_frequency(repo_owner, repo_name, token)
        commit_activity = fetch_commit_activity(repo_owner, repo_name, token)
        code_df, commit_df = process_data(code_frequency, commit_activity)
        plot_data(code_df, commit_df)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub: {e}")
