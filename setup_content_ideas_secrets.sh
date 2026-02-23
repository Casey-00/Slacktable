#!/bin/bash
# Commands to set Fly.io secrets for Content Ideas feature

# Set the Content Ideas Airtable configuration
flyctl secrets set \
  CONTENT_IDEAS_AIRTABLE_BASE_ID="appdj6QIg5WYzQdRX" \
  CONTENT_IDEAS_AIRTABLE_TABLE_NAME="Content" \
  CONTENT_IDEAS_AIRTABLE_FIELD_NAME="Idea" \
  --app slacktable

echo "Content Ideas secrets have been set!"
echo ""
echo "The following emojis are now configured:"
echo "  :content-twitter-article: → Type = Twitter Article"
echo "  :content-twitter-post: → Type = Twitter Post"
echo "  :content-blog-post: → Type = Blog Post"
echo ""
echo "Each will send messages to Airtable with:"
echo "  - Message text in 'Idea' field"
echo "  - Slack permalink in 'Slack Thread' field"
echo "  - Content type in 'Type of Content' field"
echo "  - NO Status field (unlike other emojis)"
