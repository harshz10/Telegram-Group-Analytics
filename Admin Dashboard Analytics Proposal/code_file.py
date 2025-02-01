from textblob import TextBlob
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO

def generate_plot(plot_func):
    """Helper function to generate plot image"""
    buf = BytesIO()
    plot_func()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
# ------------------------- Metric Functions -------------------------

def calculate_daily_active_users(message_info):
    # Calculate daily unique senders
    message_info['date'] = pd.to_datetime(message_info['timestamp']).dt.date
    daily_users = message_info.groupby('date')['sender_id'].nunique().reset_index()
    daily_users.columns = ['date', 'active_users']
    
    return daily_users

def plot_daily_active_users(daily_users):
    def plot():
        plt.figure(figsize=(12, 6))
        plt.bar(daily_users['date'].astype(str), daily_users['active_users'], color='green')
        plt.xlabel('Date')
        plt.ylabel('Active Users')
        plt.title('Daily Active Users')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
    return generate_plot(plot)

def calculate_weekly_new_members(member_info):
    # Convert join_date to weekly periods
    member_info['join_week'] = pd.to_datetime(member_info['join_date']).dt.to_period('W')
    
    # Group by week and count new members
    weekly_members = member_info.groupby('join_week').size().reset_index(name='new_members')
    
    # Convert Period objects to actual dates
    weekly_members['week_start'] = weekly_members['join_week'].apply(lambda x: x.start_time.date())
    
    return weekly_members[['week_start', 'new_members']]
##2
def plot_weekly_new_members(weekly_members):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.bar(weekly_members['week_start'].astype(str), 
                      weekly_members['new_members'],
                      color='orange')
        plt.title('Weekly New Members')
        plt.xlabel('Week Start Date')
        plt.ylabel('New Members')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
    
    return generate_plot(plot)                                                    # 3. Monthly Member Retention Rate
def calculate_monthly_retention(member_info, message_info):
    # Convert dates to monthly periods
    member_info['join_month'] = pd.to_datetime(member_info['join_date']).dt.to_period('M')
    message_info['message_month'] = pd.to_datetime(message_info['timestamp']).dt.to_period('M')
    
    # Find active users each month
    active_users = message_info.groupby('message_month')['sender_id'].nunique().reset_index()
    active_users.columns = ['month', 'active_users']
    
    # Calculate retention
    retention_data = []
    for month in member_info['join_month'].unique():
        cohort = member_info[member_info['join_month'] == month]
        next_month = month + 1
        retained = message_info[message_info['message_month'] == next_month]['sender_id'].nunique()
        retention_pct = (retained / len(cohort)) * 100 if len(cohort) > 0 else 0
        retention_data.append({
            'join_month': month.strftime('%Y-%m'),
            'retention_rate': round(retention_pct, 2)
        })
    
    return pd.DataFrame(retention_data)

def plot_monthly_retention(retention_data):
    def plot():
        plt.figure(figsize=(12, 6))
        plt.plot(retention_data['join_month'], retention_data['retention_rate'], 
                marker='o', linestyle='-', color='purple')
        plt.title('Monthly Member Retention Rate')
        plt.xlabel('Join Month')
        plt.ylabel('Retention Rate (%)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.ylim(0, 100)
    return generate_plot(plot)

# 4. Average Messages Per User
def calculate_avg_messages_per_user(message_info):
    user_messages = message_info.groupby('sender_id')['message_id'].count().reset_index()
    avg_messages = user_messages['message_id'].mean()
    return pd.DataFrame({'metric': ['Average Messages Per User'], 'value': [round(avg_messages, 2)]})

def plot_avg_messages_per_user(avg_data):
    def plot():
        plt.figure(figsize=(8, 6))
        plt.bar(avg_data['metric'], avg_data['value'], color='teal')
        plt.title('Average Messages Per User')
        plt.ylabel('Message Count')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
    return generate_plot(plot)

    # 5. Most Active Members
def calculate_most_active_members(message_info, member_info, top_n=10):
    # Count messages per user
    active_members = message_info.groupby('sender_id')['message_id'] \
                               .count() \
                               .reset_index(name='message_count') \
                               .sort_values('message_count', ascending=False) \
                               .head(top_n)
    
    # Merge with member info
    active_members = active_members.merge(
        member_info[['user_id', 'username']],
        left_on='sender_id',
        right_on='user_id'
    ).drop('user_id', axis=1)
    
    return active_members[['username', 'message_count']]

def plot_most_active_members(active_members):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.barh(active_members['username'], 
                       active_members['message_count'],
                       color='darkblue')
        plt.title('Most Active Members')
        plt.xlabel('Message Count')
        plt.ylabel('Username')
        plt.gca().invert_yaxis()
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}',
                    va='center')
    return generate_plot(plot)

# 6. Group Engagement Score
def calculate_group_engagement_score(message_info):
    engagement = message_info.groupby('group_id').agg(
        total_messages=('message_id', 'count'),
        total_replies=('replies', 'sum'),
        total_views=('views', 'sum')
    ).reset_index()
    
    # Calculate weighted score
    engagement['engagement_score'] = (
        engagement['total_messages'] * 0.5 +
        engagement['total_replies'] * 0.3 +
        engagement['total_views'] * 0.2
    )
    
    return engagement[['group_id', 'engagement_score']]

def plot_group_engagement_score(engagement_data):
    def plot():
        plt.figure(figsize=(12, 6))
        engagement_sorted = engagement_data.sort_values('engagement_score', ascending=False)
        bars = plt.bar(engagement_sorted['group_id'].astype(str), 
                      engagement_sorted['engagement_score'],
                      color='darkorange')
        plt.title('Group Engagement Score')
        plt.xlabel('Group ID')
        plt.ylabel('Engagement Score')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')
    return generate_plot(plot)

# 7. Bot Activity Report
def calculate_bot_activity_report(member_info, message_info):
    # Get bot users
    bots = member_info[member_info['is_bot'] == True]['user_id']
    
    # Filter bot messages
    bot_activity = message_info[message_info['sender_id'].isin(bots)] \
        .groupby('sender_id') \
        .agg(
            message_count=('message_id', 'count'),
            text_messages=('message_type', lambda x: (x == 'text').sum()),
            media_messages=('message_type', lambda x: (x == 'media').sum())
        ).reset_index()
    
    # Merge with member info
    bot_report = bot_activity.merge(
        member_info[['user_id', 'username', 'role']],
        left_on='sender_id',
        right_on='user_id'
    ).drop('user_id', axis=1)
    
    return bot_report

def plot_bot_activity_report(bot_data):
    def plot():
        plt.figure(figsize=(12, 6))
        
        # Pie chart for message types
        plt.subplot(1, 2, 1)
        total_text = bot_data['text_messages'].sum()
        total_media = bot_data['media_messages'].sum()
        plt.pie([total_text, total_media], 
               labels=['Text Messages', 'Media Messages'],
               autopct='%1.1f%%',
               colors=['lightblue', 'lightgreen'])
        plt.title('Bot Message Types')
        
        # Bar chart for top bots
        plt.subplot(1, 2, 2)
        top_bots = bot_data.sort_values('message_count', ascending=False).head(5)
        bars = plt.barh(top_bots['username'], top_bots['message_count'], color='salmon')
        plt.title('Top Active Bots')
        plt.xlabel('Message Count')
        plt.tight_layout()
        
    return generate_plot(plot)

    # 8. Most Shared URLs
def calculate_most_shared_urls(message_info, top_n=10):
    # Extract and count URLs
    url_counts = message_info['urls'].explode().value_counts().reset_index()
    url_counts.columns = ['url', 'count']
    return url_counts.head(top_n)

def plot_most_shared_urls(url_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.barh(url_data['url'], url_data['count'], color='royalblue')
        plt.title('Most Shared URLs')
        plt.xlabel('Share Count')
        plt.ylabel('URL')
        plt.gca().invert_yaxis()
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', va='center')
    return generate_plot(plot)

# 9. Top Hashtags Used
def calculate_top_hashtags(message_info, top_n=10):
    # Extract and count hashtags
    hashtags = message_info['hashtags'].explode().str.lower().value_counts().reset_index()
    hashtags.columns = ['hashtag', 'count']
    return hashtags.head(top_n)

def plot_top_hashtags(hashtag_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.barh(hashtag_data['hashtag'], hashtag_data['count'], color='darkgreen')
        plt.title('Top Hashtags')
        plt.xlabel('Usage Count')
        plt.ylabel('Hashtag')
        plt.gca().invert_yaxis()
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', va='center')
    return generate_plot(plot)

# 10. Most Popular Message Types
def calculate_message_types(message_info):
    type_counts = message_info['message_type'].value_counts().reset_index()
    type_counts.columns = ['message_type', 'count']
    type_counts['percentage'] = (type_counts['count'] / type_counts['count'].sum()) * 100
    return type_counts

def plot_message_types(type_data):
    def plot():
        plt.figure(figsize=(12, 6))
        plt.pie(type_data['count'], 
               labels=type_data['message_type'],
               autopct='%1.1f%%',
               colors=['gold', 'lightcoral', 'lightskyblue'])
        plt.title('Message Type Distribution')
    return generate_plot(plot)

# 11. Peak Activity Hours
def calculate_peak_hours(message_info):
    message_info['hour'] = pd.to_datetime(message_info['timestamp']).dt.hour
    hour_counts = message_info['hour'].value_counts().reset_index()
    hour_counts.columns = ['hour', 'count']
    return hour_counts.sort_values('hour')

def plot_peak_hours(hour_data):
    def plot():
        plt.figure(figsize=(12, 6))
        plt.plot(hour_data['hour'], hour_data['count'], 
                marker='o', linestyle='-', color='darkviolet')
        plt.title('Message Activity by Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Message Count')
        plt.xticks(range(0, 24))
        plt.grid(True)
        plt.xlim(0, 23)
    return generate_plot(plot)

# 12. Message Sentiment Analysis
from textblob import TextBlob

def analyze_sentiment(text):
    if pd.isna(text) or text.strip() == '':
        return 'neutral'
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.1:
        return 'positive'
    elif analysis.sentiment.polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'

def calculate_sentiment_analysis(message_info):
    sentiments = message_info['text'].apply(analyze_sentiment).value_counts().reset_index()
    sentiments.columns = ['sentiment', 'count']
    sentiments['percentage'] = (sentiments['count'] / sentiments['count'].sum()) * 100
    return sentiments

def plot_sentiment_analysis(sentiment_data):
    def plot():
        plt.figure(figsize=(12, 6))
        
        # Pie chart
        plt.subplot(1, 2, 1)
        plt.pie(sentiment_data['count'], 
               labels=sentiment_data['sentiment'],
               autopct='%1.1f%%',
               colors=['#4CAF50', '#FFC107', '#F44336'])
        plt.title('Sentiment Distribution')
        
        # Bar chart
        plt.subplot(1, 2, 2)
        bars = plt.bar(sentiment_data['sentiment'], sentiment_data['count'], 
                      color=['#4CAF50', '#FFC107', '#F44336'])
        plt.title('Sentiment Counts')
        plt.ylabel('Message Count')
        
        plt.tight_layout()
    return generate_plot(plot)

    # 13. Group Growth Rate
def calculate_group_growth(member_info, period='M'):
    # Convert join dates to periods
    member_info['join_period'] = pd.to_datetime(member_info['join_date']).dt.to_period(period)
    
    # Calculate growth per group
    growth_data = member_info.groupby(['group_id', 'join_period']) \
                           .size() \
                           .groupby(level=0) \
                           .cumsum() \
                           .reset_index(name='member_count')
    
    growth_data['period'] = growth_data['join_period'].dt.to_timestamp()
    return growth_data[['group_id', 'period', 'member_count']]

def plot_group_growth(growth_data):
    def plot():
        plt.figure(figsize=(12, 6))
        for group in growth_data['group_id'].unique():
            group_data = growth_data[growth_data['group_id'] == group]
            plt.plot(group_data['period'], group_data['member_count'], 
                    marker='o', label=f'Group {group}')
        plt.title('Group Growth Over Time')
        plt.xlabel('Time Period')
        plt.ylabel('Member Count')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
    return generate_plot(plot)

# 14. User Churn Rate
def calculate_churn_rate(member_info, message_info, period='M'):
    # Get last activity per user
    last_activity = message_info.groupby('sender_id')['timestamp'].max().reset_index()
    last_activity['last_active'] = pd.to_datetime(last_activity['timestamp']).dt.to_period(period)
    
    # Merge with join data
    merged = member_info.merge(last_activity, left_on='user_id', right_on='sender_id')
    merged['join_period'] = pd.to_datetime(merged['join_date']).dt.to_period(period)
    
    # Calculate churn
    current_period = pd.Period.now(freq=period)
    merged['churned'] = merged['last_active'] < (current_period - 1)
    churn_rate = merged.groupby('join_period')['churned'].mean().reset_index()
    churn_rate['churn_rate'] = churn_rate['churned'] * 100
    return churn_rate[['join_period', 'churn_rate']]

def plot_churn_rate(churn_data):
    def plot():
        plt.figure(figsize=(12, 6))
        plt.bar(churn_data['join_period'].astype(str), 
               churn_data['churn_rate'], 
               color='darkred')
        plt.title('Monthly User Churn Rate')
        plt.xlabel('Join Period')
        plt.ylabel('Churn Rate (%)')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
    return generate_plot(plot)

# 15. Admin Actions Log
def calculate_admin_actions(group_info, member_info):
    # Get admin users
    admins = member_info[member_info['role'] == 'admin']
    
    # Count pinned messages per admin
    admin_actions = group_info.explode('pinned_messages') \
                            .groupby('group_id')['pinned_messages'].count().reset_index()
    admin_actions.columns = ['group_id', 'pinned_actions']
    
    # Merge with admin info
    return admin_actions.merge(admins, on='group_id')[['group_id', 'username', 'pinned_actions']]

def plot_admin_actions(admin_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.bar(admin_data['username'], admin_data['pinned_actions'], color='purple')
        plt.title('Admin Pinned Actions')
        plt.xlabel('Admin Username')
        plt.ylabel('Pinned Messages')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
    return generate_plot(plot)

# 16. Message Forwarding Trends
def calculate_forwarding_trends(message_info, top_n=10):
    forwarded = message_info.sort_values('forwards', ascending=False) \
                          .head(top_n)[['message_id', 'text', 'forwards']]
    forwarded['text_preview'] = forwarded['text'].str[:50] + '...'
    return forwarded[['message_id', 'text_preview', 'forwards']]

def plot_forwarding_trends(forward_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.barh(forward_data['text_preview'], 
                       forward_data['forwards'], 
                       color='darkorange')
        plt.title('Most Forwarded Messages')
        plt.xlabel('Forward Count')
        plt.ylabel('Message Preview')
        plt.gca().invert_yaxis()
        plt.grid(axis='x')
    return generate_plot(plot)

# 17. Member Join/Leave Patterns
def calculate_join_leave_patterns(member_info, message_info):
    # Join patterns
    patterns = member_info.copy()
    patterns['join_hour'] = pd.to_datetime(patterns['join_date']).dt.hour
    
    # Leave patterns (approximated by last activity)
    last_activity = message_info.groupby('sender_id')['timestamp'].max().reset_index()
    last_activity['leave_hour'] = pd.to_datetime(last_activity['timestamp']).dt.hour
    patterns = patterns.merge(last_activity, left_on='user_id', right_on='sender_id')
    
    return patterns[['join_hour', 'leave_hour']]

def plot_join_leave_patterns(pattern_data):
    def plot():
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        join_counts = pattern_data['join_hour'].value_counts().sort_index()
        plt.bar(join_counts.index, join_counts.values, color='green')
        plt.title('Join Time Distribution')
        plt.xlabel('Hour of Day')
        plt.ylabel('Joins')
        
        plt.subplot(1, 2, 2)
        leave_counts = pattern_data['leave_hour'].value_counts().sort_index()
        plt.bar(leave_counts.index, leave_counts.values, color='red')
        plt.title('Leave Time Distribution')
        plt.xlabel('Hour of Day')
        
        plt.tight_layout()
    return generate_plot(plot)
 
 # 18. Inactive Members Count
def calculate_inactive_members(member_info, message_info, days_threshold=30):
    # Get last activity per user
    last_activity = message_info.groupby('sender_id')['timestamp'].max().reset_index()
    last_activity['last_active'] = pd.to_datetime(last_activity['timestamp'])
    
    # Merge with member info
    merged = member_info.merge(last_activity, left_on='user_id', right_on='sender_id')
    
    # Calculate inactivity days
    current_date = pd.to_datetime('now')
    merged['inactive_days'] = (current_date - merged['last_active']).dt.days
    inactive = merged[merged['inactive_days'] > days_threshold]
    
    return inactive[['user_id', 'username', 'inactive_days']]

def plot_inactive_members(inactive_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.barh(inactive_data['username'], 
                       inactive_data['inactive_days'], 
                       color='darkred')
        plt.title(f'Inactive Members (>30 Days)')
        plt.xlabel('Days Inactive')
        plt.ylabel('Username')
        plt.gca().invert_yaxis()
        plt.grid(axis='x')
    return generate_plot(plot)

# 19. Media Content Analysis
def calculate_media_types(message_info):
    media_messages = message_info[message_info['message_type'] == 'media']
    
    # Simple type detection from media links
    media_messages['media_type'] = media_messages['media_links'].apply(
        lambda x: 'image' if any(ext in str(x) for ext in ['.jpg', '.png']) else 
                  'video' if any(ext in str(x) for ext in ['.mp4', '.mov']) else 
                  'file'
    )
    
    type_counts = media_messages['media_type'].value_counts().reset_index()
    type_counts.columns = ['media_type', 'count']
    return type_counts

def plot_media_types(media_data):
    def plot():
        plt.figure(figsize=(12, 6))
        plt.pie(media_data['count'], 
               labels=media_data['media_type'],
               autopct='%1.1f%%',
               colors=['gold', 'lightcoral', 'lightskyblue'])
        plt.title('Media Type Distribution')
    return generate_plot(plot)

# 20. Group Comparison Metrics
def calculate_group_comparison(group_metrics):
    """
    Calculate comparison metrics for different groups
    
    Args:
        group_metrics (pd.DataFrame): DataFrame containing group metrics including
            group_id, activity_score, member_count, and total_messages
    
    Returns:
        pd.DataFrame: Aggregated comparison metrics by group
    """
    comparison = group_metrics.groupby('group_id').agg({
        'activity_score': 'mean',
        'member_count': 'max',
        'total_messages': 'sum'
    }).reset_index()
    return comparison

def calculate_activity_scores(message_info, member_info):
    """
    Calculate activity scores based on message and member information
    
    Args:
        message_info (pd.DataFrame): DataFrame containing message data
        member_info (pd.DataFrame): DataFrame containing member data
    
    Returns:
        pd.Series: Activity scores by group
    """
    # Add your activity score calculation logic here
    # This is a placeholder - modify according to your scoring criteria
    messages_per_group = message_info.groupby('group_id').size()
    members_per_group = member_info.groupby('group_id').size()
    return messages_per_group / members_per_group

def plot_group_comparison(comparison_data):
    """
    Create a plot comparing group metrics
    
    Args:
        comparison_data (pd.DataFrame): DataFrame containing comparison metrics
    
    Returns:
        str: Base64 encoded string of the plot
    """
    def plot():
        plt.figure(figsize=(12, 6))
        comparison_data.plot(x='group_id', 
                           y=['activity_score', 'total_messages'], 
                           kind='bar', 
                           secondary_y='member_count')
        plt.title('Group Comparison Metrics')
        plt.xlabel('Group ID')
        plt.ylabel('Scores')
        plt.grid(True)
    return generate_plot(plot)
# 21. New Groups Created
def calculate_new_groups(member_info, period='M'):
    # Infer group creation date as first member join date
    group_creation = member_info.groupby('group_id')['join_date'].min().reset_index()
    group_creation['creation_period'] = pd.to_datetime(group_creation['join_date']).dt.to_period(period)
    
    new_groups = group_creation.groupby('creation_period').size().reset_index(name='new_groups')
    new_groups['period'] = new_groups['creation_period'].dt.to_timestamp()
    return new_groups[['period', 'new_groups']]

def plot_new_groups(new_groups_data):
    def plot():
        plt.figure(figsize=(12, 6))
        plt.plot(new_groups_data['period'], new_groups_data['new_groups'], 
                marker='o', linestyle='-')
        plt.title('New Groups Created')
        plt.xlabel('Period')
        plt.ylabel('Number of Groups')
        plt.grid(True)
    return generate_plot(plot)

# 22. Pinned Message Interactions
def calculate_pinned_interactions(group_info, message_info):
    # Get pinned message timestamps
    pinned = group_info[['group_id', 'pinned_messages_timestamp']]
    pinned['pinned_date'] = pd.to_datetime(pinned['pinned_messages_timestamp'])
    
    # Merge with messages
    messages = message_info.copy()
    messages['message_date'] = pd.to_datetime(messages['timestamp'])
    
    merged = messages.merge(pinned, on='group_id')
    merged['time_diff'] = (merged['message_date'] - merged['pinned_date']).abs()
    
    # Get messages within 1 day of pinning
    pinned_interactions = merged[merged['time_diff'] < pd.Timedelta(days=1)] \
        .groupby('group_id') \
        .agg(total_views=('views', 'sum'),
             total_replies=('replies', 'sum')) \
        .reset_index()
    
    return pinned_interactions

def plot_pinned_interactions(interaction_data):
    def plot():
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.bar(interaction_data['group_id'], interaction_data['total_views'])
        plt.title('Pinned Message Views')
        
        plt.subplot(1, 2, 2)
        plt.bar(interaction_data['group_id'], interaction_data['total_replies'])
        plt.title('Pinned Message Replies')
        
        plt.tight_layout()
    return generate_plot(plot)

    # 23. Response Time Analysis
def calculate_response_times(message_info):
    # Ensure the timestamp is in datetime format
    message_info['timestamp'] = pd.to_datetime(message_info['timestamp'], errors='coerce')
    
    # Sort messages by group and timestamp
    sorted_msgs = message_info.sort_values(['group_id', 'timestamp'])
    
    # Calculate time differences between consecutive messages
    sorted_msgs['response_time'] = sorted_msgs.groupby('group_id')['timestamp'].diff()
    
    # Convert to seconds and filter same-user responses
    response_times = sorted_msgs[sorted_msgs['sender_id'] != sorted_msgs['sender_id'].shift()] \
        .dropna(subset=['response_time']) \
        .groupby('group_id')['response_time'] \
        .apply(lambda x: x.dt.total_seconds().mean()) \
        .reset_index(name='avg_response_sec')
    
    return response_times
def plot_response_times(response_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.bar(response_data['group_id'].astype(str), 
                      response_data['avg_response_sec'],
                      color='darkblue')
        plt.title('Average Response Times per Group')
        plt.xlabel('Group ID')
        plt.ylabel('Seconds')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
    return generate_plot(plot) 

# 24. Admin-to-Member Ratio
def calculate_admin_ratio(member_info):
    # Count the number of 'admin' and 'member' roles per group
    role_counts = member_info.groupby(['group_id', 'role']).size().unstack(fill_value=0)
    
    # Calculate the admin-to-member ratio for each group
    role_counts['admin_ratio'] = role_counts.get('admin', 0) / role_counts.get('member', 1)
    
    # Return the group_id and admin_ratio columns
    return role_counts.reset_index()[['group_id', 'admin_ratio']]


def plot_admin_ratio(ratio_data):
    def plot():
        # Ensure no NaN or infinite values in ratio_data before plotting
        ratio_data = ratio_data.dropna(subset=['admin_ratio'])

        # Check if the data is not empty
        if ratio_data.empty:
            print("No data available for plotting.")
            return None
        
        # Plot pie chart
        plt.figure(figsize=(12, 6))
        plt.pie(ratio_data['admin_ratio'], 
                labels=ratio_data['group_id'],
                autopct='%1.1f%%',
                startangle=90)
        plt.title('Admin-to-Member Ratio')

        # Save the plot to a BytesIO object
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        img_str = base64.b64encode(img_buf.read()).decode('utf-8')
        plt.close()

        return img_str

    return plot()

# 25. Trending Topics
from textblob import TextBlob

def calculate_trending_topics(message_info, top_n=10):
    # Extract nouns from messages
    messages = message_info['text'].dropna().str.cat(sep=' ')
    blob = TextBlob(messages)
    nouns = [word.lower() for word, tag in blob.tags if tag.startswith('NN')]
    
    # Count and return top topics
    topic_counts = pd.Series(nouns).value_counts().head(top_n).reset_index()
    topic_counts.columns = ['topic', 'count']
    return topic_counts

def plot_trending_topics(topic_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.barh(topic_data['topic'], topic_data['count'], color='darkgreen')
        plt.title('Top Trending Topics')
        plt.xlabel('Mention Count')
        plt.gca().invert_yaxis()
        plt.grid(axis='x')
    return generate_plot(plot)

# 26. Spam Message Detection
SPAM_KEYWORDS = ['free', 'win', 'offer', 'urgent', 'click', 'limited']

def detect_spam_messages(message_info):
    spam_flags = message_info.copy()
    spam_flags['is_spam'] = (
        spam_flags['text'].str.contains('|'.join(SPAM_KEYWORDS), case=False) |
        (spam_flags['urls'].str.len() > 2) |
        (spam_flags['text'].str.len() < 10)
    )
    return spam_flags[spam_flags['is_spam']][['message_id', 'text', 'sender_id']]
    
def plot_spam_messages(spam_data):
    def plot():
        plt.figure(figsize=(12, 6))

        # Aggregate spam messages per sender
        spam_counts = spam_data.groupby('sender_id').size().reset_index(name='spam_count')

        # Ensure proper alignment
        if spam_counts.empty:
            plt.text(0.5, 0.5, "No Spam Messages", ha='center', va='center', fontsize=12)
        else:
            bars = plt.barh(spam_counts['sender_id'].astype(str), spam_counts['spam_count'], color='red')

        plt.title('Spam Messages by Sender')
        plt.xlabel('Spam Message Count')
        plt.ylabel('Sender ID')
        plt.gca().invert_yaxis()
        plt.grid(axis='x')

    return generate_plot(plot)
def plot_spam_messages(spam_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.barh(spam_data['sender_id'].astype(str), spam_data.groupby('sender_id').size(), color='red')
        plt.title('Spam Messages by Sender')
        plt.xlabel('Spam Message Count')
        plt.ylabel('Sender ID')
        plt.gca().invert_yaxis()
        plt.grid(axis='x')
    return generate_plot(plot)

# 27. Most Mentioned Users (Enhanced)
def calculate_most_mentioned_users(message_info, member_info):
    # Extract mentions using @username pattern
    mentions = message_info['text'].str.findall(r'@(\w+)').explode()
    
    # Count valid mentions
    valid_mentions = mentions[mentions.isin(member_info['username'])]
    mention_counts = valid_mentions.value_counts().reset_index()
    mention_counts.columns = ['username', 'mention_count']
    
    return mention_counts.head(10)

def plot_most_mentioned_users(mention_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.barh(mention_data['username'], mention_data['mention_count'], color='purple')
        plt.title('Most Mentioned Users')
        plt.xlabel('Mention Count')
        plt.gca().invert_yaxis()
        plt.grid(axis='x')
    return generate_plot(plot)

# 28. Hashtag Co-occurrence Network
def calculate_hashtag_cooccurrence(message_info, top_n=10):
    # Extract hashtag pairs
    hashtags = message_info['hashtags'].dropna()
    pairs = []
    
    for tag_list in hashtags:
        unique_tags = list(set(tag_list))
        for i in range(len(unique_tags)):
            for j in range(i+1, len(unique_tags)):
                pairs.append(tuple(sorted([unique_tags[i], unique_tags[j]])))
    
    # Count pairs
    pair_counts = pd.Series(pairs).value_counts().head(top_n).reset_index()
    pair_counts.columns = ['hashtag_pair', 'count']
    pair_counts['hashtag_pair'] = pair_counts['hashtag_pair'].apply(lambda x: f"{x[0]} - {x[1]}")
    
    return pair_counts

def plot_hashtag_cooccurrence(pair_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.barh(pair_data['hashtag_pair'], pair_data['count'], color='darkgreen')
        plt.title('Top Hashtag Co-occurrences')
        plt.xlabel('Co-occurrence Count')
        plt.gca().invert_yaxis()
        plt.grid(axis='x')
    return generate_plot(plot)

# 29. Group Sentiment Trends Over Time
def calculate_sentiment_trends(message_info):
    # Add time period and sentiment
    message_info['period'] = pd.to_datetime(message_info['timestamp']).dt.to_period('W')
    message_info['sentiment'] = message_info['text'].apply(analyze_sentiment)
    
    # Convert sentiment to numerical values
    sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    message_info['sentiment_score'] = message_info['sentiment'].map(sentiment_map)
    
    # Calculate weekly average
    trend_data = message_info.groupby('period')['sentiment_score'].mean().reset_index()
    trend_data['period'] = trend_data['period'].dt.start_time
    return trend_data

def plot_sentiment_trends(trend_data):
    def plot():
        plt.figure(figsize=(12, 6))
        plt.plot(trend_data['period'], trend_data['sentiment_score'], 
                marker='o', linestyle='-', color='darkorange')
        plt.title('Sentiment Trend Over Time')
        plt.xlabel('Week')
        plt.ylabel('Average Sentiment Score')
        plt.grid(True)
        plt.axhline(0, color='gray', linestyle='--')
    return generate_plot(plot)

# 30. Message Length Distribution
def calculate_message_lengths(message_info):
    message_info['length'] = message_info['text'].str.len().fillna(0)
    bins = [0, 50, 100, 150, 200, 300, 500, 1000, float('inf')]
    labels = ['0-50', '51-100', '101-150', '151-200', '201-300', '301-500', '501-1000', '1000+']
    
    message_info['length_group'] = pd.cut(message_info['length'], bins=bins, labels=labels)
    length_dist = message_info['length_group'].value_counts().sort_index().reset_index()
    length_dist.columns = ['length_range', 'count']
    
    return length_dist

def plot_message_lengths(length_data):
    def plot():
        plt.figure(figsize=(12, 6))
        bars = plt.bar(length_data['length_range'], length_data['count'], color='teal')
        plt.title('Message Length Distribution')
        plt.xlabel('Character Length Range')
        plt.ylabel('Message Count')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
    return generate_plot(plot)