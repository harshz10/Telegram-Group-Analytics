import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Required fix for Flask compatibility
import matplotlib.pyplot as plt
import io
import base64
from urllib.parse import urlparse
import re
from textblob import TextBlob

# Helper function to generate and encode plots
def generate_plot(plot_func, *args):
    plt.figure(figsize=(10, 5))
    plot_func(*args)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

# Group Activity Analysis
def calculate_group_activity_score(group_info, member_info, message_info):
    message_count = message_info.groupby("group_id")["message_id"].count().reset_index(name="total_messages")
    active_members = message_info.groupby("group_id")["sender_id"].nunique().reset_index(name="active_members")

    group_activity = group_info.merge(message_count, on="group_id", how="left").merge(active_members, on="group_id", how="left")
    group_activity["total_messages"].fillna(0, inplace=True)
    group_activity["active_members"].fillna(0, inplace=True)

    group_activity["group_type_weight"] = group_activity["group_type"].apply(lambda x: 1.5 if x == "public" else 1.0)
    group_activity["activity_score"] = (group_activity["total_messages"] * 0.5 + group_activity["active_members"] * 1.0) * group_activity["group_type_weight"]

    return group_activity[["group_id", "activity_score"]]

def plot_group_activity_score(group_activity_scores):
    def plot():
        plt.bar(group_activity_scores["group_id"], group_activity_scores["activity_score"], color="blue")
        plt.xlabel("Group ID")
        plt.ylabel("Activity Score")
        plt.title("Group Activity Score")
        plt.xticks(group_activity_scores["group_id"])
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

# Member Activity Analysis
def calculate_avg_messages_per_user(message_info, member_info):
    message_count = message_info.groupby("group_id")["message_id"].count().reset_index(name="total_messages")
    user_count = member_info.groupby("group_id")["user_id"].nunique().reset_index(name="total_users")

    avg_messages = message_count.merge(user_count, on="group_id", how="left")
    avg_messages["avg_messages_per_user"] = avg_messages["total_messages"] / avg_messages["total_users"]
    avg_messages["avg_messages_per_user"].fillna(0, inplace=True)

    return avg_messages[["group_id", "avg_messages_per_user"]]

def plot_avg_messages_per_user(avg_messages_per_user):
    def plot():
        plt.bar(avg_messages_per_user["group_id"], avg_messages_per_user["avg_messages_per_user"], color="green")
        plt.xlabel("Group ID")
        plt.ylabel("Avg Messages per User")
        plt.title("Average Messages per User in Each Group")
        plt.xticks(avg_messages_per_user["group_id"])
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def calculate_member_growth_rate(member_info):
    member_info["join_date"] = pd.to_datetime(member_info["join_date"])
    member_info["join_month"] = member_info["join_date"].dt.to_period("M")
    
    member_growth = member_info.groupby(["group_id", "join_month"]).size().reset_index(name="new_members")
    cumulative_growth = member_growth.groupby("group_id").apply(
        lambda x: x.sort_values("join_month").assign(cumulative_members=x["new_members"].cumsum())
    )
    cumulative_growth.reset_index(drop=True, inplace=True)
    
    # Convert Period to string
    cumulative_growth["join_month"] = cumulative_growth["join_month"].astype(str)
    
    return cumulative_growth

def plot_member_growth_rate(member_growth):
    def plot():
        for group_id, data in member_growth.groupby("group_id"):
            plt.plot(data["join_month"].astype(str), data["cumulative_members"], marker="o", label=f"Group {group_id}")
        plt.xlabel("Month")
        plt.ylabel("Cumulative Members")
        plt.title("Member Growth Rate Over Time")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def calculate_admin_to_member_ratio(member_info):
    admin_count = member_info[member_info["role"] == "admin"].groupby("group_id")["user_id"].nunique().reset_index(name="admin_count")
    total_members = member_info.groupby("group_id")["user_id"].nunique().reset_index(name="total_members")

    admin_ratio = admin_count.merge(total_members, on="group_id", how="left")
    admin_ratio["admin_to_member_ratio"] = admin_ratio["admin_count"] / admin_ratio["total_members"]
    admin_ratio["admin_to_member_ratio"].fillna(0, inplace=True)

    return admin_ratio

def plot_admin_to_member_ratio(admin_ratio):
    def plot():
        plt.bar(admin_ratio["group_id"], admin_ratio["admin_to_member_ratio"], color="purple")
        plt.xlabel("Group ID")
        plt.ylabel("Admin-to-Member Ratio")
        plt.title("Admin-to-Member Ratio in Groups")
        plt.xticks(admin_ratio["group_id"])
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def calculate_bots_to_human_ratio(member_info):
    bot_count = member_info[member_info["is_bot"] == True].groupby("group_id")["user_id"].count().reset_index(name="bot_count")
    total_members = member_info.groupby("group_id")["user_id"].count().reset_index(name="total_members")

    bot_ratio = bot_count.merge(total_members, on="group_id", how="left")
    bot_ratio["bots_to_human_ratio"] = bot_ratio["bot_count"] / bot_ratio["total_members"]
    bot_ratio["bots_to_human_ratio"].fillna(0, inplace=True)

    return bot_ratio

def plot_bots_to_human_ratio(bot_ratio):
    def plot():
        plt.bar(bot_ratio["group_id"], bot_ratio["bots_to_human_ratio"], color="red")
        plt.xlabel("Group ID")
        plt.ylabel("Bots-to-Human Ratio")
        plt.title("Bots-to-Human Ratio in Groups")
        plt.xticks(bot_ratio["group_id"])
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def identify_most_active_users(message_info):
    active_users = message_info.groupby("sender_id")["message_id"].count().reset_index(name="message_count")
    return active_users.sort_values(by="message_count", ascending=False)

def plot_most_active_users(active_users, top_n=10):
    def plot():
        top_users = active_users.head(top_n)
        plt.bar(top_users["sender_id"], top_users["message_count"], color="blue")
        plt.xlabel("User ID")
        plt.ylabel("Message Count")
        plt.title(f"Top {top_n} Most Active Users")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def count_inactive_members(member_info, message_info, days_threshold=30):
    message_info["timestamp"] = pd.to_datetime(message_info["timestamp"])
    recent_threshold = message_info["timestamp"].max() - pd.Timedelta(days=days_threshold)

    active_users = message_info[message_info["timestamp"] >= recent_threshold]["sender_id"].unique()
    inactive_members = member_info[~member_info["user_id"].isin(active_users)].groupby("group_id")["user_id"].count().reset_index(name="inactive_count")

    return inactive_members

def plot_inactive_members(inactive_members):
    def plot():
        plt.bar(inactive_members["group_id"], inactive_members["inactive_count"], color="gray")
        plt.xlabel("Group ID")
        plt.ylabel("Inactive Members Count")
        plt.title("Inactive Members Count in Groups")
        plt.xticks(inactive_members["group_id"])
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

# Message Content Analysis
def analyze_message_sentiment(message_info):
    # Correct the column name from "message_text" to "text"
    message_info["sentiment_score"] = message_info["text"].apply(
        lambda x: TextBlob(str(x)).sentiment.polarity  # Ensure text is converted to string
    )
    message_info["sentiment_label"] = message_info["sentiment_score"].apply(
        lambda x: "positive" if x > 0 else ("negative" if x < 0 else "neutral")
    )
    sentiment_summary = message_info.groupby(["group_id", "sentiment_label"]).size().unstack(fill_value=0)
    return sentiment_summary

def plot_message_sentiment(sentiment_summary):
    def plot():
        sentiment_summary.plot(kind='bar', stacked=True, colormap='coolwarm')
        plt.xlabel("Group ID")
        plt.ylabel("Message Count")
        plt.title("Message Sentiment Distribution by Group")
        plt.xticks(rotation=45)
        plt.legend(title="Sentiment")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def identify_peak_activity_hours(message_info):
    message_info["timestamp"] = pd.to_datetime(message_info["timestamp"])
    message_info["hour"] = message_info["timestamp"].dt.hour

    peak_hours = message_info.groupby("hour")["message_id"].count().reset_index(name="message_count")
    return peak_hours

def plot_peak_activity_hours(peak_hours):
    def plot():
        plt.plot(peak_hours["hour"], peak_hours["message_count"], marker='o', linestyle='-', color="orange")
        plt.xlabel("Hour of the Day")
        plt.ylabel("Message Count")
        plt.title("Peak Activity Hours")
        plt.xticks(range(24))
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def extract_top_shared_urls(message_info, top_n=10):
    message_info["urls"] = message_info["text"].apply(lambda x: [urlparse(url).netloc for url in x.split() if urlparse(url).scheme])
    url_list = [url for sublist in message_info["urls"] for url in sublist]

    url_counts = pd.Series(url_list).value_counts().reset_index()
    url_counts.columns = ["url", "count"]
    return url_counts.head(top_n)


def plot_top_shared_urls(url_counts):
    def plot():
        plt.barh(url_counts["url"], url_counts["count"], color="green")
        plt.xlabel("Shared Count")
        plt.ylabel("URL")
        plt.title("Top Shared URLs")
        plt.gca().invert_yaxis()
        plt.grid(axis="x", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def extract_most_used_hashtags(message_info):
    message_info["hashtags"] = message_info["text"].apply(lambda x: re.findall(r"#\w+", str(x)))
    hashtag_list = [tag for sublist in message_info["hashtags"] for tag in sublist]

    hashtag_counts = pd.Series(hashtag_list).value_counts().reset_index()
    hashtag_counts.columns = ["hashtag", "count"]
    return hashtag_counts

def plot_most_used_hashtags(hashtag_counts):
    def plot():
        plt.barh(hashtag_counts["hashtag"], hashtag_counts["count"], color="purple")
        plt.xlabel("Usage Count")
        plt.ylabel("Hashtag")
        plt.title("Most Used Hashtags")
        plt.gca().invert_yaxis()
        plt.grid(axis="x", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def calculate_forwarded_messages_ratio(message_info):
    forwarded_counts = message_info.groupby("group_id")["forwards"].sum().reset_index(name="forwarded_count")
    total_messages = message_info.groupby("group_id")["message_id"].count().reset_index(name="total_messages")

    forwarded_ratio = forwarded_counts.merge(total_messages, on="group_id", how="left")
    forwarded_ratio["forwarded_ratio"] = forwarded_ratio["forwarded_count"] / forwarded_ratio["total_messages"]
    forwarded_ratio["forwarded_ratio"].fillna(0, inplace=True)

    return forwarded_ratio

def plot_forwarded_messages_ratio(forwarded_ratio):
    def plot():
        plt.bar(forwarded_ratio["group_id"], forwarded_ratio["forwarded_ratio"], color="orange")
        plt.xlabel("Group ID")
        plt.ylabel("Forwarded Messages Ratio")
        plt.title("Forwarded Messages Ratio in Groups")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def find_most_pinned_topics(group_info):
    pinned_messages = group_info.groupby("group_id")["pinned_messages"].sum().reset_index()
    return pinned_messages.sort_values(by="pinned_messages", ascending=False)

def plot_most_pinned_topics(pinned_messages):
    def plot():
        plt.bar(pinned_messages["group_id"], pinned_messages["pinned_messages"], color="cyan")
        plt.xlabel("Group ID")
        plt.ylabel("Pinned Messages")
        plt.title("Most Pinned Topics in Groups")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def track_daily_messages_sent(message_info):
    message_info["date"] = pd.to_datetime(message_info["timestamp"]).dt.date
    daily_messages = message_info.groupby("date")["message_id"].count().reset_index(name="message_count")
    return daily_messages

def plot_daily_messages_sent(daily_messages):
    def plot():
        plt.plot(daily_messages["date"], daily_messages["message_count"], marker='o', linestyle='-', color="blue")
        plt.xlabel("Date")
        plt.ylabel("Messages Sent")
        plt.title("Daily Messages Sent")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

def measure_message_response_rate(message_info):
    response_counts = message_info.groupby("replies")["message_id"].count().reset_index(name="reply_count")
    return response_counts

def plot_message_response_rate(response_counts):
    def plot():
        plt.hist(response_counts["reply_count"], bins=20, color="green", alpha=0.7)
        plt.xlabel("Replies per Message")
        plt.ylabel("Frequency")
        plt.title("Message Response Rate Distribution")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)

# Group Engagement Analysis
def compare_visibility_impact(group_info, message_info):
    engagement_metrics = message_info.groupby("group_id")["message_id"].count().reset_index(name="message_count")
    visibility_info = group_info[["group_id", "visibility"]]
    visibility_impact = visibility_info.merge(engagement_metrics, on="group_id", how="left")
    return visibility_impact

def plot_visibility_impact(visibility_impact):
    def plot():
        public = visibility_impact[visibility_impact["visibility"] == "public"]["message_count"].sum()
        restricted = visibility_impact[visibility_impact["visibility"] == "restricted"]["message_count"].sum()
        plt.bar(["Public", "Restricted"], [public, restricted], color=["blue", "red"])
        plt.xlabel("Group Type")
        plt.ylabel("Total Messages")
        plt.title("Visibility Impact on Engagement")
    return generate_plot(plot)

def track_admin_engagement(message_info, member_info):
    admins = member_info[member_info["role"] == "admin"]
    admin_messages = message_info[message_info["sender_id"].isin(admins["user_id"])]
    admin_engagement = admin_messages.groupby("group_id")["message_id"].count().reset_index(name="admin_message_count")
    return admin_engagement

def plot_admin_engagement(admin_engagement):
    def plot():
        plt.bar(admin_engagement["group_id"], admin_engagement["admin_message_count"], color="green")
        plt.xlabel("Group ID")
        plt.ylabel("Admin Messages Count")
        plt.title("Admin Engagement Level")
        plt.xticks(rotation=45)
    return generate_plot(plot)

def identify_most_viewed_messages(message_info):
    return message_info.sort_values(by="views", ascending=False)

def plot_most_viewed_messages(most_viewed):
    def plot():
        plt.barh(most_viewed["message_id"].head(10), most_viewed["views"].head(10), color="orange")
        plt.xlabel("Views")
        plt.ylabel("Message ID")
        plt.title("Most Viewed Messages")
        plt.gca().invert_yaxis()
    return generate_plot(plot)

def calculate_media_to_text_ratio(message_info):
    media_messages = message_info[message_info["message_type"].isin(["image", "video"])]
    text_messages = message_info[message_info["message_type"] == "text"]
    media_ratio = media_messages.groupby("group_id")["message_id"].count().reset_index(name="media_count")
    text_ratio = text_messages.groupby("group_id")["message_id"].count().reset_index(name="text_count")
    ratio = media_ratio.merge(text_ratio, on="group_id", how="outer").fillna(0)
    ratio["media_to_text_ratio"] = ratio["media_count"] / ratio["text_count"]
    ratio["media_to_text_ratio"].fillna(0, inplace=True)
    return ratio

def plot_media_to_text_ratio(ratio):
    def plot():
        plt.bar(ratio["group_id"], ratio["media_to_text_ratio"], color="purple")
        plt.xlabel("Group ID")
        plt.ylabel("Media-to-Text Ratio")
        plt.title("Media-to-Text Message Ratio")
        plt.xticks(rotation=45)
    return generate_plot(plot)

def analyze_group_lifespan(message_info):
    # Convert 'timestamp' to datetime explicitly
    message_info["timestamp"] = pd.to_datetime(message_info["timestamp"])
    
    # Extract date (as datetime64, not Python date objects)
    message_info["date"] = message_info["timestamp"].dt.floor('D')  # Keep as datetime64
    
    # Calculate start/end dates per group
    lifespan = message_info.groupby("group_id").agg(
        start_date=("date", "min"),
        end_date=("date", "max")
    )
    
    # Calculate lifespan in days using timedelta
    lifespan["lifespan_days"] = (lifespan["end_date"] - lifespan["start_date"]).dt.days
    
    return lifespan


def plot_group_lifespan(lifespan):
    def plot():
        plt.bar(lifespan.index, lifespan["lifespan_days"], color="purple")
        plt.xlabel("Group ID")
        plt.ylabel("Lifespan (Days)")
        plt.title("Group Lifespan Analysis")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    return generate_plot(plot)