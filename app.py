from flask import Flask, jsonify, Response
from code_file import (
    calculate_group_activity_score, 
    calculate_avg_messages_per_user, 
    calculate_member_growth_rate, 
    calculate_admin_to_member_ratio, 
    calculate_bots_to_human_ratio, 
    identify_most_active_users, 
    count_inactive_members, 
    analyze_message_sentiment, 
    identify_peak_activity_hours, 
    extract_top_shared_urls, 
    extract_most_used_hashtags, 
    calculate_forwarded_messages_ratio, 
    find_most_pinned_topics, 
    track_daily_messages_sent, 
    measure_message_response_rate, 
    compare_visibility_impact, 
    track_admin_engagement, 
    identify_most_viewed_messages, 
    calculate_media_to_text_ratio, 
    analyze_group_lifespan, 
    plot_group_activity_score, 
    plot_avg_messages_per_user, 
    plot_member_growth_rate, 
    plot_admin_to_member_ratio, 
    plot_bots_to_human_ratio, 
    plot_most_active_users, 
    plot_inactive_members, 
    plot_message_sentiment, 
    plot_peak_activity_hours, 
    plot_top_shared_urls, 
    plot_most_used_hashtags, 
    plot_forwarded_messages_ratio, 
    plot_most_pinned_topics, 
    plot_daily_messages_sent, 
    plot_message_response_rate, 
    plot_visibility_impact, 
    plot_admin_engagement, 
    plot_most_viewed_messages, 
    plot_media_to_text_ratio, 
    plot_group_lifespan
)
import pandas as pd
import base64

app = Flask(__name__)

# Load data
group_info = pd.read_csv("group_info.csv")
member_info = pd.read_csv("member_info.csv")
message_info = pd.read_csv("message_info.csv")


@app.route('/')
def home():
    endpoints = [
        ('/activity_score', 'Group Activity Score'),
        ('/avg_messages', 'Average Messages per User'),
        ('/member_growth_rate', 'Member Growth Rate'),
        ('/admin_to_member_ratio', 'Admin-to-Member Ratio'),
        ('/bots_to_human_ratio', 'Bots-to-Human Ratio'),
        ('/most_active_users', 'Most Active Users'),
        ('/inactive_members', 'Inactive Members'),
        ('/message_sentiment', 'Message Sentiment Analysis'),
        ('/peak_activity_hours', 'Peak Activity Hours'),
        ('/top_shared_urls', 'Top Shared URLs'),
        ('/most_used_hashtags', 'Most Used Hashtags'),
        ('/forwarded_messages_ratio', 'Forwarded Messages Ratio'),
        ('/most_pinned_topics', 'Most Pinned Topics'),
        ('/daily_messages_sent', 'Daily Messages Sent'),
        ('/message_response_rate', 'Message Response Rate'),
        ('/visibility_impact', 'Visibility Impact Analysis'),
        ('/admin_engagement', 'Admin Engagement'),
        ('/most_viewed_messages', 'Most Viewed Messages'),
        ('/media_to_text_ratio', 'Media-to-Text Ratio'),
        ('/group_lifespan', 'Group Lifespan Analysis')
    ]

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title> Analytics Proposal</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            .container { max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            .endpoint { margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #fff; }
            a { color: #3498db; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
            .plot-link { color: #e74c3c; margin-left: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1> Analytics Proposal</h1>
    """

    for endpoint, title in endpoints:
        html += f"""
        <div class="endpoint">
            <strong>{title}:</strong><br>
            <a href="{endpoint}" target="_blank">View JSON Data</a>
            <a class="plot-link" href="/plot{endpoint.replace('/', '_')}" target="_blank">View Plot</a>
        </div>
        """

    html += """
        </div>
    </body>
    </html>
    """
    return html

# Group Activity Analysis
@app.route('/activity_score', methods=['GET'])
def get_activity_score():
    result = calculate_group_activity_score(group_info, member_info, message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_activity_score', methods=['GET'])
def get_activity_score_plot():
    group_activity_scores = calculate_group_activity_score(group_info, member_info, message_info)
    img_str = plot_group_activity_score(group_activity_scores)
    return Response(base64.b64decode(img_str), mimetype='image/png')

# Member Activity Analysis
@app.route('/avg_messages', methods=['GET'])
def get_avg_messages():
    result = calculate_avg_messages_per_user(message_info, member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_avg_messages', methods=['GET'])
def get_avg_messages_plot():
    avg_messages_per_user = calculate_avg_messages_per_user(message_info, member_info)
    img_str = plot_avg_messages_per_user(avg_messages_per_user)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/member_growth_rate', methods=['GET'])
def get_member_growth_rate():
    result = calculate_member_growth_rate(member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_member_growth_rate', methods=['GET'])
def get_member_growth_rate_plot():
    member_growth = calculate_member_growth_rate(member_info)
    img_str = plot_member_growth_rate(member_growth)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/admin_to_member_ratio', methods=['GET'])
def get_admin_to_member_ratio():
    result = calculate_admin_to_member_ratio(member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_admin_to_member_ratio', methods=['GET'])
def get_admin_to_member_ratio_plot():
    admin_ratio = calculate_admin_to_member_ratio(member_info)
    img_str = plot_admin_to_member_ratio(admin_ratio)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/bots_to_human_ratio', methods=['GET'])
def get_bots_to_human_ratio():
    result = calculate_bots_to_human_ratio(member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_bots_to_human_ratio', methods=['GET'])
def get_bots_to_human_ratio_plot():
    bot_ratio = calculate_bots_to_human_ratio(member_info)
    img_str = plot_bots_to_human_ratio(bot_ratio)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/most_active_users', methods=['GET'])
def get_most_active_users():
    result = identify_most_active_users(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_most_active_users', methods=['GET'])
def get_most_active_users_plot():
    active_users = identify_most_active_users(message_info)
    img_str = plot_most_active_users(active_users)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/inactive_members', methods=['GET'])
def get_inactive_members():
    result = count_inactive_members(member_info, message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_inactive_members', methods=['GET'])
def get_inactive_members_plot():
    inactive_members = count_inactive_members(member_info, message_info)
    img_str = plot_inactive_members(inactive_members)
    return Response(base64.b64decode(img_str), mimetype='image/png')

# Message Content Analysis
@app.route('/message_sentiment', methods=['GET'])
def get_message_sentiment():
    result = analyze_message_sentiment(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_message_sentiment', methods=['GET'])
def get_message_sentiment_plot():
    sentiment_summary = analyze_message_sentiment(message_info)
    img_str = plot_message_sentiment(sentiment_summary)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/peak_activity_hours', methods=['GET'])
def get_peak_activity_hours():
    result = identify_peak_activity_hours(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_peak_activity_hours', methods=['GET'])
def get_peak_activity_hours_plot():
    peak_hours = identify_peak_activity_hours(message_info)
    img_str = plot_peak_activity_hours(peak_hours)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/top_shared_urls', methods=['GET'])
def get_top_shared_urls():
    result = extract_top_shared_urls(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_top_shared_urls', methods=['GET'])
def get_top_shared_urls_plot():
    url_counts = extract_top_shared_urls(message_info)
    img_str = plot_top_shared_urls(url_counts)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/most_used_hashtags', methods=['GET'])
def get_most_used_hashtags():
    result = extract_most_used_hashtags(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_most_used_hashtags', methods=['GET'])
def get_most_used_hashtags_plot():
    hashtag_counts = extract_most_used_hashtags(message_info)
    img_str = plot_most_used_hashtags(hashtag_counts)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/forwarded_messages_ratio', methods=['GET'])
def get_forwarded_messages_ratio():
    result = calculate_forwarded_messages_ratio(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_forwarded_messages_ratio', methods=['GET'])
def get_forwarded_messages_ratio_plot():
    forwarded_ratio = calculate_forwarded_messages_ratio(message_info)
    img_str = plot_forwarded_messages_ratio(forwarded_ratio)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/most_pinned_topics', methods=['GET'])
def get_most_pinned_topics():
    result = find_most_pinned_topics(group_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_most_pinned_topics', methods=['GET'])
def get_most_pinned_topics_plot():
    pinned_messages = find_most_pinned_topics(group_info)
    img_str = plot_most_pinned_topics(pinned_messages)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/daily_messages_sent', methods=['GET'])
def get_daily_messages_sent():
    result = track_daily_messages_sent(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_daily_messages_sent', methods=['GET'])
def get_daily_messages_sent_plot():
    daily_messages = track_daily_messages_sent(message_info)
    img_str = plot_daily_messages_sent(daily_messages)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/message_response_rate', methods=['GET'])
def get_message_response_rate():
    result = measure_message_response_rate(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_message_response_rate', methods=['GET'])
def get_message_response_rate_plot():
    response_counts = measure_message_response_rate(message_info)
    img_str = plot_message_response_rate(response_counts)
    return Response(base64.b64decode(img_str), mimetype='image/png')

# Group Engagement Analysis
@app.route('/visibility_impact', methods=['GET'])
def get_visibility_impact():
    result = compare_visibility_impact(group_info, message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_visibility_impact', methods=['GET'])
def get_visibility_impact_plot():
    visibility_impact = compare_visibility_impact(group_info, message_info)
    img_str = plot_visibility_impact(visibility_impact)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/admin_engagement', methods=['GET'])
def get_admin_engagement():
    result = track_admin_engagement(message_info, member_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_admin_engagement', methods=['GET'])
def get_admin_engagement_plot():
    admin_engagement = track_admin_engagement(message_info, member_info)
    img_str = plot_admin_engagement(admin_engagement)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/most_viewed_messages', methods=['GET'])
def get_most_viewed_messages():
    result = identify_most_viewed_messages(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_most_viewed_messages', methods=['GET'])
def get_most_viewed_messages_plot():
    most_viewed = identify_most_viewed_messages(message_info)
    img_str = plot_most_viewed_messages(most_viewed)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/media_to_text_ratio', methods=['GET'])
def get_media_to_text_ratio():
    result = calculate_media_to_text_ratio(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_media_to_text_ratio', methods=['GET'])
def get_media_to_text_ratio_plot():
    ratio = calculate_media_to_text_ratio(message_info)
    img_str = plot_media_to_text_ratio(ratio)
    return Response(base64.b64decode(img_str), mimetype='image/png')

@app.route('/group_lifespan', methods=['GET'])
def get_group_lifespan():
    result = analyze_group_lifespan(message_info)
    return jsonify(result.to_dict(orient="records"))

@app.route('/plot_group_lifespan', methods=['GET'])
def get_group_lifespan_plot():
    lifespan = analyze_group_lifespan(message_info)
    img_str = plot_group_lifespan(lifespan)
    return Response(base64.b64decode(img_str), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
    
 