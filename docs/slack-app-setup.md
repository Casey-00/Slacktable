# Slack App Setup Guide

This guide walks you through setting up your Slack app to work with Slacktable.

## Prerequisites

- A Slack workspace where you have permission to install apps
- Admin access to create and configure Slack apps

## Step 1: Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Enter the following details:
   - **App Name**: `Slacktable`
   - **Development Slack Workspace**: Choose your workspace
5. Click **"Create App"**

## Step 2: Configure Basic Information

1. In your app's **Basic Information** page, note down:
   - **App ID** (you'll need this for reference)
   - **Signing Secret** (under App Credentials)

## Step 3: Set Up Bot Token Scopes

1. Navigate to **OAuth & Permissions** in the left sidebar
2. Scroll down to **Scopes** section
3. Under **Bot Token Scopes**, add the following scopes:
   - `channels:history` - Read messages in public channels
   - `groups:history` - Read messages in private channels
   - `im:history` - Read messages in direct messages
   - `mpim:history` - Read messages in group direct messages
   - `reactions:read` - Read emoji reactions
   - `users:read` - Read user information
   - `channels:read` - Read channel information

## Step 4: Install the App to Your Workspace

1. Still in **OAuth & Permissions**, scroll up to the top
2. Click **"Install to Workspace"**
3. Review the permissions and click **"Allow"**
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

## Step 5: Configure App-Level Tokens for Socket Mode

Slacktable uses Socket Mode for real-time event delivery, which requires an App-Level Token:

1. Navigate to **Basic Information**
2. Scroll down to **App-Level Tokens**
3. Click **"Generate Token and Scopes"**
4. Enter a name like `socket-mode-token`
5. Add the scope `connections:write`
6. Click **"Generate"**
7. Copy the token (starts with `xapp-`) - you'll need this for `SLACK_APP_TOKEN`

## Step 6: Enable Socket Mode

1. Navigate to **Socket Mode** in the left sidebar
2. Turn on **Enable Socket Mode**
3. This allows your app to receive events via WebSocket instead of HTTP webhooks

## Step 7: Configure Event Subscriptions

**IMPORTANT**: Even when using Socket Mode, you must enable Event Subscriptions to specify which events your app should receive.

1. Navigate to **Event Subscriptions** in the left sidebar
2. Turn on **Enable Events**
3. **Leave the Request URL field empty** - Socket Mode doesn't use webhooks
4. Under **Subscribe to bot events**, add:
   - `reaction_added`
   - `reaction_removed`
5. Click **"Save Changes"**

**Note**: Socket Mode is the delivery method (WebSocket vs. HTTP), while Event Subscriptions defines which events to send. Both must be enabled.

## Step 8: Install the App in Channels

1. Go to any Slack channel where you want to use the app
2. Type `/invite @Slacktable` to invite the bot
3. The bot will appear in the channel members

## Step 9: Set Environment Variables

In your deployment environment (Fly.io) or local `.env` file, set these environment variables:

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
```

**Note**: Socket Mode doesn't require `SLACK_SIGNING_SECRET` since it uses WebSocket connections instead of HTTP webhooks.

## Step 10: Test the Installation

1. Send a test message in a channel where the bot is installed
2. React to the message with the `:fedex:` emoji
3. Check your Airtable base to see if the record was created
4. Monitor your app logs for any errors

## Troubleshooting

### Common Issues

1. **Events not being received**
   - Verify Socket Mode is enabled in your Slack app settings
   - Check that Event Subscriptions is enabled with `reaction_added` and `reaction_removed` events
   - Ensure the bot is installed in the channel where you're testing
   - Verify both `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` are correctly set

2. **Permission errors**
   - Make sure the bot has the required scopes
   - Verify the bot is invited to the channel

3. **Socket Mode connection issues**
   - Verify your App-Level Token has `connections:write` scope
   - Check application logs for WebSocket connection errors
   - Ensure your deployment platform (Fly.io) supports persistent connections

### Useful Commands

- Test bot permissions: `curl -H "Authorization: Bearer xoxb-your-token" https://slack.com/api/auth.test`
- Check bot info: `curl -H "Authorization: Bearer xoxb-your-token" https://slack.com/api/users.info?user=BOT_USER_ID`

## Security Notes

- Never commit tokens to version control
- Use environment variables for all sensitive information
- Regularly rotate your tokens
- Monitor your app's usage and logs

---

**Next Steps**: After completing this setup, proceed to [Airtable Setup](airtable-setup.md) to configure your Airtable integration.
