from flask import Flask, jsonify, Response

from code_file import (
    calculate_daily_active_users, plot_daily_active_users,
    calculate_weekly_new_members, plot_weekly_new_members,
    calculate_monthly_retention, plot_monthly_retention,
    calculate_avg_messages_per_user, plot_avg_messages_per_user,
    calculate_most_active_members, plot_most_active_members,
    calculate_group_engagement_score, plot_group_engagement_score,
    calculate_bot_activity_report, plot_bot_activity_report,
     calculate_most_shared_urls, plot_most_shared_urls,
    calculate_top_hashtags, plot_top_hashtags,
    calculate_message_types, plot_message_types,
    calculate_peak_hours, plot_peak_hours,
    calculate_sentiment_analysis, plot_sentiment_analysis,
    calculate_group_growth, plot_group_growth,
    calculate_churn_rate, plot_churn_rate,
    calculate_admin_actions, plot_admin_actions,
    calculate_forwarding_trends, plot_forwarding_trends,
    calculate_join_leave_patterns, plot_join_leave_patterns,
    calculate_inactive_members, plot_inactive_members,
    calculate_media_types, plot_media_types,
   calculate_group_comparison,
    plot_group_comparison,
    calculate_new_groups, plot_new_groups,
    calculate_pinned_interactions, plot_pinned_interactions,
    calculate_response_times, plot_response_times,
    calculate_admin_ratio, plot_admin_ratio,
    calculate_trending_topics, plot_trending_topics,
    detect_spam_messages,plot_spam_messages,
    calculate_most_mentioned_users, plot_most_mentioned_users,
    calculate_hashtag_cooccurrence, plot_hashtag_cooccurrence,
    calculate_sentiment_trends, plot_sentiment_trends,
    calculate_message_lengths, plot_message_lengths
)
    

import pandas as pd
import base64
import datetime
app = Flask(__name__)

# Load data
group_info = pd.read_csv("group_info.csv")
member_info = pd.read_csv("member_info.csv")
message_info = pd.read_csv("message_info.csv")

@app.route('/')
def home():
    endpoints = [
        ('/daily_active_users', 'Daily Active Users', 'Number of users active each day.'),
        ('/weekly_new_members', 'Weekly New Members', 'Number of new members joining per week.'),
        ('/monthly_retention', 'Monthly Retention', 'Percentage of users retained over a month.'),
        ('/avg_messages_per_user', 'Average Messages per User', 'Average number of messages sent per user.'),
        ('/most_active_members', 'Most Active Members', 'Top contributors in the group.'),
        ('/group_engagement_score', 'Group Engagement Score', 'Overall engagement score of the group.'),
        ('/bot_activity_report', 'Bot Activity Report', 'Analysis of bot interactions in the group.'),
        ('/most_shared_urls', 'Most Shared URLs', 'Most frequently shared links in the group.'),
        ('/top_hashtags', 'Top Hashtags', 'Most popular hashtags used by members.'),
        ('/message_types', 'Message Types Breakdown', 'Distribution of messages (text, images, videos, etc.).'),
        ('/peak_hours', 'Peak Activity Hours', 'Hours with the highest messaging activity.'),
        ('/sentiment_analysis', 'Sentiment Analysis', 'Overall sentiment of messages sent in the group.'),
        ('/group_growth', 'Group Growth Rate', 'Tracking new members joining over time.'),
        ('/churn_rate', 'Churn Rate', 'Percentage of users leaving the group.'),
        ('/admin_actions', 'Admin Actions Log', 'Tracking actions taken by admins.'),
        ('/forwarding_trends', 'Forwarding Trends', 'Analysis of how often messages are forwarded.'),
        ('/join_leave_patterns', 'Join & Leave Patterns', 'Analysis of member joins and exits.'),
        ('/inactive_members', 'Inactive Members', 'List of members with little to no activity.'),
        ('/media_types', 'Media Types Shared', 'Breakdown of media shared (images, videos, etc.).'),
        ('/group_comparison', 'Group Comparison', 'Comparing activity across multiple groups.'),
        ('/new_groups', 'New Groups Created', 'Tracking the creation of new groups.'),
        ('/pinned_interactions', 'Pinned Messages Interactions', 'Engagement on pinned messages.'),
        ('/response_times', 'Average Response Times', 'Measuring how fast users respond to messages.'),
        ('/admin_ratio', 'Admin-to-Member Ratio', 'Ratio of admins to regular members.'),
        ('/trending_topics', 'Trending Topics', 'Most discussed topics in the group.'),
        ('/spam_messages', 'Spam Messages Detection', 'Detection of spam or unwanted messages.'),
        ('/most_mentioned_users', 'Most Mentioned Users', 'Users mentioned most frequently.'),
        ('/hashtag_cooccurrence', 'Hashtag Co-occurrence', 'Relationships between different hashtags.'),
        ('/sentiment_trends', 'Sentiment Trends Over Time', 'Changes in sentiment over time.'),
        ('/message_lengths', 'Message Length Distribution', 'Analysis of message lengths in the group.')
    ]

    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Dashboard Analytics Proposal</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .header {{ text-align: center; padding: 30px; background-color: #ffffff; margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .container {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
                .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .card-title {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 1.1em; font-weight: 600; }}
                .card-description {{ color: #666; font-size: 0.9em; margin-bottom: 15px; line-height: 1.4; }}
                .links {{ display: flex; gap: 10px; }}
                .link {{ padding: 8px 15px; border-radius: 4px; text-decoration: none; font-size: 0.85em; transition: background-color 0.2s; }}
                .data-link {{ background-color: #3498db; color: white; }}
                .plot-link {{ background-color: #27ae60; color: white; }}
                .link:hover {{ opacity: 0.9; }}
                footer {{ text-align: center; margin-top: 40px; padding: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Admin Dashboard Analytics Proposal</h1>
                <p>Comprehensive group performance metrics</p>
            </div>
            <div class="container">
    """

    for endpoint, title, description in endpoints:
        plot_endpoint = f"/plot{endpoint.replace('/', '_')}"
        html += f"""
            <div class="card">
                <h3 class="card-title">{title}</h3>
                <p class="card-description">{description}</p>
                <div class="links">
                    <a href="{endpoint}" class="link data-link" target="_blank">View Data</a>
                    <a href="{plot_endpoint}" class="link plot-link" target="_blank">View Plot</a>
                </div>
            </div>
        """

    html += f"""
            </div>
            <footer>
                <p>Last updated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} | Total metrics: {len(endpoints)}</p>
            </footer>
        </body>
        </html>
    """
    return html

@app.route('/daily_active_users', methods=['GET'])
def get_daily_active_users():
    result = calculate_daily_active_users(message_info)  # Using imported function
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_daily_active_users', methods=['GET'])
def get_daily_active_users_plot():
    daily_users = calculate_daily_active_users(message_info)
    img_str = plot_daily_active_users(daily_users)  # Using imported plot function
    return Response(base64.b64decode(img_str), mimetype='image/png')

##2
@app.route('/weekly_new_members', methods=['GET'])
def get_weekly_new_members():
    result = calculate_weekly_new_members(member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_weekly_new_members', methods=['GET'])
def get_weekly_new_members_plot():
    weekly_members = calculate_weekly_new_members(member_info)
    img_str = plot_weekly_new_members(weekly_members)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/monthly_retention', methods=['GET'])
def get_monthly_retention():
    result = calculate_monthly_retention(member_info, message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_monthly_retention', methods=['GET'])
def get_monthly_retention_plot():
    retention_data = calculate_monthly_retention(member_info, message_info)
    img_str = plot_monthly_retention(retention_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/avg_messages_per_user', methods=['GET'])
def get_avg_messages_per_user():
    result = calculate_avg_messages_per_user(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_avg_messages_per_user', methods=['GET'])
def get_avg_messages_per_user_plot():
    avg_data = calculate_avg_messages_per_user(message_info)
    img_str = plot_avg_messages_per_user(avg_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
    #5
@app.route('/most_active_members', methods=['GET'])
def get_most_active_members():
    result = calculate_most_active_members(message_info, member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_most_active_members', methods=['GET'])
def get_most_active_members_plot():
    active_members = calculate_most_active_members(message_info, member_info)
    img_str = plot_most_active_members(active_members)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#6
@app.route('/group_engagement_score', methods=['GET'])
def get_group_engagement_score():
    result = calculate_group_engagement_score(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_group_engagement_score', methods=['GET'])
def get_group_engagement_score_plot():
    engagement_data = calculate_group_engagement_score(message_info)
    img_str = plot_group_engagement_score(engagement_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#7
@app.route('/bot_activity_report', methods=['GET'])
def get_bot_activity_report():
    result = calculate_bot_activity_report(member_info, message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_bot_activity_report', methods=['GET'])
def get_bot_activity_report_plot():
    bot_data = calculate_bot_activity_report(member_info, message_info)
    img_str = plot_bot_activity_report(bot_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#8
@app.route('/most_shared_urls', methods=['GET'])
def get_most_shared_urls():
    result = calculate_most_shared_urls(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_most_shared_urls', methods=['GET'])
def get_most_shared_urls_plot():
    url_data = calculate_most_shared_urls(message_info)
    img_str = plot_most_shared_urls(url_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#9
@app.route('/top_hashtags', methods=['GET'])
def get_top_hashtags():
    result = calculate_top_hashtags(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_top_hashtags', methods=['GET'])
def get_top_hashtags_plot():
    hashtag_data = calculate_top_hashtags(message_info)
    img_str = plot_top_hashtags(hashtag_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#10
@app.route('/message_types', methods=['GET'])
def get_message_types():
    result = calculate_message_types(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_message_types', methods=['GET'])
def get_message_types_plot():
    type_data = calculate_message_types(message_info)
    img_str = plot_message_types(type_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#11
@app.route('/peak_hours', methods=['GET'])
def get_peak_hours():
    result = calculate_peak_hours(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_peak_hours', methods=['GET'])
def get_peak_hours_plot():
    hour_data = calculate_peak_hours(message_info)
    img_str = plot_peak_hours(hour_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#12
@app.route('/sentiment_analysis', methods=['GET'])
def get_sentiment_analysis():
    result = calculate_sentiment_analysis(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_sentiment_analysis', methods=['GET'])
def get_sentiment_analysis_plot():
    sentiment_data = calculate_sentiment_analysis(message_info)
    img_str = plot_sentiment_analysis(sentiment_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#13
@app.route('/group_growth', methods=['GET'])
def get_group_growth():
    result = calculate_group_growth(member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_group_growth', methods=['GET'])
def get_group_growth_plot():
    growth_data = calculate_group_growth(member_info)
    img_str = plot_group_growth(growth_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#14
@app.route('/churn_rate', methods=['GET'])
def get_churn_rate():
    result = calculate_churn_rate(member_info, message_info)

    # Convert Period objects to strings
    result = result.astype(str)

    return jsonify(result.to_dict(orient="records"))


@app.route('/plot_churn_rate', methods=['GET'])
def get_churn_rate_plot():
    churn_data = calculate_churn_rate(member_info, message_info)
    img_str = plot_churn_rate(churn_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#15
@app.route('/admin_actions', methods=['GET'])
def get_admin_actions():
    result = calculate_admin_actions(group_info, member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_admin_actions', methods=['GET'])
def get_admin_actions_plot():
    admin_data = calculate_admin_actions(group_info, member_info)
    img_str = plot_admin_actions(admin_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#16
@app.route('/forwarding_trends', methods=['GET'])
def get_forwarding_trends():
    result = calculate_forwarding_trends(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_forwarding_trends', methods=['GET'])
def get_forwarding_trends_plot():
    forward_data = calculate_forwarding_trends(message_info)
    img_str = plot_forwarding_trends(forward_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#17
@app.route('/join_leave_patterns', methods=['GET'])
def get_join_leave_patterns():
    result = calculate_join_leave_patterns(member_info, message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_join_leave_patterns', methods=['GET'])
def get_join_leave_patterns_plot():
    pattern_data = calculate_join_leave_patterns(member_info, message_info)
    img_str = plot_join_leave_patterns(pattern_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#18
@app.route('/inactive_members', methods=['GET'])
def get_inactive_members():
    result = calculate_inactive_members(member_info, message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_inactive_members', methods=['GET'])
def get_inactive_members_plot():
    inactive_data = calculate_inactive_members(member_info, message_info)
    img_str = plot_inactive_members(inactive_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#19
@app.route('/media_types', methods=['GET'])
def get_media_types():
    result = calculate_media_types(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_media_types', methods=['GET'])
def get_media_types_plot():
    media_data = calculate_media_types(message_info)
    img_str = plot_media_types(media_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#20
@app.route('/group_comparison', methods=['GET'])
def get_group_comparison():
    # Combine all the data first
    group_metrics = pd.DataFrame({
        'group_id': group_info['group_id'],
        'member_count': member_info.groupby('group_id').size(),
        'total_messages': message_info.groupby('group_id').size(),
        'activity_score': calculate_activity_scores(message_info, member_info)
    })
    
    # Then pass the combined metrics to calculate_group_comparison
    result = calculate_group_comparison(group_metrics)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_group_comparison', methods=['GET'])
def get_group_comparison_plot():
    # Similar data preparation as above
    group_metrics = pd.DataFrame({
        'group_id': group_info['group_id'],
        'member_count': member_info.groupby('group_id').size(),
        'total_messages': message_info.groupby('group_id').size(),
        'activity_score': calculate_activity_scores(message_info, member_info)
    })



#21
@app.route('/new_groups', methods=['GET'])
def get_new_groups():
    result = calculate_new_groups(member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_new_groups', methods=['GET'])
def get_new_groups_plot():
    new_groups_data = calculate_new_groups(member_info)
    img_str = plot_new_groups(new_groups_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#22
@app.route('/pinned_interactions', methods=['GET'])
def get_pinned_interactions():
    result = calculate_pinned_interactions(group_info, message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_pinned_interactions', methods=['GET'])
def get_pinned_interactions_plot():
    interaction_data = calculate_pinned_interactions(group_info, message_info)
    img_str = plot_pinned_interactions(interaction_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#23
@app.route('/response_times', methods=['GET'])
def get_response_times():
    result = calculate_response_times(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_response_times', methods=['GET'])
def get_response_times_plot():
    response_data = calculate_response_times(message_info)
    img_str = plot_response_times(response_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#24
@app.route('/admin_ratio', methods=['GET'])
def get_admin_ratio():
    result = calculate_admin_ratio(member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_admin_ratio', methods=['GET'])
def get_admin_ratio_plot():
    # Calculate the admin ratio for each group
    ratio_data = calculate_admin_ratio(member_info)

    # Check if there is valid data to plot
    if ratio_data.empty:
        return Response("No data available for the plot", status=400)

    # Generate the plot and convert it to base64 string
    img_str = plot_admin_ratio(ratio_data)
    
    # Check if img_str is None, indicating no plot was generated
    if img_str is None:
        return Response("No data available for the plot", status=400)

    return Response(base64.b64decode(img_str), mimetype='image/png')

#25
@app.route('/trending_topics', methods=['GET'])
def get_trending_topics():
    result = calculate_trending_topics(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_trending_topics', methods=['GET'])
def get_trending_topics_plot():
    topic_data = calculate_trending_topics(message_info)
    img_str = plot_trending_topics(topic_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
#26
@app.route('/spam_messages', methods=['GET'])
def get_spam_messages():
    result = detect_spam_messages(message_info)
    return jsonify(result.to_dict(orient="records"))
@app.route('/plot_spam_messages', methods=['GET'])
def get_spam_messages_plot():
    spam_data = detect_spam_messages(message_info)
    img_str = plot_spam_messages(spam_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')
    #27
@app.route('/most_mentioned_users', methods=['GET'])
def get_most_mentioned_users():
    result = calculate_most_mentioned_users(message_info, member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_most_mentioned_users', methods=['GET'])
def get_most_mentioned_users_plot():
    mention_data = calculate_most_mentioned_users(message_info, member_info)
    img_str = plot_most_mentioned_users(mention_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/hashtag_cooccurrence', methods=['GET'])
def get_hashtag_cooccurrence():
    result = calculate_hashtag_cooccurrence(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_hashtag_cooccurrence', methods=['GET'])
def get_hashtag_cooccurrence_plot():
    pair_data = calculate_hashtag_cooccurrence(message_info)
    img_str = plot_hashtag_cooccurrence(pair_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/sentiment_trends', methods=['GET'])
def get_sentiment_trends():
    result = calculate_sentiment_trends(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_sentiment_trends', methods=['GET'])
def get_sentiment_trends_plot():
    trend_data = calculate_sentiment_trends(message_info)
    img_str = plot_sentiment_trends(trend_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/message_lengths', methods=['GET'])
def get_message_lengths():
    result = calculate_message_lengths(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_message_lengths', methods=['GET'])
def get_message_lengths_plot():
    length_data = calculate_message_lengths(message_info)
    img_str = plot_message_lengths(length_data)
    return Response(base64.b64decode(img_str), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

