# This file is part of OSMSG (https://github.com/kshitijrajsharma/OSMSG).
# MIT License

# Copyright (c) 2023 Kshitij Raj Sharma

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""OSMSG (OpenStreetMap Stats Generator) - Tweet Generator Module.

This module is deprecated, but part of the code can be used to post stats on
oither platforms, such as Mastodon

This module automated the generation and tweeting of OpenStreetMap (OSM) contribution statistics.
It read a CSV file containing OSM contribution data, generated summary statistics,
and posted them as a tweet (optionally with images and a thread).
It used the Tweepy library for Twitter API interaction and Pandas for data processing.
"""

import argparse
import os

import humanize
import pandas as pd
import tweepy


def main():
    """Main function to post tweets.

    It parses command-line arguments, process OSM contrubtion data and
    post a tweet with statistics and optional images

    Steps:
    1. Parses command-line arguments for output file name, tweet text, mention, and Git commit ID.
    2. Authenticates with the Twitter API using environment variables.
    3. Reads and processes the CSV file containing OSM contribution data.
    4. Generates summary statistics for the tweet and thread.
    5. Uploads images (if available) and posts the tweet and thread.

    Command-line arguments:
        --name (str): Output stat file name. Default: "stats".
        --tweet (str): Main stats name to include in the tweet. Required.
        --mention (str): Twitter ID to mention in the tweet. Provide with @. Default: "".
        --git (str): GitHub commit ID to include in the tweet. Default: "master".
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--name",
        default="stats",
        help="Output stat file name",
    )
    parser.add_argument(
        "--tweet",
        required=True,
        help="Main Stats Name to include in tweet",
    )
    parser.add_argument(
        "--mention",
        default="",
        help="Tweeter id to mention on tweet, Provide with @",
    )

    parser.add_argument(
        "--git",
        default=None,
        help="Github Commit id to include in tweet",
    )

    args = parser.parse_args()

    if not args.git:
        args.git = "master"
    # Authenticate using your API keys and access tokens
    auth = tweepy.OAuthHandler(os.environ["API_KEY"], os.environ["API_KEY_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])

    api = tweepy.API(auth)

    summary_text = ""
    thread_summary = ""
    csv_file = os.path.join(os.getcwd(), f"{args.name}.csv")
    full_path = os.path.abspath(os.path.join(os.getcwd(), csv_file))
    base_dir = os.path.abspath(os.path.dirname(full_path))
    rel_csv_path = os.path.relpath(base_dir, os.getcwd())

    # read the .csv file and store it in a DataFrame
    df = pd.read_csv(csv_file)
    start_date = str(df.iloc[0]["start_date"])
    end_date = str(df.iloc[0]["end_date"])

    created_sum = df["nodes.create"] + df["ways.create"] + df["relations.create"]
    modified_sum = df["nodes.modify"] + df["ways.modify"] + df["relations.modify"]
    deleted_sum = df["nodes.delete"] + df["ways.delete"] + df["relations.delete"]

    # Get the attribute of first row
    summary_text = (
        f"{len(df)} Users made {df['changesets'].sum()} changesets with "
        f"{humanize.intword(df['map_changes'].sum())} map changes."
    )
    thread_summary = (
        f"{humanize.intword(created_sum.sum())} OSM Elements were Created, "
        f"{humanize.intword(modified_sum.sum())} Modified & "
        f"{humanize.intword(deleted_sum.sum())} Deleted. Including "
        f"{humanize.intword(df['building.create'].sum())} buildings & "
        f"{humanize.intword(df['highway.create'].sum())} highways created."
        if "building" in df.columns and "highway" in df.columns
        else f"{humanize.intword(created_sum.sum())} OSM Elements were Created, "
        f"{humanize.intword(modified_sum.sum())} Modified & {humanize.intword(deleted_sum.sum())} "
        f"Deleted. {df.loc[0, 'name']} tops table with "
        f"{humanize.intword(df.loc[0, 'map_changes'])} changes followed by {df.loc[1, 'name']}"
    )

    try:
        api.verify_credentials()
        print("Authentication OK")
    except Exception as e:
        print(f"Error during authentication: {e}")
    media_ids = []
    thread_media_ids = []

    chart_png_files = [f for f in os.listdir(base_dir) if f.endswith(".png")]
    for _i, chart in enumerate(chart_png_files):
        file_path = os.path.join(base_dir, chart)
        chart_media = api.media_upload(file_path)
        if len(media_ids) < 4:
            if "top_users" in chart:
                thread_media_ids.append(chart_media.media_id)
            else:
                media_ids.append(chart_media.media_id)
        else:
            thread_media_ids.append(chart_media.media_id)
    orginal_tweet = api.update_status(
        status=(
            f"{args.tweet} Contributions\n{start_date} to "
            f"{end_date}\n{summary_text}\nFullStats:https://github.com/kshitijrajsharma/OSMSG/blob/{args.git}/{rel_csv_path}"
            f"#gischat #OpenStreetMap {args.mention}"
        ),
        media_ids=media_ids,
    )
    if len(thread_media_ids) > 0:
        api.update_status(
            status=thread_summary,
            in_reply_to_status_id=orginal_tweet.id,
            auto_populate_reply_metadata=True,
            media_ids=thread_media_ids,
        )


if __name__ == "__main__":
    main()
